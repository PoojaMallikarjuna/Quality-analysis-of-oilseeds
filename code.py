import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
import os

GradeA: float = 0.00
GradeB: float = 0.00
GradeC: float = 0.00
def get_classificaton(ratio):
    ratio = round(ratio, 1)
    toret = ""
    if (ratio >= 1):
        toret = "Grade A"
    elif (ratio >= 0.7):
        toret = "Grade B"
    else:
        toret = "Grade C"

    toret = "(" + toret + ")"
    return toret


aspect_ratio = []
cv2_file = []
counter = 0
total_number = len(os.listdir("C:/Users/91874/PycharmProjects/final/photos"))
for file in glob.glob("C:/Users/91874/PycharmProjects/final/photos/*.jpg"):
    img = cv2.imread(file, 0)
    ret, binary = cv2.threshold(img, 160, 255,
                                cv2.THRESH_BINARY)  # 160 - threshold, 255 - value to assign, THRESH_BINARY_INV - Inverse binary

    # averaging filter
    kernel = np.ones((5, 5), np.float32) / 25
    dst = cv2.filter2D(binary, -1, kernel)
    dst = cv2.medianBlur(dst, 5)
    # -1 : depth of the destination image
    #

    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    print(kernel2)

    # erosion
    erosion = cv2.erode(dst, kernel2, iterations=15)

    # dilation
    dilation = cv2.dilate(erosion, kernel2, iterations=15)

    # edge detection
    edges = cv2.Canny(dilation, 100, 200)
    plt.subplot(131), plt.imshow(edges)
    plt.show()

    # ### Size detection
    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print("No. of seeds=", len(contours))
    total_ar = 0
    total_sum = 0
    total_average = 0
    num = len(contours)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        if (aspect_ratio < 0.8):
            aspect_ratio = 1 / aspect_ratio
            print(round(aspect_ratio, 2), get_classificaton(aspect_ratio))

        total_ar += aspect_ratio
        num = len(contours)
        avg_ar = (total_ar / num)
        print("Average Aspect Ratio=", round(avg_ar, 2), get_classificaton(avg_ar))
        total_sum = (total_sum) + round(avg_ar, 2)
        if round(avg_ar, 2) >= 1.00:
            GradeA = GradeA + 1
        elif round(avg_ar, 2) >= 0.70:
            GradeB = GradeB + 1
        else:
            GradeC = GradeC + 1


# plot the images
# imgs_row = 2
# imgs_col = 3
##plt.subplot(imgs_row, imgs_col, 1), plt.imshow(img, 'gray')
# plt.title("Original image")

# ff = cv2_file.append(img)
# print(ff)

# plt.subplot(imgs_row, imgs_col, 2), plt.imshow(binary, 'gray')
# plt.title("Binary image")

# plt.subplot(imgs_row, imgs_col, 3), plt.imshow(dst, 'gray')
# plt.title("Filtered image")

# plt.subplot(imgs_row, imgs_col, 4), plt.imshow(erosion, 'gray')
# plt.title("Eroded image")

# plt.subplot(imgs_row, imgs_col, 5), plt.imshow(dilation, 'gray')
# plt.title("Dialated image")

# plt.title("Edge detect")

# plt.show()
print()
print("Number of seeds in GradeA : ",GradeA)
print("Number of seeds in GradeB : ",GradeB)
print("Number of seeds in GradeC : ",GradeC)
total = GradeA + GradeB + GradeC
print()
print("% of GradeA : ",round(((GradeA/total)*100),2),"%")
print("% of GradeB : ",round(((GradeB/total)*100),2),"%")
print("% of GradeC : ",round(((GradeC/total)*100),2),"%")
