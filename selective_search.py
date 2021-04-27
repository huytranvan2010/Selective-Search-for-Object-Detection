import argparse
import random
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-m", "--method", type=str, default="fast", choices=["fast", "quality"], help="selective search method")
args = vars(ap.parse_args())

# load ảnh
image = cv2.imread(args["image"])

# khởi tạo OpenCV's selective search implementation và set the input image
ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
ss.setBaseImage(image)

# Lựa chọn internal mode of operation của Selective search
if args["method"] == "fast":
    print("[INFO] using *fast* selective search")
    ss.switchToSelectiveSearchFast()

# otherwise we are using the *slower* but *more accurate* version
else:
    print("[INFO] using *quality* selective search")
    ss.switchToSelectiveSearchQuality()

# chạy selective search trên image đầu vào
start = time.time()
rects = ss.process()    # để thực hiện Selective search, trả về list of rectangles
end = time.time()

# Xem selective search chạy mất bao lâu
print("[INFO] selective search took {:.4f} seconds".format(end - start))
print("[INFO] {} tổng số region proposals".format(len(rects)))

# Vẽ ra các region proposals cho từng nhớm, do có nhiều proposals regions nên chia ra
for i in range(0, len(rects), 100):
    # copy ảnh ban đầu để vẽ
    clone = image.copy()

    # duyệt qua các regions proposals trong nhóm
    for (x, y, w, h) in rects[i:i + 100]:
        color = [random.randint(0, 255) for j in range(0, 3)]   # tạo color ngẫu nhiên
        cv2.rectangle(clone, (x, y), (x + w, y + h), color, 2)

    cv2.imshow("Output", clone)

    if cv2.waitKey(0) & 0xFF == ord("q"):   # nhấn "q" thì thoát ra luôn, nhấm phím khác nó quay lên vòng lặp
        break

""" 
Một bức ảnh kích thước nhỏ, chạy chế độ 'fast' cần tới 7.5 seconds (i5-6300U, 8Gb Ram) để có thể trích xuất
các regions of proposals
"""