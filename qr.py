import cv2
import numpy as np
from pyzbar.pyzbar import decode
import json

img = cv2.imread("images/qrcode.png", cv2.IMREAD_COLOR)
img = cv2.resize(img, (400, 400))
# cv2.imshow("image", img)
for barcode in decode(img):
    x, y, w, h = barcode.rect
    myData = barcode.data.decode('utf-8')
    jData = json.loads(myData)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)
    cv2.circle(img, (int(x+w/2), int(y+h/2)), 2, (255, 0, 0), 2)
    print(f"{jData['name']}  {jData['height']}")
    print(f"{x} {y} {w} {h}")

    # pts = np.array([barcode.polygon],np.int32)
#         pts = pts.reshape((-1,1,2))
#         cv2.polylines(img,[pts],True,(255,0,255),5)
#         pts2 = barcode.rect
#         cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
#                     0.9,(255,0,255),2)

# cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.imshow('Result', img)

cv2.waitKey(0)

# It is for removing/deleting created GUI window from screen
# and memory
# cv2.destroyAllWindows()
