import cv2 as cv
import numpy as np
from PIL import Image

# check if the image is grayscale
def is_grey_scale(img_path):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i,j))
            if r != g != b:
                return False
    return True

def read_img(imgpath):
    Cr = 0
    Cb = 0
    if(is_grey_scale(imgpath)):
        image = cv.imread(imgpath, 0)
        image = cv.normalize(image, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
        color = "gray"
    else:
        image = cv.imread(imgpath)
        image = cv.cvtColor(image, cv.COLOR_BGR2YCrCb)
        channels = cv.split(image)
        image = cv.normalize(channels[0], None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
        Cr = channels[1]
        Cb = channels[2]
        color = "rgb"
    return image , color, Cr, Cb

# p.176 Gonzalez
# https://pythontic.com/image-processing/pillow/logarithmic%20transformation
def log_transform(image):
    log_image = np.log1p(image)
    return log_image

def gui(image):
    cv.namedWindow('Homomorphic Filter', cv.WINDOW_NORMAL)
    start_ghigh = 30  # slider start position
    max_ghigh = 200  # maximal slider position
    start_glow = 4  # slider start position
    max_glow = 100  # maximal slider position
    start_c = 50  # slider start position
    max_c = 500  # maximal slider position
    start_d0 = 20  # slider start
    max_d0 = 200  # maximal slider position
    cv.createTrackbar('ghigh (/10)', 'Homomorphic Filter', start_ghigh, max_ghigh, (lambda a: None))
    cv.createTrackbar('glow (/10)', 'Homomorphic Filter', start_glow, max_glow, (lambda a: None))
    cv.createTrackbar('cc (/10)', 'Homomorphic Filter', start_c, max_c, (lambda a: None))
    cv.createTrackbar('d0', 'Homomorphic Filter', start_d0, max_d0, (lambda a: None))

# the filer we are using is a custom GHPF, DoG taken from here
#
# Homomorphic filtering based illumination normalization method
# for face recognition
# Chun-Nian Fan a,b
#, Fu-Yan Zhang a
def gaussian_lp(img, c, D0):
        P,Q = img.shape
        centerX = P/2
        centerY = Q/2
        H = np.zeros(img.shape)
        U, V = np.meshgrid(range(int(P)), range(int(Q)), sparse=False, indexing='ij')
        Duv = (((U-centerX)**2+(V-centerY)**2)).astype(float)
        H = np.exp((-c*Duv/(D0**2)))
        return H

def gaussian_hp(gammah,gammal,c,D0,img):
    lp = gaussian_lp(img, c, D0)
    base = (gammah - gammal)*(1-lp) + gammal
    return base, lp

def exp(image):
    exp_image = np.expm1(image)
    return exp_image

def normalize(exp_image, color, Cr, Cb):
    if (color == "gray"):
        return cv.normalize(exp_image, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
    else:
        image = cv.normalize(exp_image, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
        image = cv.merge((image, Cr, Cb))
        return cv.cvtColor(image, cv.COLOR_YCrCb2BGR)

