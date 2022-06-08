import cv2
from PyQt5.QtWidgets import QMainWindow
from matplotlib import pyplot as plt


class final_project_class(QMainWindow):
    def __init__(self):
        from PyQt5.uic import loadUi
        super(final_project_class, self).__init__()
        loadUi('final_project_app.ui', self)
        self.source_image = None
        self.btnOpenimage.clicked.connect(lambda: self.open_image())
        self.btnConnectWebcam.clicked.connect(lambda: self.connectwebcam())
        self.btnStopWebcam.clicked.connect(lambda: self.stopwebcam())
        self.btnRotate90.clicked.connect(lambda: self.set_rotate90())
        self.btnRotate180.clicked.connect(lambda: self.set_rotate180())
        self.btnRotate270.clicked.connect(lambda: self.set_rotate270())
        self.btnConvertToGray.clicked.connect(lambda: self.convert_image())
        self.btnCropimage.clicked.connect(lambda: self.crop_image())
        self.btnVer.clicked.connect(lambda: self.flip_vertical_image())
        self.btnFlipHor.clicked.connect(lambda: self.flip_horizontal_image())
        self.btnBMP.clicked.connect(lambda: self.save_bmp_image())
        self.btnJPG.clicked.connect(lambda: self.save_jpg_image())
        self.btnPNG.clicked.connect(lambda: self.save_png_image())
        self.btnEqulization.clicked.connect(lambda: self.equalization_image())
        self.btnScaling.clicked.connect(lambda: self.scaling())
        self.btnWarp.clicked.connect(lambda: self.warp())
        self.btnRotate.clicked.connect(lambda: self.rotate())
        self.btnBlur.clicked.connect(lambda: self.set_blur())
        self.btnsharpen.clicked.connect(lambda: self.sharpen_image())
        self.btnBlurring.clicked.connect(lambda: self.blur_image())
        self.btnMoreSmoothing.clicked.connect(lambda: self.smoothmore_image())
        self.btnSmoothing.clicked.connect(lambda: self.smooth_image())
        self.btnGray.clicked.connect(lambda: self.set_gray())
        self.btnShowhist.clicked.connect(lambda: self.show_histogram())
        self.btnGamma.clicked.connect(lambda: self.gamma_correction())

        self.stop_webcam = False
        self.blur_flag = False
        self.gray_flag = False
        self.rotate90_flag = False
        self.rotate180_flag = False
        self.rotate270_flag = False

    def open_image(self):
        from PyQt5 import QtWidgets, QtCore
        from skimage import io
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',QtCore.QDir.rootPath(),'*.*')
        try:
            self.source_image = io.imread(fileName)
            self.show_image(self.lblImage1, self.source_image)
        except Exception as e:
            print('Error: {}'.format(e))

    def show_image(self, label, image):
        import qimage2ndarray
        from PyQt5 import QtGui

        image = qimage2ndarray.array2qimage(image)
        qpixmap = QtGui.QPixmap.fromImage(image)
        label.setPixmap(qpixmap)

    def connectwebcam(self):
        import cv2
        self.stop_webcam = False
        self.blur_flag = False
        cap = cv2.VideoCapture(0)
        while True:
            ret, self.source_image = cap.read()
            self.source_image = cv2.cvtColor(self.source_image, cv2.COLOR_BGRA2RGB)
            self.show_image(self.lblImage1, self.source_image)
            if self.blur_flag:
                blur_image = cv2.blur(self.source_image, (9,9))
                self.show_image(self.lblImage2, blur_image)
            cv2.waitKey(1)
            if self.stop_webcam:
                break
            if self.gray_flag:
                gray_image = cv2.cvtColor(self.source_image, cv2.COLOR_BGR2GRAY)
                self.show_image(self.lblImage2, gray_image)
            if self.rotate90_flag:
                rotate90_image = cv2.rotate(self.source_image, cv2.ROTATE_90_CLOCKWISE)
                self.show_image(self.lblImage2, rotate90_image)
            if self.rotate180_flag:
                rotate180_image = cv2.rotate(self.source_image, cv2.ROTATE_180)
                self.show_image(self.lblImage2, rotate180_image)
            if self.rotate270_flag:
                rotate270_image = cv2.rotate(self.source_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self.show_image(self.lblImage2, rotate270_image)

        cap.release()
        cv2.destroyAllWindows()

    def stopwebcam(self):
        self.stop_webcam = True

    def set_blur(self):
        self.blur_flag = True

    def set_gray(self):
        self.gray_flag = True

    def set_rotate90(self):
        self.rotate90_flag = True

    def set_rotate180(self):
        self.rotate180_flag = True

    def set_rotate270(self):
        self.rotate270_flag = True

    def crop_image(self):
        from PIL import Image
        from skimage import io
        try:
            top = int(self.top.toPlainText())
            left = int(self.left.toPlainText())
            bottom = int(self.bottom.toPlainText())
            right = int(self.right.toPlainText())
            im = Image.fromarray(self.source_image, 'RGB')
            print(im.size)
            im_crop = im.crop((left, right, left+top, right+bottom))
            im_crop.save("crop_image.jpeg")
            crop_img = io.imread("crop_image.jpeg")
            self.show_image(self.lblImage2, crop_img)
        except Exception as e:
            print(f"Error:{e}")

    def flip_vertical_image(self):
        from PIL import Image
        from skimage import io
        import numpy as np
        try:
            im = Image.fromarray(self.source_image, 'RGB')
            Image.fromarray(np.fliplr(im)).save('flip_left_right.jpeg')
            img_flip_lr = io.imread('flip_left_right.jpeg')
            self.show_image(self.lblImage2, img_flip_lr)
        except Exception as e:
            print(f"Error:{e}")

    def flip_horizontal_image(self):
        from PIL import Image
        from skimage import io
        import numpy as np
        try:
            im = Image.fromarray(self.source_image, 'RGB')
            Image.fromarray(np.flipud(im)).save('flip_top_bottom.jpeg')
            img_flip_lr = io.imread('flip_top_bottom.jpeg')
            self.show_image(self.lblImage3, img_flip_lr)
        except Exception as e:
            print(f"Error:{e}")

    def save_bmp_image(self):
        from PIL import Image
        try:
            im = Image.fromarray(self.source_image,'RGB')
            im.save("convert_bmp.bmp", 'bmp')
        except Exception as e:
            print(f"Error:{e}")


    def save_jpg_image(self):
        from PIL import Image
        try:
            im = Image.fromarray(self.source_image,'RGB')
            im.save("convert_jpeg.jpeg", 'jpeg')
        except Exception as e:
            print(f"Error:{e}")

    def save_png_image(self):
        from PIL import Image
        try:
            im = Image.fromarray(self.source_image,'RGB')
            im.save("convert_png.png", 'png')
        except Exception as e:
            print(f"Error:{e}")

    def scaling(self):
        from PIL import Image
        from skimage import io
        try:
            im = Image.fromarray(self.source_image, 'RGB')
            im_size = im.resize((256, 256))
            im_size.save("resize.png")
            im_resize = io.imread('resize.png')
            self.show_image(self.lblImage3, im_resize)
        except Exception as e:
            print(f"Error:{e}")

    def warp(self):
        from PIL import Image
        from skimage import io
        import numpy as np
        import math
        try:
            im = Image.fromarray(self.source_image, 'RGB').convert("L")
            im = np.array(im)
            rows, cols = im.shape[0], im.shape[1]
            im_output = np.zeros((rows, cols))
            for i in range(rows):
                for j in range(cols):
                    offset_y = int(40.0 * math.sin(2 * 3.14 * j / 180))
                    if i + offset_y < rows:
                        im_output[i, j] = im[(i + offset_y) % rows, j]
                    else:
                        im_output[i, j] = 0
            im_warp = Image.fromarray(im_output)
            im_warp.save("warp.TIFF")
            im_warping = io.imread('warp.TIFF')
            self.show_image(self.lblImage2, im_warping)
        except Exception as e:
            print(f"Error:{e}")

    def blur_image(self):
        from skimage import filters, io
        try:
            sigma = int(self.txtBlur.toPlainText())
            io.imsave('blurImage.png', filters.gaussian(self.source_image, sigma=sigma, multichannel=True))
            image2 = io.imread('blurImage.png')
            self.show_image(self.lblImage2, image2)
        except Exception as e:
            print(f"Error: {e}")

    def sharpen_image(self):
        from PIL import Image
        from PIL import ImageFilter
        from skimage import io

        im = Image.fromarray(self.source_image,'RGB')
        sharpenImage = im.filter(ImageFilter.SHARPEN)
        sharpenImage.save('sharpen.png')
        sharpenImage = io.imread('sharpen.png')
        self.show_image(self.lblImage3, sharpenImage)

    def smoothmore_image(self):
        from PIL import Image
        from PIL import ImageFilter
        from skimage import io

        im = Image.fromarray(self.source_image,'RGB')
        smoothImage = im.filter(ImageFilter.SMOOTH_MORE)
        # smoothImage = im.filter(ImageFilter.SMOOTH)
        smoothImage.save('smooth.png')
        smoothImage = io.imread('smooth.png')
        self.show_image(self.lblImage3, smoothImage)

    def smooth_image(self):
        from PIL import Image
        from PIL import ImageFilter
        from skimage import io

        im = Image.fromarray(self.source_image,'RGB')
        # smoothImage = im.filter(ImageFilter.SMOOTH_MORE)
        smoothImage = im.filter(ImageFilter.SMOOTH)
        smoothImage.save('smooth.png')
        smoothImage = io.imread('smooth.png')
        self.show_image(self.lblImage2, smoothImage)

    def equalization_image(self):
        from PIL import Image
        from skimage import io, exposure
        from matplotlib import pyplot as plt

        # equlizationImage = exposure.equalize_hist(self.source_image)

        io.imsave('equlization.png', exposure.equalize_hist(self.source_image))
        equlizationImage = io.imread('equlization.png')
        self.show_image(self.lblImage2, equlizationImage)

        plt.figure(figsize=(5, 4))
        plt.hist(equlizationImage.ravel(), bins=256)
        plt.savefig('histEqulization.png')
        hist_img = io.imread('histEqulization.png')
        self.show_image(self.lblImage3, hist_img)

    def show_histogram(self):
        from matplotlib import pyplot as plt
        from skimage import io
        plt.figure(figsize=(5, 4))
        plt.hist(self.source_image.ravel(), bins=256)
        plt.savefig('hist.png')
        hist_img = io.imread('hist.png')
        self.show_image(self.lblImage2, hist_img)

    def convert_image(self):
        from matplotlib import pyplot as plt
        from skimage import io
        from PIL import Image

        im = Image.fromarray(self.source_image, 'RGB')
        imgGray = im.convert('L')
        imgGray.save('grayImg.png')
        imgGray = io.imread('grayImg.png')
        self.show_image(self.lblImage2, imgGray)

        plt.figure(figsize=(5, 4))
        plt.hist(imgGray.ravel(), bins=256)
        plt.savefig('histGray.png')
        hist_img = io.imread('histGray.png')
        self.show_image(self.lblImage3, hist_img)

    def gamma_correction(self):
        from PIL import Image
        from skimage import io
        try:
            im = Image.fromarray(self.source_image, 'RGB').convert("LA")
            row = im.size[0]
            col = im.size[1]
            gamma = float(self.gamma.toPlainText())
            result_img = Image.new("L", (row, col))
            for i in range(1, row):
                for j in range(1, col):
                    value = pow(im.getpixel((i, j))[0] / 255, (1 / gamma)) * 255
                    if value >= 255:
                        value = 255
                    result_img.putpixel((i, j), int(value))
            result_img.save("gamma.png")
            gamma_image = io.imread("gamma.png")
            self.show_image(self.lblImage3, gamma_image)
        except Exception as e:
            print(f"Error:{e}")

    def rotate(self):
        from PIL import Image
        from skimage import io
        try:
            im = Image.fromarray(self.source_image, 'RGB')
            alpha = int(self.alpha.toPlainText())
            im_rotated = im.rotate(alpha)
            im_rotated.save("rotated_image.jpg")
            im_rotate = io.imread("rotated_image.jpg")
            self.show_image(self.lblImage3, im_rotate)
        except Exception as e:
            print(f"Error:{e}")
def final_project_app():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = final_project_class()
    window.show()
    app.exec()

if __name__ == "__main__":
    final_project_app()