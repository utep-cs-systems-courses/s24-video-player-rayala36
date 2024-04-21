#! /usr/bin/env python3

import threading
import cv2
import os
import numpy as np
import base64

class ProducerConsumerQueue:
    def __init__(self):
        self.storage = []
        self.Lock = threading.Lock()
        self.queueLength = 30
        self.vacantCells = threading.Semaphore(self.queueLength)
        self.occupiedCells = threading.Semaphore(0)

    # Adds a frame to a queue only if the frame is not full
    # Locks are acquired and released, and frames are added to
    # the queue; ensures no race conditions between threads.
    def add(self, frame):
        self.vacantCells.acquire()
        self.Lock.acquire()
        self.storage.append(frame)
        self.Lock.release()
        self.occupiedCells.release()

    # Deletes a frame from a queue and returns that frame;
    # my own version of pop.  Locks are acquired and released,
    # and frames are deleted from the queue in between; ensures
    # no race conditions between threads.
    def delete(self):
        self.occupiedCells.acquire()
        self.Lock.acquire()
        frame = self.storage.pop(0)
        self.Lock.release()
        self.vacantCells.release()
        return frame
