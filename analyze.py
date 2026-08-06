
import cv2
import sys
import numpy as np



def main():

  file = ''

  print("\n\nML auto vid clipper v1\n")
  try:
    file = str(input("Input file name with file extension (input.mp4): "))
    print("File received, editing\n")

    findAoi(file)


  except ValueError as e:
    print(f"{e}")
    print("Ditching process\n")
    return 1

  return 0



def findAoi(f:str):

  cap = cv2.VideoCapture(f)

  fps = cap.get(cv2.CAP_PROP_FPS)
  n_frames =cap.get(cv2.CAP_PROP_FRAME_COUNT)
  w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
  h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

  print(f"File information:\nFile: {f}\nFPS: {fps}\nFrame count: {n_frames}\nVideo Resolution: {w} x {h}\n")



  while cap.isOpened():
    isOk, frame = cap.read()
    if not isOk:
      break
    cv2.imshow('Frame', frame)

    t_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
    t_s = round(t_ms/1000, 3)

  cap.release()
  


  # KDA is on the 7/8th portion of the screen and top 1/8th of the screen. If we were to partition the screen into 8x8 pieces (for v1), it would be at position vid_portions[0][6].



  return











if __name__ == "__main__":
  main()

