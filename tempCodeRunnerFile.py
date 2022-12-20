pts = np.array([barcode.polygon],np.int32)
#         pts = pts.reshape((-1,1,2))
#         cv2.polylines(img,[pts],True,(255,0,255),5)
#         pts2 = barcode.rect
#         cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
#                     0.9,(255,0,255),2)

# cv2.imshow('Result',img)

# cv2.waitKey(0)