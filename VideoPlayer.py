#! /usr/bin/env python3

import cv2
import numpy as np
import threading
import base64
from ProducerConsumerQueue import ProducerConsumerQueue

def extractFrames(fName, queue, maxFrames = 9999):

    # Frame counter
    frameCount = 0
    # Video file
    videoCapture = cv2.VideoCapture(fName)

    # First image read
    read, image = videoCapture.read()

    print(f'Frame number {frameCount} {read}')
    while(read and frameCount < maxFrames):

        # Each frame is obtained as a jpeg
        read, singleImage = cv2.imencode('.jpg', image)

        encodedImage = base64.b64encode(singleImage)

        # Jpeg frame is added to the ProducerConsumerQueue
        queue.add(image)

        read, image = videoCapture.read()
        print(f'Reading frame {frameCount} {read}')
        frameCount += 1
    # None signals that all frames have been read, and to stop inserting to queue.
    queue.add(None)
    os.write(1, "All frames have been extracted".encode())

def grayFrames(coloredFrameQueue, bwFrameQueue):
    # Takes in a queue with colored frames and converts them to mono
    # readFromQueue has all the colored frames
    frameCount = 0
    # First queue element is obtained as a means to access the whole queue
    normalFrame = coloredFrameQueue.delete()

    while(normalFrame is not None):
        monoFrame = cv2.cvtColor(normalFrame, cv2.COLOR_BGR2GRAY)

        print("Currently Decoloring frame "+str(frameCount))
        bwFrameQueue.add(monoFrame)

        frameCount += 1

        #Queue with colored frames will be emptied
        normalFrame = coloredFrameQueue.delete()
    # None signals that all frames have been decolored, and to stop inserting into the queue.
    print("All frames are decolored :(")
    bwFrameQueue.add(None)

def display(frameQueue):

    # Takes in a queue with frames, which should be grey jpegs, and display them all in sequence in a window
    frameCount = 0
    # Delete is essentially my version of pop
    singleFrame = frameQueue.delete()

    while(singleFrame is not None):

        print("Currently showing frame \n"+str(singleFrame))
        # Video window will simply be called "Video"
        cv2.imshow("Video", singleFrame)

        # Between every frame access there will be a 42 ms delay
        if(cv2.waitKey(42) and 0xFF == ord("q")):
            break

        frameCount += 1
        singleFrame = frameQueue.delete()

    print("Video Finished")
    cv2.destroyAllWindows()

video = 'clip.mp4'

# Producer for grey video
pQForGreyVid = ProducerConsumerQueue()
# Consumer for grey video
cQForGreyVid = ProducerConsumerQueue()

producerThreadForVid = threading.Thread(target = extractFrames, args = [video, pQForGreyVid, 1000])
grayFrameThreadForVid = threading.Thread(target = grayFrames, args = [pQForGreyVid, cQForGreyVid])
consumerThreadForVid = threading.Thread(target = display, args = [cQForGreyVid])

producerThreadForVid.start()
grayFrameThreadForVid.start()
consumerThreadForVid.start()
