# -*- coding: utf-8 -*-
import glob
import re
import cv2
import csv
import os

VIDEOPATH = "media/video/"
IMAGEPATH = "media/image/"
TEMPLATEPATH = "media/template.jpg"

def save_frames(video_path, image_dir):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("video cannot opened")
        return

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    n = 0

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}/raw/{}_{}.{}'.format(IMAGEPATH, "frame", str(n), "jpg"), frame)
            n += 1
        else:
            return

def grayscale(image_path):
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25,2)
    save_image(image_path, "gray", img_thresh)

def backgroundsub():
    """
    背景差分
    """
    img_list = glob.glob(IMAGEPATH + "raw/frame_*.jpg")
    img_list = sorted(img_list, key=lambda val: int(re.sub("\D","",val)))
    source = img_list[0]
    for path in img_list:
        diff = cv2.absdiff(cv2.imread(source), cv2.imread(path))
        source = path
        save_image(path, "bgsub", diff)

def template_matching():
    """
    テンプレート画像とフレーム画像でテンプレートマッチングを行う
    """
    template_img = cv2.imread(IMAGEPATH + "gray/template.jpg")
    img_list = glob.glob(IMAGEPATH + "gray/frame_*.jpg")
    def num(val): return int(re.sub("\D", "", val))
    img_list = sorted(img_list, key=(num))
    location_list = []
    for path in img_list:
        img =cv2.imread(path)
        result = cv2.matchTemplate(img, template_img, cv2.TM_CCOEFF)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        location_list.append(maxLoc)

    return location_list


def draw_rectangle(location_list,b,g,r):
    """
    マッチング結果を画像に描画する
    """
    source = cv2.imread(IMAGEPATH + "raw/frame_0.jpg")
    cv2.imwrite(IMAGEPATH + "result.jpg", source)
    template_img = cv2.imread(IMAGEPATH + "gray/template.jpg")
    w, h, _ = template_img.shape
    for loc in location_list:
        x, y = round(loc[0] + w/2), round(loc[1] + h/2)
        img = cv2.drawMarker(source, (x,y), (b, g, r), markerType=cv2.MARKER_TILTED_CROSS, thickness=2)

    return img


def save_image(img_path, dir, img):
    """
    画像保存
    img_path : 画像のパス
    dir : ディレクトリ名
    img : 画像データ
    """
    file_name = img_path.replace("\\","/").split(".")[0].split("/")[-1]
    cv2.imwrite("{}{}/{}.{}".format(IMAGEPATH, dir, file_name, "jpg"), img)

def create_csv(file_name,location_list):
    file = open(file_name, 'w')
    writer = csv.writer(file)
    writer.writerow(['x座標','y座標'])
    template_img = cv2.imread(IMAGEPATH + "gray/template.jpg")
    w, h, _ = template_img.shape
    for loc in location_list:
        x, y = round(loc[0] + w/2), round(loc[1] + h/2)
        writer.writerow([x,y])

if __name__=="__main__":
    print("動画ファイル名を入力")
    video_name = input()
    VIDEOPATH = VIDEOPATH + video_name
    video_name = os.path.splitext(os.path.basename(video_name))[0]
    print(VIDEOPATH)
    save_frames(VIDEOPATH,IMAGEPATH)

    backgroundsub()
    grayscale(TEMPLATEPATH)
    for path in glob.glob(IMAGEPATH + "bgsub/frame_*.jpg"):
        grayscale(path)

    location_list = template_matching()
    print("画像で出力:0、CSVで出力:1")
    output = input()
    if int(output) == 0:
        img = draw_rectangle(location_list,0,255,0)
        cv2.imwrite('media/result/result.jpg', img)
    else:
        create_csv("media/result/" + video_name + ".csv",location_list)