import os
import shutil
import glob

# image/busub /gray /raw 内のファイルを一括削除
def remove_images():
    file_list = glob.glob('media/image/*.jpg')
    for file in file_list:
        os.remove(file)

    file_list = glob.glob('media/image/*')
    for file in file_list:
        shutil.rmtree(file)

    os.makedirs('media/image/raw')
    os.makedirs('media/image/bgsub')
    os.makedirs('media/image/gray')
    os.makedirs('media/image/result')

if __name__ == '__main__':
    remove_images()
