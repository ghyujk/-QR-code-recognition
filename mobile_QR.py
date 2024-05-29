# 导入必要的包
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

# 构造参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# 初始化视频流并让相机传感器预热
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# 打开输出CSV文件写入并初始化
# 到目前为止找到的条形码
csv = open(args["output"], "w")
found = set()

# 循环视频流中的帧
while True:
	#  最大宽度为 400 像素
	frame = vs.read()
	frame = imutils.resize(frame, width=800)

	# 找到框架中的条形码并解码每个条形码
	barcodes = pyzbar.decode(frame)
	
	
    # 遍历检测到的条形码
	for barcode in barcodes:
		# 提取条形码的边界框位置并绘制
		# 图像上条形码周围的边界框
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

		# 条形码数据是一个字节对象，所以如果我们想绘制它
		# 在我们的输出图像上，我们需要先将其转换为字符串
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type

		# 在图像上绘制条码数据和条码类型
		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		# 如果条形码文本当前不在我们的 CSV 文件中，请写入
		# 时间戳+条形码到磁盘并更新集合
		if barcodeData not in found:
			csv.write("{},{}\n".format(datetime.datetime.now(),
				barcodeData))
			csv.flush()
			found.add(barcodeData)
			
            	
                
                # 显示输出帧
	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF

	# 如果按下'q'键，则退出循环
	if key == ord("q"):
		break

# 关闭输出 CSV 文件做一些清理
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()