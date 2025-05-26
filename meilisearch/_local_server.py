"""Local Meilisearch server management utilities."""

from __future__ import annotations

import atexit
import os
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional, Tuple
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen


class LocalMeilisearchServer:
    """Manages a local Meilisearch server instance."""

    def __init__(
        self,
        port: int = 7700,
        data_path: Optional[str] = None,
        master_key: Optional[str] = None,
    ):
        self.port = port
        self.data_path = data_path or tempfile.mkdtemp(prefix="meilisearch_")
        self.master_key = master_key
        self.process: Optional[subprocess.Popen] = None
        self.binary_path: Optional[str] = None
        self.url = f"http://127.0.0.1:{self.port}"
        self._temp_data_dir = data_path is None

    def _find_meilisearch_binary(self) -> Optional[str]:
        """Find Meilisearch binary in PATH or common locations."""
        # First, check if 'meilisearch' is in PATH
        binary_name = "meilisearch" if platform.system() != "Windows" else "meilisearch.exe"
        binary_path = shutil.which(binary_name)
        if binary_path:
            return binary_path

        # Check common installation locations
        common_paths = []
        if platform.system() == "Darwin":  # macOS
            common_paths.extend(
                [
                    "/usr/local/bin/meilisearch",
                    "/opt/homebrew/bin/meilisearch",
                    str(Path.home() / ".local" / "bin" / "meilisearch"),
                ]
            )
        elif platform.system() == "Linux":
            common_paths.extend(
                [
                    "/usr/local/bin/meilisearch",
                    "/usr/bin/meilisearch",
                    str(Path.home() / ".local" / "bin" / "meilisearch"),
                ]
            )

        for path in common_paths:
            if Path(path).exists() and Path(path).is_file():
                return path

        return None

    def _download_meilisearch(self) -> str:
        """Download Meilisearch binary for the current platform."""
        system = platform.system().lower()
        machine = platform.machine().lower()

        # Map platform to Meilisearch release names
        if system == "darwin":
            if machine in ["arm64", "aarch64"]:
                platform_str = "apple-silicon"
            else:
                platform_str = "amd64"
            binary_name = f"meilisearch-macos-{platform_str}"
        elif system == "linux":
            if machine in ["x86_64", "amd64"]:
                platform_str = "amd64"
            elif machine in ["aarch64", "arm64"]:
                platform_str = "aarch64"
            else:
                raise RuntimeError(f"Unsupported Linux architecture: {machine}")
            binary_name = f"meilisearch-linux-{platform_str}"
        else:
            raise RuntimeError(f"Unsupported platform: {system}")

        # Download the latest release
        download_url = (
            f"https://github.com/meilisearch/meilisearch/releases/latest/download/{binary_name}"
        )

        # Create a temporary directory for the binary
        binary_dir = Path.home() / ".meilisearch" / "bin"
        binary_dir.mkdir(parents=True, exist_ok=True)
        binary_path = binary_dir / "meilisearch"

        # Download if not already present
        if not binary_path.exists():
            print(f"Downloading Meilisearch binary from {download_url}...")
            try:
                with urlopen(download_url, timeout=300) as response:
                    with open(binary_path, "wb") as f:
                        f.write(response.read())
                # Make it executable
                binary_path.chmod(0o755)
                print(f"Downloaded Meilisearch to {binary_path}")
            except Exception as e:
                raise RuntimeError(f"Failed to download Meilisearch: {e}") from e

        return str(binary_path)

    def start(self) -> None:
        """Start the local Meilisearch server."""
        if self.process and self.process.poll() is None:
            return  # Already running

        # Find or download Meilisearch binary
        self.binary_path = self._find_meilisearch_binary()
        if not self.binary_path:
            try:
                self.binary_path = self._download_meilisearch()
            except Exception as e:
                raise RuntimeError(
                    "Meilisearch binary not found in PATH. "
                    "Please install Meilisearch: https://www.meilisearch.com/docs/learn/getting_started/installation"
                ) from e

        # Prepare command
        cmd = [
            self.binary_path,
            "--http-addr",
            f"127.0.0.1:{self.port}",
            "--db-path",
            self.data_path,
            "--no-analytics",
        ]

        if self.master_key:
            cmd.extend(["--master-key", self.master_key])

        # Start the process
        try:
            # pylint: disable=consider-using-with
            # We don't use 'with' here because we want the process to run in the background
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )

            # Register cleanup on exit
            atexit.register(self.stop)

            # Wait for server to be ready
            self._wait_for_server()

        except Exception as e:
            self.stop()
            raise RuntimeError(f"Failed to start Meilisearch: {e}") from e

    def _wait_for_server(self, timeout: int = 30) -> None:
        """Wait for the server to be ready."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with urlopen(f"{self.url}/health", timeout=1) as response:
                    if response.status == 200:
                        return
            except (OSError, URLError):
                pass

            # Check if process has died
            if self.process and self.process.poll() is not None:
                stdout, stderr = self.process.communicate()
                raise RuntimeError(
                    f"Meilisearch process died unexpectedly. "
                    f"stdout: {stdout.decode()}, stderr: {stderr.decode()}"
                )

            time.sleep(0.1)

        raise RuntimeError("Meilisearch server failed to start within timeout")

    def stop(self) -> None:
        """Stop the local Meilisearch server."""
        if self.process and self.process.poll() is None:
            # Try graceful shutdown first
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if needed
                if sys.platform == "win32":
                    self.process.kill()
                else:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                self.process.wait()

            self.process = None

        # Clean up temporary data directory
        if self._temp_data_dir and os.path.exists(self.data_path):
            try:
                shutil.rmtree(self.data_path)
            except OSError:
                pass  # Ignore cleanup errors

    def __del__(self) -> None:
        """Ensure cleanup on object destruction."""
        self.stop()


def parse_url_components(url: str) -> Tuple[str, int]:
    """Parse URL to extract host and port."""
    parsed = urlparse(url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 7700
    return host, port
