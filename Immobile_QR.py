# 导入必要的包
from pyzbar import pyzbar
import argparse
import cv2

# 构造参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# 加载输入图像
image = cv2.imread(args["image"])
# 找到图像中的条形码并解码每个条形码
barcodes = pyzbar.decode(image)

# 遍历检测到的条形码
for barcode in barcodes:# 循环读取检测到的条形码
	# 提取条形码的边界框位置并绘制
	# 图像上条形码的边界框
	(x, y, w, h) = barcode.rect
	cv2.rectangle(image, (x, y), (x + w+10, y + h+20), (0, 0, 255), 2)

	# 条形码数据是一个字节对象，所以如果我们想在框上绘制它
	# 我们需要先将输出图像转换为字符串
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type

	# 在图像上绘制条码数据和条码类型
	text = "{} ({})".format(barcodeData, barcodeType)
	cv2.putText(image, text, (70,70), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 0, 255), 2)

	# 将条码类型和数据打印到终端
	print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

# 显示输出图像
cv2.imshow("Image", image)
cv2.waitKey(0)