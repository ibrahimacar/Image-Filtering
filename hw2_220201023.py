### import necessary packages### find new filtered pixel for diameter*diameter window
import numpy as np
import cv2
import sys
import math

### find new filtered pixel for diameter*diameter window
def bileteralFilteredPixel(img, x, y, diameter, sigma_i, sigma_s):
    hl = diameter//2
    filteredIndex = 0
    Wp = 0
    i = 0
    while i < diameter:
        j = 0
        while j < diameter:
            xNeighbour = x - (hl - i)
            yNeighbour = y - (hl - j)
            if xNeighbour >= len(img):
                xNeighbour -= len(img)
            if yNeighbour >= len(img[0]):
                yNeighbour -= len(img[0])
            gi = gaussian(img[xNeighbour][yNeighbour] - img[x][y], sigma_i)
            gs = gaussian(distance(xNeighbour, yNeighbour, x, y), sigma_s)
            w = gi * gs
            filteredIndex += img[xNeighbour][yNeighbour] * w
            Wp += w
            j += 1
        i += 1
    filteredIndex =int(round(filteredIndex / Wp))
    return filteredIndex

### visit all the pixels and create filtered image
def visitAndApply(img,diameter,sigma_i, sigma_s):
    i=0
    new_img=np.zeros(img.shape)
    while(i<len(img)):
        j=0
        while(j<len(img[1])):
            new_img[i][j]=bileteralFilteredPixel(img,i,j,diameter,sigma_i,sigma_s)

            j=j+1
        i=i+1
    return new_img

###Distance Function
def distance(x1,y1,x2,y2):
    return math.sqrt( ( (x1-x2) * (x1-x2) ) + ( (y1-y2) * (y1-y2) ) )

###Gaussian distrubuter
def gaussian(x, sigma):
    return (1.0 / (2 * math.pi * (sigma ** 2))) * math.exp(- (x ** 2) / (2 * sigma ** 2))

windowSize=7
image=cv2.imread("in_img.jpg",0)

myFilteredImage=visitAndApply(image,windowSize,10,10)
cv2.imwrite("filtered image own.png", myFilteredImage)

OpencvFilteredImage=cv2.bilateralFilter(image,windowSize, 10,10)
cv2.imwrite("filtered image OpenCV.png",OpencvFilteredImage)



### I First choosed Intensity sigma as a constant 2 and choosed spatial sigma as 10,20 to see affects of the spatial sigma.
###I couldn't see much difference then I choose spatial sigma very large numbers and there wasn't much affect still.For spatial sigma,
### it dose not have much affect on image because we choose a neighborhood size and for an constant neighborhood size spatial distances stays constant.
### Our neighborhood size proportional to spatial sigma. Then I choosed Spatial sigma as constant and choosed intensity sigma as 10,20.
###For the intensity sigma, as we increase the intensity sigma, farther index's intensity values's effect starts to increase which means image starts to smooth while preserving edges.
###However for much larger values of intensity sigma,it starts to smooth edges,too. Finally I started to choose sigmas differently (10,10),(15,10),(10,15)
###I saw that images dosen't change as sigma spatial changes.
