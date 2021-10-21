import sys
import cv2 as cv
import numpy as np
import easygui

# Custom Utilities module
import Utilities as utl

# dynamically ask for the image to open
# this is so the program works well on every OS
imgpath = utl.load_image()

# if image is grayscale continue, otherwise exit
# Cr, Cb values are gonna be used when we have a YCrCb image
# otherwise the value is 0
image, color, Cr, Cb = utl.read_img(imgpath)

# log the image
log_image = utl.log_transform(image)

# here we initialize the gui
utl.gui(log_image)

while(True):
    ghigh = cv.getTrackbarPos('ghigh (/10)', 'Homomorphic Filter') / 10
    glow  = cv.getTrackbarPos('glow (/10)', 'Homomorphic Filter')  / 10
    cc    = cv.getTrackbarPos('cc (/10)', 'Homomorphic Filter')    / 10
    d0    = cv.getTrackbarPos('d0', 'Homomorphic Filter')
    #this check is to avoid division by zero
    if d0 == 0:
        d0 = 1

    # fft image
    fft_image = np.fft.fft2(log_image)

    # shift fft frequency
    shift_image = np.fft.fftshift(fft_image)

    # create filter
    gauss, lp = utl.gaussian_hp(ghigh, glow, cc, d0, shift_image)

    ## apply filter on image
    # using numpy's `multiply` we perform element-wise multiplication as the `.*` operator does in matlab
    # so for example:
    #
    # a = np.array([[1,2],
    #               [3,4]])
    #
    # b = np.array([[5,6],
    #               [7,8]])
    #
    # np.multiply(a,b)
    #
    # Produces the following:
    #
    # array([[ 5, 12],
    #       [21, 32]])
    filtered_image = np.multiply(shift_image,gauss)

    # reverse the frequency back to the corner
    reverse_shift_image = np.fft.ifftshift(filtered_image)

    # invert fourier
    inverse_fft_image = np.real(np.fft.ifft2(reverse_shift_image, axes=(0,1)))

    # exp image
    exp_image = utl.exp(inverse_fft_image)

    # normalize image back
    img_homomorphic = utl.normalize(exp_image, color, Cr, Cb)

    cv.imshow("Homomorphic Filter", img_homomorphic)
    k = cv.waitKey(1)
    if k == 27:
        save_path = easygui.filesavebox()
        cv.imwrite(save_path, img_homomorphic)
        cv.destroyAllWindows()
        break
