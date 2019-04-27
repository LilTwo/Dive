import cv2
import numpy as np
import matplotlib.pyplot as plt

class Image:
    def __init__(self, img_dir):
        self.img = cv2.imread(img_dir).astype(np.float)
        self.origin = self.img.copy()
        self.raw = self.img.copy()
        self.b, self.g, self.r = self.img[:, :, 0], self.img[:, :, 1], self.img[:, :, 2]
        self.shape = self.img.shape

    def scale(self,min,max,color):
        slope = 255/(max-min)
        b = -slope*min
        self.img[:,:,color] = np.array([slope*p+b for p in self.raw[:,:,color]])

    def auto_adjust(self, mean=None):
        meanR, meanG, meanB = self.r.mean(), self.g.mean(), self.b.mean()
        if not mean:
            mean = np.mean([meanR, meanG, meanB])
        self.b *= mean / meanB
        self.g *= mean / meanG
        self.r *= mean / meanR

    def adjust_temp(self, diff):
        self.img[:,:,2] = self.raw[:,:,2] + diff
        self.img[:,:,0] = self.raw[:,:,0] + diff

    def adjust_tint(self, diff):
        self.img[:,:,1] = self.raw[:,:,1] + diff

    def to_uint8(self,reverse=True):
        bgr = np.clip(self.img, 0, 255).astype(np.uint8)
        return cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB) if reverse else bgr

    def adjust_contrast(self):
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        img = self.to_uint8(False)
        for i in range(3):
            img[:,:,i] = clahe.apply(img[:,:,i])
        self.img = img.astype(np.float)
        self.raw = self.img.copy()

    def reset(self):
        self.raw = self.origin.copy()
        self.img = self.origin.copy()

    def hist(self):
        img = self.to_uint8()
        bins = 255
        histr = cv2.calcHist([img],[2],None,[bins],[0,256]).flatten()
        print(histr[0])
        histg = cv2.calcHist([img],[1],None,[bins],[0,256]).flatten()
        histb = cv2.calcHist([img],[0],None,[bins],[0,256]).flatten()
        x = [i for i in range(bins)]
        plt.bar(x,histr,color='r')
        plt.bar(x,histg,color='g')
        plt.bar(x,histb,color='b')