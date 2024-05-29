import cv2
from cv2 import CV_16U
print('cv2.__version__:',cv2.__version__)
img = cv2.imread("D:/code CODE/point_color/triangle/triangle.jpg")
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # 转换为灰度图
thresh,img_bin = cv2.threshold(img,127,255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
print('thresh:',thresh)
cv2.imshow('img_bin',img_bin)
cv2.imwrite('save.jpg',img_bin)
cv2.waitKey(0)
cv2.destroyAllWindows()