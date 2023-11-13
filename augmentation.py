import random
import numpy as np
import os
import cv2
from PIL import Image, ImageEnhance, ImageChops
import albumentations as A
import matplotlib.pyplot as plt
# 데이터 증강을 적용할 최상위 폴더
input_root_folder_path = 'data/'

# 증강된 이미지를 저장할 최상위 폴더
output_folder_path = 'result'

# 데이터 증강 확률
invert_probability = 0.5
#file name 1부터 시작
file_number = 1


def add_shear(image, intensity):
    width, height = image.size
    # 수평 전단 변환 매트릭스 생성
    m = random.uniform(-intensity, intensity)
    xshift = abs(m) * width
    new_width = width + int(round(xshift))
    shear = (1, m, -xshift if m > 0 else 0, 0, 1, 0)
    return image.transform((new_width, height), Image.AFFINE, shear, Image.BICUBIC)


def random_hue_change(image, hue_range=8):
    # OpenCV를 사용하여 PIL 이미지를 NumPy 배열로 변환 (RGB to BGR)
    img = np.array(image)[:, :, ::-1]

    # RGB 이미지를 HSV 이미지로 변환
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Hue 채널을 랜덤하게 변경 (더 작은 범위)
    hue_delta = random.randint(-hue_range, hue_range)
    hsv_img[:, :, 0] = (hsv_img[:, :, 0] + hue_delta) % 180

    # HSV 이미지를 다시 RGB 이미지로 변환
    new_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)[:, :, ::-1]

    # NumPy 배열을 PIL 이미지로 변환
    return Image.fromarray(new_img)

for folder in os.listdir(input_root_folder_path):
    input_folder_path = os.path.join(input_root_folder_path, folder)
# 출력 폴더 생성 (존재하지 않을 경우)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)



    # 폴더의 모든 이미지 파일에 대해 반복
    for file_name in os.listdir(input_folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder_path, file_name)
            image = Image.open(image_path)

            # resize
            image = image.resize((620, 620))

            # 원본 이미지 저장
            output_file_name = f"{file_number}.jpg"
            image.save(os.path.join(output_folder_path, output_file_name))
            file_number += 1  # 파일 번호 증가
            for augmentation_index in range(1, 4):  # 세 번의 데이터 증강을 위한 루프
                image = image.copy()

                # 이미지 좌우 반전
                if random.random() < invert_probability:
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)

                # 밝기, 채도, 색상 등의 증강 작업은 여기에 추가
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(random.uniform(0.7, 1.5))

                change_color = ImageEnhance.Color(image)
                image = change_color.enhance(random.uniform(0.5, 2.0))

                image = random_hue_change(image)

                # 이미지 기울이기, 전단, 노이즈 추가
                image = image.rotate(random.randrange(-10, 10))
                image = add_shear(image, 0.1)

                image = np.array(image)  # PIL 이미지를 NumPy 배열로 변환
                row, col, ch = image.shape
                mean = 0
                var = 0.1
                sigma = var ** 0.4
                gauss = np.random.normal(mean, sigma, (row, col, ch))
                gauss = gauss.reshape(row, col, ch)
                noisy_array = image + gauss
                image = Image.fromarray(np.uint8(noisy_array)).convert('RGB')

                # resize 및 저장
                image = image.resize((620, 620))
                output_file_name = f"{file_number}.jpg"
                image.save(os.path.join(output_folder_path, output_file_name))

                file_number += 1





            '''
            # 좌우 이동
            width, height = image.size
            shift = random.randint(0, width * 0.2)
            image = ImageChops.offset(image, shift, 0)
            image.paste((0), (0, 0, shift, height))
            '''
