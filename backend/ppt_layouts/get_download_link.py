import base64
def get_link(file_path : str):
    with open(file_path, "rb") as f:
        ppt_bytes = f.read()

    encoded = base64.b64encode(ppt_bytes).decode('utf-8')

    # Raw data URI link (safe to use as href without tags)
    download_link = f"data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{encoded}"

    return download_link