
# def connect_cam():
#     global cap
#     cap.release()
#     cap = cv2.VideoCapture(CAMERA)


# if __name__ == "__main__":
#     while True:
#         ret, frame = cap.read()
#         cv2.imshow("window", frame)
#         if cv2.waitKey(1) == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()