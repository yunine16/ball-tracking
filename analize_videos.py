import glob
import os
import main
import cv2
import remove_img

# video内の全ファイルについて解析を行う
def analize_videos(output):
    file_list = glob.glob('media/video/*')

    for file in file_list:
        main.save_frames(file,'media/image/')

        main.backgroundsub()
        main.grayscale('media/template.jpg')
        for path in glob.glob("media/image/bgsub/frame_*.jpg"):
            main.grayscale(path)

        location_list = main.template_matching()
        file = os.path.splitext(os.path.basename(file))[0]

        if output == 0:
            result_img = main.draw_rectangle(location_list,0,255,0)
            cv2.imwrite('media/result/' + file + '.jpg', result_img)
        else:
            main.create_csv("media/result/" + file + 'csv', location_list)

        print(file + ' completed!!')
        remove_img.remove_images()


if __name__ == '__main__':
    print("画像で出力:0 CSVで出力:1")
    output = int(input())
    analize_videos(output)