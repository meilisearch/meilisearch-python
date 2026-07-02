from unittest.mock import patch

import pytest


def test_render_template_calls_route(client):
    """The SDK posts template and input to the render-template route."""
    template = {"kind": "inlineDocumentTemplate", "inline": "Rendered on {{doc.id}}"}
    document = {"kind": "inlineDocument", "inline": {"id": "42"}}

    with patch.object(
        client.http, "post", return_value={"template": "x", "rendered": "y"}
    ) as mock_post:
        client.render_template(template=template, input=document)

    mock_post.assert_called_once_with(
        "render-template",
        body={"template": template, "input": document},
    )


def test_render_template_omits_input_when_none(client):
    """Without an input the body only carries the template."""
    template = {"kind": "inlineDocumentTemplate", "inline": "Rendered on {{doc.id}}"}

    with patch.object(
        client.http, "post", return_value={"template": "x", "rendered": None}
    ) as mock_post:
        client.render_template(template=template)

    mock_post.assert_called_once_with("render-template", body={"template": template})


@pytest.mark.usefixtures("enable_render_route")
def test_render_template_inline(client):
    """Renders an inline template with an inline document."""
    response = client.render_template(
        template={"kind": "inlineDocumentTemplate", "inline": "Rendered on {{doc.id}}"},
        input={"kind": "inlineDocument", "inline": {"id": "42"}},
    )

    assert isinstance(response, dict)
    assert {"template", "rendered"} <= set(response)
    assert "42" in response["rendered"]


@pytest.mark.usefixtures("enable_render_route")
def test_render_template_without_input(client):
    """Omitting the input returns the unrendered template and a null result."""
    response = client.render_template(
        template={"kind": "inlineDocumentTemplate", "inline": "Rendered on {{doc.id}}"},
    )

    assert isinstance(response, dict)
    assert response["rendered"] is None
