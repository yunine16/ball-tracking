import os
import shutil
import glob
import cv2

# image/busub /gray /raw 内のファイルを一括削除
def remove_images():
    file_list = glob.glob('media/image/*.jpg')
    for file in file_list:
        os.remove(file)

    folder_list = glob.glob('media/image/*')
    for folder in folder_list:
        shutil.rmtree(folder)

    os.makedirs('media/image/raw')
    os.makedirs('media/image/bgsub')
    os.makedirs('media/image/gray')

if __name__ == '__main__':
    remove_images()
