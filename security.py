from PIL import Image
import imagehash
# store hashes
stored_hashes = []
def generate_hash(image_path):
    image = Image.open(image_path)
    return imagehash.phash(image)
def is_duplicate(new_hash):
    for old_hash in stored_hashes:
        if new_hash - old_hash < 10:
            return True
    return False
def check_image(image_path):
    new_hash = generate_hash(image_path)   
    if is_duplicate(new_hash):
        return "🚫 BLOCKED: Image already exists"
    else:
        stored_hashes.append(new_hash)
        return "✅ SAFE"
if __name__ == "__main__": 
 print(check_image(r"C:\original_photo.jpeg")) 
 print(check_image(r"C:\screenshot_of_photo.jpeg")) 
 print(check_image(r"C:\original_photo.jpeg")) 