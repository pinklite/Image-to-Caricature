import cv2              # for image processing
import easygui          # to open the filebox
import numpy as np      # to store image
import imageio          # to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image

root = tk.Tk()
root.geometry('400x400')
root.title('Image to Caricature!')
root.configure(bg="#E0E0FF")
label = Label(root, bg="#E0E0FF", font=("arial", 16, "bold"))


def upload_image():
    image_path = easygui.fileopenbox()
    caricature(image_path)


def caricature(image_path):
    # reading original image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    # print(image)
    # image stored as numbers

    # confirming that the image is chosen
    if original_image is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    Re_Size1 = cv2.resize(original_image, (960, 540))
    # plt.imshow(Re_Size1, cmap='gray')

    # converting image to grayscale
    grayScImage = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    Re_Size2 = cv2.resize(grayScImage, (960, 540))
    # plt.imshow(Re_Size2, cmap='gray')

    # median blur for image smoothening
    smoothGraySc = cv2.medianBlur(grayScImage, 5)
    Re_Size3 = cv2.resize(smoothGraySc, (960, 540))
    # plt.imshow(Re_Size3, cmap='gray')

    # retrieving edges of image by using thresholding technique
    get_edges = cv2.adaptiveThreshold(smoothGraySc, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    Re_Size4 = cv2.resize(get_edges, (960, 540))
    # plt.imshow(Re_Size4, cmap='gray')

    # bilateral filter for removing noise and keeping sharp edges
    colored_image = cv2.bilateralFilter(original_image, 9, 300, 300)
    Re_Size5 = cv2.resize(colored_image, (960, 540))
    # plt.imshow(Re_Size5, cmap='gray')

    # masking edged image with "BEAUTIFY" image
    cartoon = cv2.bitwise_and(colored_image, colored_image, mask=get_edges)

    Re_Size6 = cv2.resize(cartoon, (960, 540))
    # plt.imshow(Re_Size6, cmap='gray')

    # Plotting the whole transition
    Allimages = [Re_Size1, Re_Size2, Re_Size3, Re_Size4, Re_Size5, Re_Size6]

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(Allimages[i], cmap='gray')

    sv = Button(root, text="Save cartoon image", command=lambda: save_image(Re_Size6, image_path), padx=30, pady=5)
    sv.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    sv.pack(side=TOP, pady=50)

    plt.show()


def save_image(Re_Size6, image_path):
    # saving an image using imwrite()
    new_Name = "cartoonified_Image"
    img_path = os.path.dirname(image_path)
    extnsn = os.path.splitext(image_path)[1]
    pth = os.path.join(img_path, new_Name + extnsn)
    cv2.imwrite(pth, cv2.cvtColor(Re_Size6, cv2.COLOR_RGB2BGR))
    Img_message = "Image saved by name " + new_Name + " at " + pth
    tk.messagebox.showinfo(title=None, message=Img_message)


upld = Button(root, text="Convert Image to Caricature", command=upload_image, padx=10, pady=5)
upld.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
upld.pack(side=TOP, pady=50)

root.mainloop()
