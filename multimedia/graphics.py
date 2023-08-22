import math
import pandas as pd
import matplotlib.pyplot as plt

def get_components(image, filename, position, start_pos, width, height):
    step = 0
    store_image = [[]]
    component_pos = 0
    for i in range(start_pos, len(image)):
        cur_height = len(store_image) - 1
        if position != step:
            image[i] = 0
        else:
            store_image[cur_height].append(image[i])
            component_pos = component_pos + 1
        if (component_pos == width and cur_height + 1 != height):
            store_image.append([])
            component_pos = 0
        step = (step + 1) % 3
    imageFile = open(filename, 'wb')
    imageFile.write(bytes(image))
    imageFile.close()

    return store_image

def get_r(image1, image2):
    len1 = len(image1[0])
    len2 = len(image2[0])
    mean1 = sum(sum(image1, [])) / (len(image1) * len1)
    mean2 = sum(sum(image2, [])) / (len(image2) * len2)
    cov = 0
    std1 = 0
    std2 = 0
    for i in range(len(image1)):
        for j in range(len1):
            cov += (image1[i][j] - mean1) * (image2[i][j] - mean2)
            std1 += (image1[i][j] - mean1) ** 2
            std2 += (image2[i][j] - mean2) ** 2
    cov = cov / (len(image2) * len2)
    std1 = math.sqrt(std1 / (len(image2) * len2 - 1))
    std2 = math.sqrt(std2 / (len(image2) * len2 - 1))

    corr = cov / (std1 * std2)

    return corr

def get_r_auto(full_image, delta_x, delta_y):
    image1tm = [[]]
    image2 = [[]]
    W = len(full_image[0])
    H = len(full_image)
    current_row = 0

    def correct_x(x):
        if x < 0:
            return 0
        elif x > H:
            return H
        return x

    def correct_y(y):
        if y < 0:
            return 0
        elif y > W:
            return W
        return y

    first_start_row = correct_x(0 + delta_x)
    first_start_column = correct_y(0 + delta_y)
    first_end_row = correct_x(H + delta_x)
    first_end_column = correct_y(W + delta_y)

    second_start_row = correct_x(0 - delta_x)
    second_start_column = correct_y(0 - delta_y)
    second_end_row = correct_x(H - delta_x)
    second_end_column = correct_y(W - delta_y)
    image1 = [row[first_start_column : first_end_column] for row in full_image[first_start_row : first_end_row]]
    image2 = [row[second_start_column : second_end_column] for row in full_image[second_start_row : second_end_row]]

    return get_r(image1, image2)

def show_graphics(image, title):
    max_check_points = 300
    #all_x.insert(0,math.floor((-0.5) * max_check_points))

    all_x = [i for i in range(-int(max_check_points / 2), int(max_check_points / 2) + 5, 5)]
    all_y = [-10, -5, 0, 5, 10]

    def auto_correlation(all_x, current_y):
        result = []
        for current_x in all_x:
            tmp = get_r_auto(image, current_x, current_y)
            result.append(tmp)
        return result

    #plt.figure()
    #frame = {x:0 for x in range(-10, 15, 5)}
    frame = {y:[] for y in all_y}
    for y in all_y:
        tmp = auto_correlation(all_x, y)
        frame[y] = tmp
        # plt.title(title)
        # plt.plot(all_x, tmp, label='$y = %i$'%y)
        # plt.legend()
    df = pd.DataFrame(frame)
    df.to_excel('/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/g.xlsx')
    #plt.show()

with open('/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/ycc.bmp', 'rb') as f:
    a = str(5)
    header = f.read(54)
    pixel_offset = int.from_bytes(header[10:14], byteorder='little')
    width = int.from_bytes(header[18:22], byteorder='little')
    height = int.from_bytes(header[22:26], byteorder='little')

    f.seek(0)
    full_image = bytearray(f.read())

    # image_r = get_components(full_image.copy(), '/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/red.bmp', 2, pixel_offset, width, height)
    # image_g = get_components(full_image.copy(), '/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/green.bmp', 1, pixel_offset, width, height)
    # image_b = get_components(full_image.copy(), '/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/blue.bmp', 0, pixel_offset, width, height)

    image_Y = get_components(full_image.copy(), '/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/y1.bmp', 2, pixel_offset, width, height)
    image_Cb = get_components(full_image.copy(), '/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/Cb1.bmp', 1, pixel_offset, width, height)
    image_Cr = get_components(full_image.copy(), '/Users/vladislavkacanovskij/Documents/Programs/Python/multimedia/Cr1.bmp', 0, pixel_offset, width, height)

#print(get_r(image_r, image_g))
#print(get_r(image_r, image_b))
# print(get_r(image_b, image_g))
print(get_r(image_Y, image_Cb))
# print(get_r(image_Y, image_Cr))
# print(get_r(image_Cb, image_Cr))


#show_graphics(image_r, "image_r")
#show_graphics(image_b, "image_b")
# show_graphics(image_g, "image_g")
show_graphics(image_Y, "image_Y")
# show_graphics(image_Cb, "image_Cb")
# show_graphics(image_Cr, "image_Cr")