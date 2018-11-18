import cv2
import numpy as np
import os
import csv

IMG_PATH = "images"
LOWER_PURPLE = [0, 0, 0]
UPPER_PURPLE = [255, 255, 255]

def hsv(image):

	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, np.array(LOWER_PURPLE), np.array(UPPER_PURPLE))
	res = cv2.bitwise_and(image, image, mask=mask)
	blur = cv2.GaussianBlur(res, (7, 7), 0)
	kernel = np.ones((5, 5), np.uint8)
	dilation = cv2.dilate(blur, kernel, iterations=1)
	edges = cv2.Canny(dilation, 100, 200)
	edges, contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
	img_contours = cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

	return hsv, edges, img_contours, contours

def main():
	# -images/
	# --------A/
	# --------B/
	# --------C/
	# --------N/
	for dirpath, dnames, fnames in os.walk(IMG_PATH):
		for name in dnames:
			print(name)
			for sub_dirpath, sub_dnames, sub_fnames in os.walk(os.path.join(dirpath, name)):
				for sub_name in sub_fnames:
					img = cv2.imread(sub_dirpath + "/" + sub_name)
					img_hsv, img_edges, img_contours, contours = hsv(img)
					for cnt in contours:
						print(cv2.contourArea(cnt))
						rect = cv2.minAreaRect(cnt)
						box = cv2.boxPoints(rect)
						box = np.int0(box)
						cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
						cv2.imshow("img", cv2.resize(img, (800, 600)))
						cv2.waitKey(0)
					cv2.imshow("hsv", cv2.resize(img_hsv, (800, 600)))
					cv2.imshow("edges", cv2.resize(img_edges, (800, 600)))
					cv2.imshow("contours", cv2.resize(img_contours, (800, 600)))
					cv2.waitKey(0)
					# print(os.path.join(sub_dirpath, sub_name))
					# with open('employee_file.csv', mode='w') as employee_file:
					# 	employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"',
					# 								 quoting=csv.QUOTE_MINIMAL)
					#
					# 	employee_writer.writerow(['John Smith', 'Accounting', 'November'])
					# 	employee_writer.writerow(['Erica Meyers', 'IT', 'March'])


if __name__ == '__main__':
	main()