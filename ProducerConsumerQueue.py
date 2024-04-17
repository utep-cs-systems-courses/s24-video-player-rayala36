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

    def add(self, frame):
        self.vacantCells.acquire()
        self.Lock.acquire()
        self.storage.append(frame)
        self.Lock.release()
        self.occupiedCells.release()

    def delete(self):
        self.occupiedCells.acquire()
        self.Lock.acquire()
        frame = self.storage.pop(0)
        self.Lock.release()
        self.vacantCells.release()
        return frame
