import cv2
import numpy as np
from ollama import chat
import base64

# mp4 is made of frames that are really just jpg or png encoded binary.
# mp4



class RECT:
  def __init__(self, right, top, width, height):
    self.right = right
    self.top = top  
    self.width = width
    self.height = height



def crop_frame(np_array, dimensions):
  pass



def getRawDim(input_str):
  #input_str is from stdio, need to parse it, detect whitespace = next parameter. When parsing a parameter, ignore all initial and trailing whitespace. 
  # If not a number, return 0 intialized RECT obj
  pass








def extract_frames(filepath):

  cap = cv2.VideoCapture(filepath)



  dimensions = RECT(0,0,0,0)

  print(dimensions)
  print("Would you like to create an area of focus using raw pixels or with video proportions?")
  print("1. Raw pixels\n2. Video proportions\n", end = 'Choice: ')
  choice = float('inf')
  while choice:
    try:
      choice_chosen = int(input(""))
      # for some reason choice > 2 or choice < 1 does not work with 0
      if choice_chosen > 2 or choice_chosen < 1:
        print("Key in a proper value\nChoice: ", end = "")
        continue
      choice = choice_chosen
      if choice < float('inf'):
        break
    except ValueError as e1:
      print("Key in a proper value\nChoice: ", end = "")

  if choice == 1:
    while choice == 1:
      try:
        print("Key in pixel dimensions in the following format: rightmost_pixel, topmost_pixel, width, height")
        r = str(input("Dimensions:"))
        ok, raw_dim = getRawDim(r)
        if not ok:
          print("Key in valid values")
          continue
      except ValueError:
        print("Key in valid values")

      
  if choice == 2:
    pass



  while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
      break
    # frame here is the decoded np pixel array.
    # Take it and crop it.

    crop_frame(frame, dimensions)



  return 



def main():

  try:

    filepath = str(input("Type in file path: "))


    extract_frames(filepath)

  except ValueError as e:

    raise ValueError(e) # already returns 1

  return 0


if __name__ == "__main__":
  main()


