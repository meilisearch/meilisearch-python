from meilisearch._httprequests import HttpRequests

class SysInfo:
    """
    Sys-info routes wrapper

    Index's parent that gives access to all the sys-info methods of meilisearch.
    https://docs.meilisearch.com/references/sys-info.html#get-pretty-system-information
    """
    sys_info_path = 'sys-info'

    def __init__(self, config):
        """
        Attributes
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        """
        self.config = config

    def get_sys_info(self):
        """Get system information of meilisearch

        Get information about memory usage and processor usage.

        Returns
        ----------
        sys_info: dict
            Information about memory and processor usage.
        """
        return HttpRequests.get(self.config, self.sys_info_path)
