import glob
import re
import cv2

VIDEOPATH = "media/video/test5.mp4"
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
    img_list = glob.glob(IMAGEPATH + "gray/frame_*.jpg")
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
    img_list = glob.glob(IMAGEPATH + "bgsub/frame_*.jpg")
    def num(val): return int(re.sub("\D", "", val))
    img_list = sorted(img_list, key=(num))
    location_list = []
    for path in img_list:
        result = cv2.matchTemplate(cv2.imread(
            path), template_img, cv2.TM_CCOEFF)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        location_list.append(maxLoc)


        lx, ly, rx, ry = maxLoc[0] - 20, maxLoc[1] - 20, maxLoc[0] + 20, maxLoc[1] + 20
        img = cv2.rectangle(cv2.imread(path), (lx, ly), (rx, ry), (0, 255, 0), 3)
        save_image(path, "result", img)

    return location_list


def draw_rectangle(location_list):
    """
    マッチング結果を画像に描画する
    """
    source = cv2.imread(IMAGEPATH + "raw/frame_0.jpg")
    cv2.imwrite(IMAGEPATH + "result.jpg", source)
    source = cv2.imread(IMAGEPATH + "result.jpg")
    index = 0
    for loc in location_list:
        lx, ly, rx, ry = loc[0] - 20, loc[1] - 20, loc[0] + 20, loc[1] +20
        img = cv2.rectangle(source, (lx, ly), (rx, ry), (0, 255, 0), 3)
        # index =index + 1
        # index_img = cv2.rectangle(cv2.imread(IMAGEPATH + "raw/frame_0.jpg"), (lx, ly), (rx, ry), (0, 255, 0), 3)
        # cv2.imwrite(IMAGEPATH + "/result/frame_" + str(index) + ".jpg", index_img)
        cv2.imwrite(IMAGEPATH + "result.jpg", img)


def save_image(img_path, dir, img):
    """
    画像保存
    img_path : 画像のパス
    dir : ディレクトリ名
    img : 画像データ
    """
    file_name = img_path.replace("\\","/").split(".")[0].split("/")[-1]
    cv2.imwrite("{}{}/{}.{}".format(IMAGEPATH, dir, file_name, "jpg"), img)

if __name__=="__main__":
    save_frames(VIDEOPATH,IMAGEPATH)

    grayscale(TEMPLATEPATH)
    for path in glob.glob(IMAGEPATH + "raw/frame_*.jpg"):
        grayscale(path)

    backgroundsub()
    location_list = template_matching()
    draw_rectangle(location_list)
