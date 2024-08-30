import cv2
import sys

r = cv2.imread('R.jfif')
# r = cv.imread('pingu.jpg')

if r is None:
    print('Image not found')
    sys.exit(1)
    
cv2.imshow('pingu', r)
cv2.waitKey(0)
cv2.destroyAllWindows()