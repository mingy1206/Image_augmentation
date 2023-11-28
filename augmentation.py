import os
import random
import numpy as np
import cv2
from PIL import Image, ImageEnhance
from keras.preprocessing.image import ImageDataGenerator, img_to_array


def random_hue_change(image, hue_range=30):
    img = np.array(image)[:, :, ::-1]
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_delta = random.randint(-hue_range, hue_range)
    hsv_img[:, :, 0] = (hsv_img[:, :, 0] + hue_delta) % 180
    new_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)[:, :, ::-1]
    return Image.fromarray(new_img)

def add_gaussian_noise(image):
    row, col, ch = image.shape
    mean = 0
    sigma = 25
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy_image = image + gauss
    noisy_image = np.clip(noisy_image, 0, 255)  # To ensure we have valid pixel values
    return noisy_image

# ImageDataGenerator Configuration
datagen = ImageDataGenerator(
    rotation_range=5,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=40.0,
    zoom_range=0.1,
    fill_mode='nearest')

# Paths and Constants
input_root_folder_path = 'data/'    #The folder you want to open
output_folder_path = 'result'       #The folder you want to save result
invert_probability = 0.5
file_number = 1                     #Start name number
# Create output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Process each image
for folder in os.listdir(input_root_folder_path):
    input_folder_path = os.path.join(input_root_folder_path, folder)
    for file_name in os.listdir(input_folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder_path, file_name)
            original_image = Image.open(image_path).resize((620, 620))

            # Save original image
            original_image.save(os.path.join(output_folder_path, f"{file_number}.jpg"))
            file_number += 1

            # Perform augmentation 3 times for each image
            #invert_probability is 0.5
            for _ in range(3):
                aug_image = original_image.copy()
                if random.random() < invert_probability:
                    aug_image = aug_image.transpose(Image.FLIP_LEFT_RIGHT)
                if random.random() < invert_probability:
                    aug_image = aug_image.transpose(Image.FLIP_TOP_BOTTOM)

                # In the main augmentation loop
                aug_image = random_hue_change(aug_image)
                aug_image = ImageEnhance.Brightness(aug_image).enhance(random.uniform(0.8, 1.2))  # Moderate brightness change
                aug_image = ImageEnhance.Color(aug_image).enhance(random.uniform(0.8, 1.2))  # Moderate color enhancement

                # Convert PIL image to numpy array for Keras ImageDataGenerator
                x = img_to_array(aug_image)
                x = x.reshape((1,) + x.shape)

                # Apply Keras ImageDataGenerator augmentations
                #
                for batch in datagen.flow(x, batch_size=1):
                    # Convert numpy array batch to PIL Image
                    batch_image = Image.fromarray(batch[0].astype('uint8'), 'RGB')

                    # Convert PIL Image to numpy array for Gaussian noise addition
                    noisy_image_array = img_to_array(batch_image)

                    # Add Gaussian noise
                    noisy_image_array = add_gaussian_noise(noisy_image_array)

                    # Convert numpy array back to PIL image
                    final_image = Image.fromarray(np.uint8(noisy_image_array))

                    # Save the final augmented image to file_number
                    final_image.save(os.path.join(output_folder_path, f"{file_number}.jpg"))
                    break
                # file_number++
                file_number += 1