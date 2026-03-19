from security import check_image

def process_image(image_path):
    """
    Processes an image by checking it for security using the security module.

    Args:
        image_path (str): The file path to the image to be checked.

    Returns:
        dict: A dictionary with the status of the image check.
              - {"status": "SAFE"} if the image is safe.
              - {"status": "BLOCKED"} if the image is blocked.
              - {"status": "ERROR", "message": "error details"} if an error occurs.
    """
    try:
        result = check_image(image_path)
        return {"status": result}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}