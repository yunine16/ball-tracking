import glob
import os
import main
import cv2
import remove_img

# video内の全ファイルについて解析を行う
def analize_onefile():
    file_list = glob.glob('media/video/*')
    first_flg = True

    for file in file_list:
        print(file)
        b = int(input('input B number'))
        g = int(input('input G number'))
        r = int(input('input R number'))

        main.save_frames(file,'media/image/')
        main.backgroundsub()

        for path in glob.glob("media/image/bgsub/frame_*.jpg"):
            main.grayscale(path)

        main.grayscale('media/template.jpg')
        location_list = main.template_matching()
        file = os.path.splitext(os.path.basename(file))[0]

        if first_flg:
            source = "media/image/raw/frame_0.jpg"
            first_flg = False
        else:
            source = "media/result/result.jpg"

        result_img = draw_rectangle(location_list,b,g,r,source)
        cv2.imwrite('media/result/result.jpg', result_img)
        
        print(file + ' completed!!')
        remove_img.remove_images()


def draw_rectangle(location_list,b,g,r,SOURCE):
    """
    マッチング結果を画像に描画する
    """
    source = cv2.imread(SOURCE)
    cv2.imwrite("media/result/result.jpg", source)
    template_img = cv2.imread("media/image/gray/template.jpg")
    w, h, _ = template_img.shape
    for loc in location_list:
        x, y = round(loc[0] + w/2), round(loc[1] + h/2)
        img = cv2.drawMarker(source, (x,y), (b, g, r), markerType=cv2.MARKER_TILTED_CROSS, thickness=2)

    return img


if __name__ == '__main__':
    analize_onefile()