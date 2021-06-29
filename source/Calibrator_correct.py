# 1) The Header ******************************************

import io
import math
from fractions import Fraction as fr

import numpy as np
from PIL import Image

try:
    from picamera import PiCamera
    import RPi.GPIO as gpio
except ImportError as error:
    print('Picamera module not found Use -usb to run application with USB_Camera')


class PiCameraCalibrator:
    FULLSCREEN = False
    WINDOW = (1000, 0, 780, 640)
    WIDTH = 1024
    HEIGHT = 768

    def __init__(self,
                 my_camera=False,
                 gain_r=1.0,
                 gain_b=1.0):
        if not my_camera:
            print('No Camera Detected!')
        else:
            self.camera = my_camera
            self.br1 = self.camera.brightness
            self.contrast = self.camera.contrast
            self.camera.awb_gains = (gain_r, gain_b)
            self.capture_image()
            self._start_processing()

    def capture_image(self):
        stream = io.BytesIO()  # create stream to the memory
        self.camera.capture(stream, format='bmp')  # capture from stream
        stream.seek(2)  # rewind the stream
        self.image = Image.open(stream)

    def _start_processing(self):
        self.red, self.green, self.blue = self.image.split()
        self.yr = np.array(self.red)  # convert channels to  arrays
        self.yb = np.array(self.blue)
        self.yg = np.array(self.green)

    def gray_world(self):
        mrgw = self.yr.sum()  # sum of the channel intensity values
        mggw = self.yg.sum()
        mbgw = self.yb.sum()
        self.gair_gw = (mggw) / (mrgw)  # ratio of sums
        self.gaib_gw = (mggw) / (mbgw)
        self._finish_processing()
        return self.gair_gw, self.gaib_gw

    def retinex(self):
        mr = self.yr.max()  # findig maximal intensities in channels
        mg = self.yg.max()
        mb = self.yb.max()
        self.gair_ret = (mg) / (mr)  # find gains from maxima ratios
        self.gaib_ret = (mg) / (mb)
        self._finish_processing()
        return float(self.gair_ret), float(self.gaib_ret)

    def std(self):
        pimg = self.image.convert(mode='RGB')
        nimg = np.array(pimg)
        subwidth = 480
        subheight = 360
        nimg = nimg.astype(np.uint32)
        height, width, ch = nimg.shape
        strides = nimg.itemsize * np.array([width * subheight, subwidth, width, 3, 1])
        shape = (height // subheight, width // subwidth, subheight, subwidth, 3)
        blocks = np.lib.stride_tricks.as_strided(nimg, shape=shape, strides=strides)
        y, x = blocks.shape[:2]
        std_r = np.zeros([y, x], dtype=np.float16)
        std_g = np.zeros([y, x], dtype=np.float16)
        std_b = np.zeros([y, x], dtype=np.float16)
        std_r_sum = 0.0
        std_g_sum = 0.0
        std_b_sum = 0.0
        for i in range(y):
            for j in range(x):
                subblock = blocks[i, j]
                subb = subblock.transpose(2, 0, 1)
                std_r[i, j] = np.std(subb[0])
                std_g[i, j] = np.std(subb[1])
                std_b[i, j] = np.std(subb[2])
                std_r_sum += std_r[i, j]
                std_g_sum += std_g[i, j]
                std_b_sum += std_b[i, j]
        sdwa_r = 0.0
        sdwa_g = 0.0
        sdwa_b = 0.0

        for i in range(y):
            for j in range(x):
                subblock = blocks[i, j]
                subb = subblock.transpose(2, 0, 1)
                mean_r = np.mean(subb[0])
                mean_g = np.mean(subb[1])
                mean_b = np.mean(subb[2])
                sdwa_r += (std_r[i, j] / std_r_sum) * mean_r
                sdwa_g += (std_g[i, j] / std_g_sum) * mean_g
                sdwa_b += (std_b[i, j] / std_b_sum) * mean_b
        sdwa_avg = (sdwa_r + sdwa_g + sdwa_b) / 3.0
        gainr_std = sdwa_avg / sdwa_r
        gaing_std = sdwa_avg / sdwa_g
        gainb_std = sdwa_avg / sdwa_b
        self._finish_processing()
        return float(gainr_std), float(gainb_std)

    def white_patches(self):
        r_2 = self.yr ** 2
        g_2 = self.yg ** 2
        b_2 = self.yb ** 2
        w = PiCameraCalibrator.WIDTH
        h = PiCameraCalibrator.HEIGHT
        sycc_2 = r_2 + g_2 + b_2
        sycc = self.yr + self.yg + self.yb
        Y = self.__get_user_respond()
        if Y.any():
            maxY = np.max(Y)
            corrR = (maxY * w * h) / self.yr.sum()
            corrB = (maxY * w * h) / self.yb.sum()
            self._finish_processing
            return float(corrR), float(corrB)

    def __get_user_respond(self):
        # print('Y = yr*0.3+yg*0.59+yb*0.11: enter "1" ')
        # print('Y = yr*0.21 + yg*0.71 +yb*0.08: enter "2" ')
        # print('Y = yr*0.26 + yg*0.68 +yb*0.06: enter "3" ')
        # Yrec = input("Make a choise [1, 2, 3] ")
        # if Yrec in '123':
        #    if int(Yrec) == 1:
        #         #Method for Human eyes
        #    if int(Yrec) == 2:
        #        Y = self.yr*0.21 + self.yg*0.71 + self.yb*0.08
        #    if int(Yrec) == 3:
        #        Y = self.yr*0.26 + self.yg*0.68 + self.yb*0.06
        Y = self.yr * 0.3 + self.yg * 0.59 + self.yb * 0.11
        self._finish_processing()
        return Y if Y.any() else 0

    def _finish_processing(self):
        # mx = 255 * 0.9270 #4layers
        mx = 255 * 0.7922  # 2layers
        mg = self.yg.max()
        self.ys = self.yg.std()
        self.br2 = mx / (mg - self.ys) * self.br1
        if not 0 <= self.br2 <= 100:
            self.br2 = self.br1

        k = self.br2 / self.br1  # ratio between old and new contrast
        ymin = self.yg.min() * k  # black level
        ymax = self.yg.max() * k  # white level
        ymean = self.yg.mean() * k  # average level
        mn = 52
        cr = mn + (ymean - ymin) * (mx - mn) / (ymax - ymin)  # estimated contrast ratio
        self.cc = 10 * math.log10(cr)  # contrast in decibels
        self.camera.brightness = fr(self.br2)  # set estimated brightenss
        self.camera.contrast = round(self.cc)


if __name__ == '__main__':
    camera = PiCamera()
    calibrator = PiCameraCalibrator(my_camera=camera)
    gains = calibrator.gray_world()
