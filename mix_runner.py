import cv2
import numpy as np
import os
import csv
import imutils

IMG_PATH = "images"
LOWER_PURPLE = [0, 0, 0]
UPPER_PURPLE = [255, 255, 255]
MIN_AREA = 0
RESIZE_BY_WIDTH = 1000.

SHOW_IMG = False

def resize_by_width(image, size=RESIZE_BY_WIDTH):
	# Resize by opencv
	W = size
	height, width, depth = image.shape
	imgScale = W / width
	newX, newY = image.shape[1] * imgScale, image.shape[0] * imgScale
	img_coppy = cv2.resize(image, (int(newX), int(newY)))

	return img_coppy

def hsv(image):

	out_image = image.copy()

	# STEP 1
	img_coppy1 = image.copy()
	hsv1 = cv2.cvtColor(img_coppy1, cv2.COLOR_BGR2HSV)
	mask1 = cv2.inRange(hsv1, np.array(LOWER_PURPLE), np.array(UPPER_PURPLE))
	res1 = cv2.bitwise_and(img_coppy1, img_coppy1, mask=mask1)
	blur1 = cv2.GaussianBlur(res1, (7, 7), 0)
	# kernel = np.ones((5, 5), np.uint8)
	# dilation = cv2.dilate(blur, kernel, iterations=1)
	edges1 = cv2.Canny(blur1, 100, 200)
	new_edges1, contours1, hierarchy1 = cv2.findContours(edges1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
	best_cnt1 = best_contours(contours1)
	img_contours1 = cv2.drawContours(img_coppy1, best_cnt1, -1, (0, 255, 0), 3)

	# STEP 2
	img_coppy2 = img_contours1.copy()
	hsv2 = cv2.cvtColor(img_coppy2, cv2.COLOR_BGR2HSV)
	mask2 = cv2.inRange(hsv2, np.array([0, 230, 255]), np.array([255, 255, 255]))
	res2 = cv2.bitwise_and(img_coppy2, img_coppy2, mask=mask2)

	blur2 = cv2.GaussianBlur(res2, (7, 7), 0)
	# kernel = np.ones((5, 5), np.uint8)
	# dilation = cv2.dilate(blur, kernel, iterations=1)
	edges2 = cv2.Canny(blur2, 100, 200)
	new_edges2, contours2, hierarchy2 = cv2.findContours(edges2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	best_cnt2 = best_contours(contours2)
	img_coppy2 = cv2.drawContours(out_image, best_cnt2, -1, (0, 255, 0), 1)
	print("Area contour: " + str(cv2.contourArea(best_cnt2)))
	return new_edges2, img_coppy2, best_cnt2

def best_contours(contours):

	min = MIN_AREA
	contour = None
	for cnt in contours:
		if cv2.contourArea(cnt) > min:
			min = cv2.contourArea(cnt)
			contour = cnt

	return contour

def main():
	# -images/
	# --------A/
	# --------B/
	# --------C/
	# --------N/
	# write data.csv
	with open('data.csv', mode='w', newline='\n') as data:
		data_writer = csv.DictWriter(data, ['image_path', 'width', 'height', 'area', 'class'])
		data_writer.writeheader()

		for dirpath, dnames, fnames in os.walk(IMG_PATH):
			for name in dnames:
				for sub_dirpath, sub_dnames, sub_fnames in os.walk(os.path.join(dirpath, name)):
					for sub_name in sub_fnames:
						# walk images
						img = cv2.imread(sub_dirpath + "/" + sub_name)
						contour = None
						img_edges, img_contours, contour = hsv(img)
						rect = cv2.minAreaRect(contour)
						box = cv2.boxPoints(rect)
						box = np.int0(box)

						height, width = 0,0
						dis_1 = np.sqrt(((box[0][0] - box[3][0]) ** 2) + ((box[0][1] - box[3][1]) ** 2))
						dis_2 = np.sqrt(((box[0][0] - box[1][0]) ** 2) + ((box[0][1] - box[1][1]) ** 2))
						# print(m1, m2)
						if dis_1 > dis_2:
							width = dis_1
							height = dis_2
						else:
							width = dis_2
							height = dis_1

						print("widht: " + str(width) + " ,height: " + str(height))
						print(os.path.join(sub_dirpath, sub_name))
						# show image
						if SHOW_IMG:
							cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
							cv2.imshow("img", img)
							cv2.imshow("edges", img_edges)
							cv2.imshow("contours", img_contours)
							cv2.waitKey(0)

						#TODO เหลือคำนวณหา ความกว้าง ความสูง (x1, y1, x2, y2) อยู่ในตัวแปล box
						data_writer.writerow(
							{
								'image_path': os.path.join(sub_dirpath, sub_name),
								'width': width,
								'height': height,
								'area': cv2.contourArea(contour),
								'class': name
							}
						)


if __name__ == '__main__':
	main()