#!/usr/bin/env python

# internal
import logging
import os
import glob

# external
import numpy as np
import cv2

"""
	recognition test
"""

def test_cascade_recognition(cascade_file_path, scaleFactor, minNeighbors):

    # load cascade
    cascade = cv2.CascadeClassifier(cascade_file_path)

    # initilize video capture
    cap = cv2.VideoCapture(0)

    # start capture loop
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        recognized = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x,y,w,h) in recognized:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow('img',img)

        #press escape to exit
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()