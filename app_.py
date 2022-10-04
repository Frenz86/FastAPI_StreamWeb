import threading
import queue
import time
import numpy as np
import cv2

def read_kbd_input(inputQueue):
    print('Ready for keyboard input:')
    while (True):
        input_str = input()
        inputQueue.put(input_str)

def main():
    inputQueue = queue.Queue()

    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    cap = cv2.VideoCapture(0)

    font                   = cv2.FONT_HERSHEY_DUPLEX
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    input_str = "test"

    while (True):
        check, frame = cap.read()

        if (inputQueue.qsize() > 0):
            input_str = inputQueue.get() 

            if (input_str == '280602017300'):
                print("do something")

        cv2.putText(frame, input_str, (10,30), font, fontScale, fontColor, lineType)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.01) 
    print("End.")

if (__name__ == '__main__'): 
    main()