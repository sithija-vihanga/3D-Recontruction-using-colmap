import os
import cv2

def compare_sift_properties(image1_path, image2_path):
    # Load images
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and descriptors for both images
    keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

    # Initialize a BFMatcher (Brute Force Matcher) with default params
    bf = cv2.BFMatcher()

    # Match descriptors using KNN (K-Nearest Neighbors)
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Apply ratio test to find good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Return the number of common keypoints
    return len(good_matches)

# Directory containing images
image_directory = "sift_ordering/"

# Function to find the image with the most common SIFT keypoints
def find_best_reference_image(images):
    max_keypoints = -1
    best_reference_image = None
    for filename in images:
        image_path = os.path.join(image_directory, filename)
        num_common_keypoints = compare_sift_properties(reference_image_path, image_path)
        if num_common_keypoints > max_keypoints:
            max_keypoints = num_common_keypoints
            best_reference_image = image_path
    return best_reference_image

# List to store the order of images
ordered_images = []

# Initial reference image
reference_image_path = os.path.join(image_directory, "001.jpg")

# Get a list of all image files in the directory
image_files = [filename for filename in os.listdir(image_directory) if filename.endswith(".jpg")]

# Iterate through images and reorder based on SIFT features
while image_files:
    # Find the best reference image from the remaining images
    new_reference_image = find_best_reference_image(image_files)

    # Remove the new reference image from the list
    image_files.remove(os.path.basename(new_reference_image))

    # Add the new reference image to the ordered list
    ordered_images.append(os.path.basename(new_reference_image))

# Print the final ordered list of images
print("Final ordered images based on SIFT properties (highest to lowest):")
for filename in ordered_images:
    print(filename)

for idx, filename in enumerate(ordered_images, start=1):
    original_path = os.path.join(image_directory, filename)
    new_filename = f"IM{str(idx).zfill(3)}.jpg"  # Format the new filename as IM001, IM002, ...
    new_path = os.path.join(image_directory, new_filename)
    os.rename(original_path, new_path)

    # Update the reference image path if it's being renamed
    if original_path == reference_image_path:
        reference_image_path = new_path
