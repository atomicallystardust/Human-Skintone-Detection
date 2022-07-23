import numpy as np
import cv2
import os
import sklearn
from sklearn.cluster import KMeans
from collections import Counter
import imutils
from matplotlib import pyplot as plt


rgb_lower = [38,21,1]
rgb_higher = [252,238,221]

skin_shades = {
    'dark' : [rgb_lower,[150,87,12]],
    'mild' : [[150,87,12],[180,105,15]],
    'fair':[[180,105,15],rgb_higher],

}

convert_skintones = {}
for shade in skin_shades:
    convert_skintones.update({
        shade : [
            (skin_shades[shade][0][0] * 256 * 256) + (skin_shades[shade][0][1] * 256) + skin_shades[shade][0][2],
            (skin_shades[shade][1][0] * 256 * 256) + (skin_shades[shade][1][1] * 256) + skin_shades[shade][1][2]
        ]
    })

def extractSkin(image):
    img = image.copy()
    black_img = np.zeros((img.shape[0],img.shape[1],img.shape[2]),dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_threshold = np.array([0, 48, 80], dtype=np.uint8)
    print(lower_threshold)
    upper_threshold = np.array([20, 255, 255], dtype=np.uint8)
    print(upper_threshold)

    skinMask = cv2.inRange(img, lower_threshold, upper_threshold)
    skin = cv2.bitwise_and(img, img, mask=skinMask)
    return cv2.cvtColor(skin, cv2.COLOR_HSV2BGR)

def removeBlack(estimator_labels, estimator_cluster):
    hasBlack = False
    occurance_counter = Counter(estimator_labels)
    def compare(x, y): return Counter(x) == Counter(y)
    for x in occurance_counter.most_common(len(estimator_cluster)):
        color = [int(i) for i in estimator_cluster[x[0]].tolist()]
        if compare(color, [0, 0, 0]) == True:
            del occurance_counter[x[0]]
            hasBlack = True
            estimator_cluster = np.delete(estimator_cluster, x[0], 0)
            break
    return (occurance_counter, estimator_cluster, hasBlack)

def getColorInformation(estimator_labels, estimator_cluster, hasThresholding=False):
    occurance_counter = None
    colorInformation = []
    hasBlack = False
    if hasThresholding == True:
        (occurance, cluster, black) = removeBlack(
            estimator_labels, estimator_cluster)
        occurance_counter = occurance
        estimator_cluster = cluster
        hasBlack = black
    else:
        occurance_counter = Counter(estimator_labels)
    totalOccurance = sum(occurance_counter.values())
    for x in occurance_counter.most_common(len(estimator_cluster)):
        index = (int(x[0]))
        index = (index-1) if ((hasThresholding & hasBlack)
                              & (int(index) != 0)) else index
        color = estimator_cluster[index].tolist()
        color_percentage = (x[1]/totalOccurance)
        colorInfo = {"cluster_index": index, "color": color,
                     "color_percentage": color_percentage}
        colorInformation.append(colorInfo)
    return colorInformation

def extractDominantColor(image, number_of_colors=1, hasThresholding=False):
    if hasThresholding == True:
        number_of_colors += 1
    img = image.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0]*img.shape[1]), 3)
    estimator = KMeans(n_clusters=number_of_colors, random_state=0)
    estimator.fit(img)
    colorInformation = getColorInformation(
        estimator.labels_, estimator.cluster_centers_, hasThresholding)
    return colorInformation

def plotColorBar(colorInformation):
    color_bar = np.zeros((100, 500, 3), dtype="uint8")
    top_x = 0
    for x in colorInformation:
        bottom_x = top_x + (x["color_percentage"] * color_bar.shape[1])
        color = tuple(map(int, (x['color'])))
        cv2.rectangle(color_bar, (int(top_x), 0),
                      (int(bottom_x), color_bar.shape[0]), color, -1)
        top_x = bottom_x
    return color_bar


from verzeo.models import Photo
from django.core.files.base import ContentFile
import urllib
import requests
from urllib.parse import urlparse
from django.core.files import File
import urllib.request
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import cv2
import os
def predictfromdevice(request):
    print(request)
    print(request.POST.dict())
    fileobj=request.FILES['filepath']
    fs=FileSystemStorage()
    filepathName=fs.save(fileobj.name,fileobj)
    filepathName=fs.url(filepathName)
    url ="http://127.0.0.1:8000"+filepathName
    print(url)
    image = imutils.url_to_image(url)

    image = imutils.resize(image, width=250)
    

    skin = extractSkin(image)


    unprocessed_dominant = extractDominantColor(skin, number_of_colors=1, hasThresholding=True)

    decimal_lower = (rgb_lower[0] * 256 * 256) + (rgb_lower[1] * 256) + rgb_lower[2]
    decimal_higher = (rgb_higher[0] * 256 * 256) + (rgb_higher[1] * 256) + rgb_higher[2]
    dominantColors = []
    for clr in unprocessed_dominant:
        clr_decimal = int((clr['color'][0] * 256 * 256) + (clr['color'][1] * 256) + clr['color'][2])
        if clr_decimal in range(decimal_lower,decimal_higher+1):
            clr['decimal_color'] = clr_decimal
            dominantColors.append(clr)

    skin_tones = []
    if len(dominantColors) == 0:
        skin_tones.append('Unrecognized')
    else:
      for color in dominantColors:
        for shade in convert_skintones:
            if color['decimal_color'] in range(convert_skintones[shade][0],convert_skintones[shade][1]+1):
                skin_tones.append(shade)

    print(skin_tones)
   

    context={'filepathName':filepathName,'skin_tones':skin_tones}
    return render(request,'device.html',context)

    


def predictbyurl(request,):
    try:
        url = request.POST['myinput']

        image = imutils.url_to_image(url)

        image = imutils.resize(image, width=250)

        skin = extractSkin(image)
       

        unprocessed_dominant = extractDominantColor(skin, number_of_colors=1, hasThresholding=True)

        decimal_lower = (rgb_lower[0] * 256 * 256) + (rgb_lower[1] * 256) + rgb_lower[2]
        decimal_higher = (rgb_higher[0] * 256 * 256) + (rgb_higher[1] * 256) + rgb_higher[2]
        dominantColors = []
        for clr in unprocessed_dominant:
            clr_decimal = int((clr['color'][0] * 256 * 256) + (clr['color'][1] * 256) + clr['color'][2])
            if clr_decimal in range(decimal_lower,decimal_higher+1):
                 clr['decimal_color'] = clr_decimal
                 dominantColors.append(clr)

        skin_tones = []
        if len(dominantColors) == 0:
            skin_tones.append('Unrecognized')
        else:
          for color in dominantColors:
              for shade in convert_skintones:
                  if color['decimal_color'] in range(convert_skintones[shade][0],convert_skintones[shade][1]+1):
                     skin_tones.append(shade)

        print(skin_tones)
        print("Color Bar")
        

        context={'filepathName':url,'skin_tones':skin_tones}
        return render(request,'krke.html',context)
    except Exception as e:
        print(e)
        return render(request, "krke.html", {'skin_tones': 'This site not given permission to access it..try other one'})

# Create your views here.
def device(request):
    context={'a':1}
    return render(request,'device.html',context)

def byurl(request):
    context={'a':1}
    return render(request,'krke.html',context)

def home(request):
    context={'a':1}
    return render(request,'home.html',context)


def dono(request):
    context={'a':1}
    return render(request,'dono.html',context)
def about(request):
    context={'a':1}
    return render(request,'about.html',context)

