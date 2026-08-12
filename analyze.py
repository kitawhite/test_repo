
import cv2
import sys
import numpy as np
import base64

from ollama import chat


# grab is cheap
# 

def crop(frame, box):
    h, w = frame.shape[:2]
    x0, y0, x1, y1 = box
    return frame[int(y0*h):int(y1*h), int(x0*w):int(x1*w)]

def signature(frame, box):
    _crop = crop(frame, box)

    # tbr
    print(VLM(_crop))
    
    grey = cv2.cvtColor(_crop, cv2.COLOR_BGR2GRAY)   # color doesn't matter for digits
    return cv2.resize(grey, (16, 16))               # shrink hard -> kills noise, keeps shape

def changed(a, b, tol=12):
    return cv2.absdiff(a, b).mean() > tol           # mean pixel difference, 0..255



# sample_ms is the period between jumps.
# debounce_ms is the min period between two clips
def find_changes(path, box, sample_ms=120, debounce_ms=400):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise SystemExit(f"Could not open {path}")

    prev, marks, next_at, last_mark = None, [], 0.0, -1e9 
    while True:
        if not cap.grab():                  # cap.grab winds forward one frame.
            break
        t = cap.get(cv2.CAP_PROP_POS_MSEC) # Grab the timestamp of the frame in milisecs
        if t < next_at:                      # only look ~8x/sec, skip the rest without decoding. At start, t=0 and so will move to next line of code.
            continue
        next_at = t + sample_ms

        ok, frame = cap.retrieve()           # retrieve takes the decoded frame, decodes it, moves to the next frame.
        if not ok:
            break

        sig = signature(frame, box) #crop and grayscale the frame.

        #Take sig and pass into VLM
        if prev is not None and changed(sig, prev) and (t - last_mark) >= debounce_ms:
            marks.append(round(t / 1000, 3)) # seconds, ms precision -> ffmpeg-ready
            last_mark = t
            
        prev = sig

    cap.release() # What does .release even do?
    return marks


def VLM(decoded_frame_image):
    ok, encoded_png_in_memory = cv2.imencode('.png', decoded_frame_image)
    if not ok:
        raise RuntimeError("Cannot encode frame into PNG")

    # b64_img = base64.b64encode(encoded_png_in_memory)
    b64_img = base64.b64encode(encoded_png_in_memory.tobytes()).decode("utf-8")

    response = chat(
        model='qwen3.5',
        messages=[
            {
            'role': 'user',
            'content': 'What is in this image? Be concise.',
            'images': [b64_img],
            }
        ],
    )

    return response.message.content   



def main():
  
    file = ''

    kda_box = (0.33, 0.00, 1.00, 0.17)
    time_stamp = []

    print("\n\nML auto vid clipper v1\n")
    try:
        file = str(input("Input file name with file extension (input.mp4): "))
        print("File received, editing\n")

        # Find the time_stamps of the changes.
        timestamp = find_changes("videos./1out.mp4", kda_box)



        # Send images to VLM to find out what is the change in number
        VLM(timestamp)

    except ValueError as e:
        print(f"{e}")
        print("Ditching process\n")
        return 1

    return 0



if __name__ == "__main__":
    main()

