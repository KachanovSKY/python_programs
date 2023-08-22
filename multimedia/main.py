import math
import matplotlib.pyplot as plt
import numpy as np
import struct
from PIL import Image


tmp = 0

def saveInFileAndGetComponents(image, filename, position, startPos, width, height):
    step = 0
    storeImage = []
    for i in range(startPos, len(image)):
        if step != position:
            image[i] = 0
        else:
            storeImage.append(image[i])
        step = (step + 1) % 3
    imageFile = open(filename, 'wb')
    imageFile.write(bytes(image)) 
    imageFile.close()

    return storeImage

with open('/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/kodim20.bmp', 'rb') as f:
    header = f.read(54)
    pixel_offset = int.from_bytes(header[10:14], byteorder='little')
    width = int.from_bytes(header[18:22], byteorder='little')
    height = int.from_bytes(header[22:26], byteorder='little')

    # f_bitcount = struct.unpack(format,)
    image = Image.open('/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/kodim20.bmp')

    f.seek(0)
    fullImage = bytearray(f.read())

    imageR = saveInFileAndGetComponents(fullImage.copy(), 'red.bmp', 2, pixel_offset, width, height)
    imageG = saveInFileAndGetComponents(fullImage.copy(), 'green.bmp', 1, pixel_offset, width, height)
    imageB = saveInFileAndGetComponents(fullImage.copy(), 'blue.bmp', 0, pixel_offset, width, height)

def getR(image1, image2):
    mean1 = sum(image1) / (width * height)
    mean2 = sum(image2) / (width * height)
    cov = sum([(image1[i] - mean1) * (image2[i] - mean2) for i in range(len(image1))]) / (width * height)
    std1 = math.sqrt(sum([(image1[i] - mean1) ** 2 for i in range(len(image1))]) / (width * height - 1))
    std2 = math.sqrt(sum([(image2[i] - mean2) ** 2 for i in range(len(image2))]) / (width * height - 1))
    corr = cov / (std1 * std2)

    return corr

def cadr(value):
    global tmp
    if value < 0:
        tmp += 1
        return 0
    elif value > 255:
        tmp += 1
        return 255
    return value

def calculateEntropy(arrayValues, label):
    valueToAmount = {}
    for i in arrayValues:
        value = int(i)
        temp = valueToAmount.get(value)
        valueToAmount[value] = 1 if temp == None else valueToAmount[value] + 1
    entropy = 0
    all = 0
    for key in valueToAmount.keys():
        all += valueToAmount[key]
    for key in valueToAmount.keys():
        px = valueToAmount[key] / all
        entropy = entropy - px * math.log2(px)
    print(label, entropy)

def createBarChart(componentArray, label, rangeValues):
    fig = plt.figure()
    plt.title(label)
    plt.hist(componentArray, bins=255, range=rangeValues)
    plt.savefig(label + '_plot.png')
    # plt.show()

def calculateDifferenceModulation(componentArray, width, height, cmplabel):
    diffModulation1 = []
    diffModulation2 = []
    diffModulation3 = []
    diffModulation4 = []
    for i in range(1, height):
        for j in range(1, width):
            diffModulation1.append(componentArray[i * width + j] - componentArray[i * width + j - 1])
            diffModulation2.append(componentArray[i * width + j] - componentArray[(i - 1) * width + j])
            diffModulation3.append(componentArray[i * width + j] - componentArray[(i - 1) * width + j - 1])          
            average = (componentArray[i * width + j - 1] + componentArray[(i - 1) * width + j] + componentArray[(i - 1) * width + j - 1]) / 3
            diffModulation4.append(componentArray[i * width + j] - average)

    createBarChart(diffModulation1, "diff " + cmplabel + " frequency 1", (-127, 128))
    createBarChart(diffModulation2, "diff " + cmplabel + " frequency 2", (-127, 128))
    createBarChart(diffModulation3, "diff " + cmplabel + " frequency 3", (-127, 128))
    createBarChart(diffModulation4, "diff " + cmplabel + " frequency 4", (-127, 128))

    calculateEntropy(diffModulation1, 'H(d' + cmplabel + '^1) = ')
    calculateEntropy(diffModulation2, 'H(d' + cmplabel + '^2) = ')
    calculateEntropy(diffModulation3, 'H(d' + cmplabel + '^3) = ')
    calculateEntropy(diffModulation4, 'H(d' + cmplabel + '^4) = ')

def splitIntoSubframes(array, i_count, j_count):
    h_downsampled, w_downsampled = height // 2, width // 2
    A_downsampled = []
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            A_downsampled.append(array[(i + i_count) * w_downsampled + (j + j_count)])

    A_restored = [[0 for j in range(width)] for i in range(height)]
    for i in range(h_downsampled):
        for j in range(w_downsampled):
            i_new = i * 2 + 1
            j_new = j * 2 + 1

            A_restored[i_new][j_new] = A_downsampled[i * w_downsampled + j]
            if j_new > 0:
                A_restored[i_new][j_new - 1] = A_downsampled[i * w_downsampled + j]
            if i_new > 0:
                A_restored[i_new - 1][j_new] = A_downsampled[i * w_downsampled + j]
            if i_new > 0 and j_new > 0:
                A_restored[i_new - 1][j_new - 1] = A_downsampled[i * w_downsampled + j]
    result = []
    for sublist in A_restored:
        for item in sublist:
            result.append(item)
    return result

def createSubframes(yArray):
    yFile = bytearray(fullImage[:pixel_offset])
    j = 0
    for i in range(pixel_offset, len(fullImage), 3):
        yFile.extend(bytearray([int(yArray[j]), int(yArray[j]), int(yArray[j])]))
        j += 1
    return yFile

def decimationEvenNumbered(array, times=1): # четная нумерация
    h_downsampled, w_downsampled = height, width
    for time in range(times):
        A_downsampled = []
        for i in range(1, h_downsampled + 1, 2):
            for j in range(1, w_downsampled + 1, 2):
                A_downsampled.append(array[i * w_downsampled + j])
        array = A_downsampled
        h_downsampled, w_downsampled = h_downsampled // 2, w_downsampled // 2

    A_restored = []
    for time in range(times):
        A_restored = [[0 for j in range(w_downsampled * 2)] for i in range(h_downsampled * 2)]
        for i in range(h_downsampled):
            for j in range(w_downsampled):
                i_new = i * 2 + 1
                j_new = j * 2 + 1

                A_restored[i_new][j_new] = A_downsampled[i * w_downsampled + j]
                if j_new > 0:
                    A_restored[i_new][j_new - 1] = A_downsampled[i * w_downsampled + j]
                if i_new > 0:
                    A_restored[i_new - 1][j_new] = A_downsampled[i * w_downsampled + j]
                if i_new > 0 and j_new > 0:
                    A_restored[i_new - 1][j_new - 1] = A_downsampled[i * w_downsampled + j]
        A_downsampled = [] # A_downsampled = A_restored
        for sublist in A_restored:
            for item in sublist:
                A_downsampled.append(item)
        h_downsampled *= 2
        w_downsampled *= 2
    return A_restored

def decimationAriphmeticMean(array, times=1): #ср арифм
    h_downsampled, w_downsampled = height, width
    for time in range(times):
        A_downsampled = []
        for i in range(1, h_downsampled + 1, 2):
            for j in range(1, w_downsampled + 1, 2):
                A_downsampled.append((array[i * w_downsampled + j] + array[(i - 1) * w_downsampled + j] + array[i * w_downsampled + j - 1] + array[(i - 1) * w_downsampled + j - 1]) // 4)
        array = A_downsampled
        h_downsampled, w_downsampled = h_downsampled // 2, w_downsampled // 2

    A_restored = []
    for time in range(times):
        A_restored = [[0 for j in range(w_downsampled * 2)] for i in range(h_downsampled * 2)]
        for i in range(h_downsampled):
            for j in range(w_downsampled):
                i_new = i * 2 + 1
                j_new = j * 2 + 1

                A_restored[i_new][j_new] = A_downsampled[i * w_downsampled + j]
                if j_new > 0:
                    A_restored[i_new][j_new - 1] = A_downsampled[i * w_downsampled + j]
                if i_new > 0:
                    A_restored[i_new - 1][j_new] = A_downsampled[i * w_downsampled + j]
                if i_new > 0 and j_new > 0:
                    A_restored[i_new - 1][j_new - 1] = A_downsampled[i * w_downsampled + j]
        A_downsampled = [] # A_downsampled = A_restored
        for sublist in A_restored:
            for item in sublist:
                A_downsampled.append(item)
        h_downsampled *= 2
        w_downsampled *= 2
    return A_restored

def convertForDecimation(yArray, Cr_restored, Cb_restored, label): # Конвертировать для децимации
    global tmp
    tmp = 0
    yFile = bytearray(fullImage[:pixel_offset])
    sumR = 0
    sumG = 0
    sumB = 0
    sumCr = 0
    sumCb = 0
    schet = 0
    for i in range(height):
        for j in range(width):
            g = cadr((yArray[i * width + j] - 0.714 * (Cr_restored[i][j] - 128) - 0.334 * (Cb_restored[i][j] - 128)))
            r = cadr((yArray[i * width + j] + 1.402 * (Cr_restored[i][j] - 128)))
            b = cadr((yArray[i * width + j] + 1.772 * (Cb_restored[i][j] - 128)))
            sumR = sumR + (imageR[i * width + j] - int(r)) ** 2
            sumG = sumG + (imageG[i * width + j] - int(g)) ** 2
            sumB = sumB + (imageB[i * width + j] - int(b)) ** 2
            sumCr = sumCr + (int(Cr_restored[i][j]) - int(crArray[i * width + j])) ** 2
            sumCb = sumCb + (int(Cb_restored[i][j]) - int(cbArray[i * width + j])) ** 2
            yFile.append(int(b))
            yFile.append(int(g))
            yFile.append(int(r))
    print('')
    print(label)
    print('PSNR( Blue ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumB))
    print('PSNR( Green ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumG))
    print('PSNR( Red ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumR))
    print('PSNR( Cb ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumCb))
    print('PSNR( Cr ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumCr))
    print ('clip_count = ' + str(tmp))
    return yFile
print('------------------------------------------------')

print('biBitCount = ' + (str)(image.BITFIELDS * 8))

print('--------------4---correlation-------------------')

print('r(red, green) = ', getR(imageR, imageG))
print('r(red, blue) = ', getR(imageR, imageB))
print('r(blue, green) = ', getR(imageB, imageG))
print('')


yFile = bytearray(fullImage[:pixel_offset])
cbFile = bytearray(fullImage[:pixel_offset])
crFile = bytearray(fullImage[:pixel_offset])
yccFile = bytearray(fullImage[:pixel_offset])


yArray = []
cbArray = []
crArray = []
for i in range(pixel_offset, len(fullImage), 3):
    y = 0.299 * fullImage[i + 2] + 0.587 * fullImage[i + 1] + 0.114 * fullImage[i]
    cb = 0.5643 * (fullImage[i] - y) + 128
    cr = 0.7132 * (fullImage[i + 2] - y) + 128
    yArray.append(y)
    cbArray.append(cb)
    crArray.append(cr)

    yccFile.append(int(cr))
    yccFile.append(int(cb))
    yccFile.append(int(y))


    yFile.extend(bytearray([int(y),int(y),int(y)]))
    crFile.extend(bytearray([int(cr),int(cr),int(cr)]))
    cbFile.extend(bytearray([int(cb),int(cb),int(cb)]))


print('-------------5--correlation------------------')
print('R(y, Cb) = ', getR(yArray, cbArray))
print('R(y, Cr) = ', getR(yArray, crArray))
print('R(Cb, Cr) = ', getR(cbArray, crArray))
print('')


imageFile = open('y.bmp', 'wb')
imageFile.write(bytes(yFile))
imageFile.close()

imageFile = open('Cb.bmp', 'wb')
imageFile.write(bytes(cbFile))
imageFile.close()

imageFile = open('Cr.bmp', 'wb')
imageFile.write(bytes(crFile))
imageFile.close()

imageFile = open('ycc.bmp', 'wb')
imageFile.write(bytes(yccFile)) 
imageFile.close()

tmp = 0
print('---------------------7----------------------')
yFile = bytearray(fullImage[:pixel_offset])
sumR = 0
sumG = 0
sumB = 0 
for i in range(len(yArray)):
    g = cadr((yArray[i] - 0.714 * (crArray[i] - 128) - 0.334 * (cbArray[i] - 128)))
    r = cadr((yArray[i] + 1.402 * (crArray[i] - 128)))
    b = cadr((yArray[i] + 1.772 * (cbArray[i] - 128)))
    sumR = sumR + (imageR[i] - int(r)) ** 2
    sumG = sumG + (imageG[i] - int(g)) ** 2
    sumB = sumB + (imageB[i] - int(b)) ** 2 
    yFile.append(int(b))
    yFile.append(int(g))
    yFile.append(int(r))
print('psnr(blue) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumB))
print('psnr(green) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumG))
print('psnr(red) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumR))
print ('clip_count = ' + str(tmp))

print('')

imageFile = open('after.bmp', 'wb')
imageFile.write(bytes(yFile)) 
imageFile.close()

print('---------------------dop----------------------')
y_new_File = bytearray(fullImage[:pixel_offset])

brightness = 50

sumR = 0
sumG = 0
sumB = 0 
for i in range(len(yArray)):
    g = cadr(yArray[i] - 0.714 * (crArray[i] - 128) - 0.334 * (cbArray[i] - 128))
    r = cadr(yArray[i] + 1.402 * (crArray[i] - 128))
    b = cadr(yArray[i] + 1.772 * (cbArray[i] - 128))
    sumR = sumR + (imageR[i] - int(r)) ** 2
    sumG = sumG + (imageG[i] - int(g)) ** 2
    sumB = sumB + (imageB[i] - int(b)) ** 2 

    new_b = (int(b) + brightness)
    new_g = (int(g) + brightness)
    new_r = (int(r) + brightness)

    
    y_new_File.append(cadr(new_b))
    y_new_File.append(cadr(new_g))
    y_new_File.append(cadr(new_r))


# print('psnr(blue) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumB))
# print('psnr(green) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumG))
# print('psnr(red) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumR))
# print('')

imageFile = open('brightness_DOP.bmp', 'wb')
imageFile.write(bytes(y_new_File)) 
imageFile.close()
print('Complite!\n')

sumR = 0
sumG = 0
sumB = 0 
for i in range(len(yArray)):
    g = cadr(yArray[i] + brightness - 0.714 * (crArray[i] - 128) - 0.334 * (cbArray[i] - 128))
    r = cadr(yArray[i] + 1.402 * (crArray[i] - 128))
    b = cadr(yArray[i] + 1.772 * (cbArray[i] - 128))
    sumR = sumR + (imageR[i] - int(r)) ** 2
    sumG = sumG + (imageG[i] - int(g)) ** 2
    sumB = sumB + (imageB[i] - int(b)) ** 2 

    new_b = (int(b))
    new_g = (int(g))
    new_r = (int(r))

    
    y_new_File.append(cadr(new_b))
    y_new_File.append(cadr(new_g))
    y_new_File.append(cadr(new_r))


imageFile = open('brightness_DOP_ycbcr.bmp', 'wb')
imageFile.write(bytes(y_new_File)) 
imageFile.close()
print('Complite!\n')

print('Complite!\n')

yArray = [round(yArray[i]) for i in range(len(yArray))]
yArray = np.array(yArray)
cbArray = [round(cbArray[i]) for i in range(len(cbArray))]
cbArray = np.array(cbArray)
crArray = [round(crArray[i]) for i in range(len(crArray))]
crArray = np.array(crArray)

imageR = [round(imageR[i]) for i in range(len(imageR))]
imageR = np.array(imageR)
imageG = [round(imageG[i]) for i in range(len(imageG))]
imageG = np.array(imageG)
imageB = [round(imageB[i]) for i in range(len(imageB))]
imageB = np.array(imageB)

# print('------------------12----------------\n')

createBarChart(yArray, "(Y_comp) frequency", (0, 255))
createBarChart(cbArray, "(Cb_comp) frequency", (0, 255))
createBarChart(crArray, "(Cr_comp) frequency", (0, 255))
createBarChart(imageR, "(R_comp) frequency", (0, 255))
createBarChart(imageG, "(G_comp) frequency", (0, 255))
createBarChart(imageB, "(B_comp) frequency", (0, 255))

Cb_restored = decimationEvenNumbered(cbArray)
Cr_restored = decimationEvenNumbered(crArray)

print('---------------------8-11---------------------')

yFile = convertForDecimation(yArray,Cr_restored,Cb_restored, "even_numbered decimation x2")

imageFile = open('after_EvenNumb_Decim_x2.bmp', 'wb')
imageFile.write(bytes(yFile)) 
imageFile.close()

Cb_restored = decimationAriphmeticMean(cbArray)
Cr_restored = decimationAriphmeticMean(crArray)

yFile = convertForDecimation(yArray,Cr_restored,Cb_restored, "ariphmetic mean decimation x2")

imageFile = open('after_AriphmMean_Decim_x2.bmp', 'wb')
imageFile.write(bytes(yFile))
imageFile.close()


Cb_restored2 = decimationEvenNumbered(cbArray, times=2)
Cr_restored2 = decimationEvenNumbered(crArray, times=2)

yFile = convertForDecimation(yArray, Cr_restored2, Cb_restored2, "even_numbered decimation x4")

imageFile = open('after_EvenNumb_Decim_x4.bmp', 'wb')
imageFile.write(bytes(yFile)) 
imageFile.close()

Cb_restored2 = decimationAriphmeticMean(cbArray, times=2)
Cr_restored2 = decimationAriphmeticMean(crArray, times=2)

yFile = convertForDecimation(yArray, Cr_restored2, Cb_restored2, "ariphmetic mean decimation x4")

imageFile = open('after_AriphmMean_Decim_x4.bmp', 'wb')
imageFile.write(bytes(yFile))
imageFile.close()

print('--------------------13----------------------')

calculateEntropy(imageB, 'H(B) = ')
calculateEntropy(imageG, 'H(G) = ')
calculateEntropy(imageR, 'H(R) = ')
calculateEntropy(yArray, 'H(Y) = ')
calculateEntropy(cbArray, 'H(Cb) = ')
calculateEntropy(crArray, 'H(Cr) = ')

print('--------------------16----------------------')
calculateDifferenceModulation(imageB, width, height, 'B')
print('')
calculateDifferenceModulation(imageG, width, height, 'G')
print('')
calculateDifferenceModulation(imageR, width, height, 'R')
print('')
calculateDifferenceModulation(yArray, width, height, 'Y')
print('')
calculateDifferenceModulation(cbArray, width, height, 'Cb')
print('')
calculateDifferenceModulation(crArray, width, height, 'Cr')
print('--------------------------------------------')
