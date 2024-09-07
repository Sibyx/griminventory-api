from flask import request, send_file, redirect, Response, Blueprint

from griminventory_api.notion.service import get_notion_page_data
from griminventory_api.utils.lbx_generator import create_lbx_file
from griminventory_api.utils.qr_code_generator import generate_qr_code_image
from io import BytesIO

items = Blueprint("items", __name__)


@items.route("/v1/items/<item_uuid>.png", methods=["GET"])
def generate_qr_code(item_uuid: str) -> Response:
    qr_link = request.url_root.strip("/").replace("http://", "https://") + f"/v1/items/{item_uuid}"
    qr_img = generate_qr_code_image(qr_link)

    img_io = BytesIO()
    qr_img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


@items.route("/v1/items/<item_uuid>.lbx", methods=["GET"])
def generate_lbx_file(item_uuid: str) -> Response:
    """Generates and returns a Brother .lbx file for the Notion item."""
    # Fetch page data from Notion
    notion_data = get_notion_page_data(item_uuid)
    title = notion_data.get("properties", {}).get("Name", {}).get("title", [{}])[0].get("plain_text", "Unknown Item")
    qr_link = request.url_root.strip("/").replace("http://", "https://") + f"/v1/items/{item_uuid}"

    # Generate the binary .lbx content
    lbx_content = create_lbx_file(qr_data=qr_link, text_data=title)

    # Return the LBX file as binary content
    lbx_io = BytesIO()
    lbx_io.write(lbx_content)
    lbx_io.seek(0)

    return send_file(lbx_io, mimetype="application/zip", as_attachment=True, download_name=f"{title}.lbx")


@items.route("/v1/items/<item_uuid>", methods=["GET"])
def redirect_to_notion(item_uuid: str) -> Response:
    notion_data = get_notion_page_data(item_uuid)
    notion_url = notion_data.get("url").replace("https://", "notion://")
    if notion_url:
        return redirect(notion_url)
    else:
        return Response("Notion page not found", status=404)
