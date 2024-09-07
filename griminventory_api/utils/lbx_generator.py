import re
import zipfile
from io import BytesIO
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os

# Set up Jinja2 environment
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "../templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)


# Custom filter to minify XML
def minify_xml(xml_str):
    """Removes unnecessary whitespaces and line breaks."""
    return re.sub(r">\s+<", "><", xml_str.strip())


def render_template(template_name: str, context: dict) -> str:
    """Render a Jinja2 template with the given context."""
    template = env.get_template(template_name)
    return minify_xml(template.render(context))


def create_lbx_file(qr_data: str, text_data: str) -> bytes:
    """Generate a .lbx file with the given QR code and text data."""

    # Create context for label.xml
    label_context = {
        "qr": qr_data,
        "title": text_data,
    }

    # Create context for prop.xml
    now = datetime.now()
    prop_context = {
        "title": text_data,
        "creator": "Notion Exporter",
        "template": "Standard Label",
        "created_time": now,
        "modified_time": now,
        "revision": "1",
        "edit_time": "6",
    }

    # Render XML files from templates
    label_xml = render_template("label.xml.j2", label_context)
    prop_xml = render_template("prop.xml.j2", prop_context)

    # Create a ZIP file (LBX format) in memory
    lbx_io = BytesIO()
    with zipfile.ZipFile(lbx_io, "w", zipfile.ZIP_DEFLATED) as lbx_zip:
        lbx_zip.writestr("label.xml", label_xml)
        lbx_zip.writestr("prop.xml", prop_xml)

    # Return the ZIP file content as bytes
    return lbx_io.getvalue()
