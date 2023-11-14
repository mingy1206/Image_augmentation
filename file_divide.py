import os
import shutil
from math import ceil
import re


def extract_number(s):
    # 파일 이름에서 숫자 추출
    match = re.search(r'\d+', s)
    return int(match.group()) if match else float('inf')
def copy_files_to_folders_in_order(source_folder, destination_folder, number_of_folders):
    # 소스 폴더에서 파일 목록을 가져오기
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    # 숫자크기순으로 오름차순 정렬
    files.sort(key=extract_number)

    total_files = len(files)
    # 총 파일 수 / 나누는 폴더 수 = 폴더당 파일 수
    files_per_folder = ceil(total_files / number_of_folders)

    # divide and create folder
    for i in range(number_of_folders):
        folder_name = os.path.join(destination_folder, f'folder_{i + 1}')
        os.makedirs(folder_name, exist_ok=True)

        # 하나의 폴더를 채우고 다음 폴더로 이동
        for file in files[i * files_per_folder:(i + 1) * files_per_folder]:
            shutil.copy(os.path.join(source_folder, file), folder_name)

# Run
source_folder = 'result'  #파일경로
divide_folder = 'divide'  #나눠진 폴더들의 우치
number_of_folders = 5  # 나눠지는 폴더의 수

copy_files_to_folders_in_order(source_folder, divide_folder, number_of_folders)
