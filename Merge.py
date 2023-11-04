from PIL import Image
import os

def slice_image(input_image_path, output_folder):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    tile_size = 256

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(0, width, tile_size):
        for j in range(0, height, tile_size):
            left = i
            upper = j
            right = i + tile_size
            lower = j + tile_size

            small_image = original_image.crop((left, upper, right, lower))
            small_image.save(os.path.join(output_folder, f"{i}_{j}.png"))

def merge_images(input_folder, output_image_path, original_width):
    images = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            x, y = map(int, filename[:-4].split("_"))  # Extract coordinates from filename
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            images.append((x, y, img))

    if not images:
        print("No images found in the input folder.")
        return

    # Sort images based on their coordinates
    images.sort(key=lambda x: (x[1], x[0]))

    # Calculate total width and height of the merged image
    total_width = images[0][2].width * (original_width // images[0][2].width)
    total_height = images[0][2].height * ((len(images) // (original_width // images[0][2].width)) + 1)

    # Create a new image with the calculated dimensions
    merged_image = Image.new("RGB", (total_width, total_height))

    # Paste small images onto the merged image
    x_offset = 0
    y_offset = 0
    for _, _, img in images:
        merged_image.paste(img, (x_offset, y_offset))
        x_offset += img.width
        if x_offset >= total_width:
            x_offset = 0
            y_offset += img.height

    merged_image.save(output_image_path)




# Example usage:
input_image_path = "input/image.jpg"
output_folder = "immediate"
output_image_path = "output/output.jpg"

#slice_image(input_image_path, output_folder)
merge_images(output_folder, output_image_path ,1500)
