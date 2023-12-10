from PIL import Image
import numpy as np
import cv2

def create_intensity_groups():
    intensity_dict={}
    intensity_groups = []
    intensity=0
    while(intensity<=255):
        if intensity <= 25:
            intensity_groups.append([intensity])
            intensity_dict[int(intensity)]=int(intensity)
            intensity=intensity+1
        elif 25 < intensity <= 75:
            intensity_groups.append([intensity, intensity + 1])
            intensity_dict[int(intensity)]=int(intensity)
            intensity_dict[intensity+1]=intensity
            intensity=intensity+2
        elif 75 < intensity <= 150:
            intensity_groups.append([intensity, intensity + 1, intensity + 2])
            intensity_dict[intensity]=intensity+1
            intensity_dict[intensity+1]=intensity+1
            intensity_dict[intensity+2]=intensity+1
            intensity=intensity+3
        elif 150 < intensity <= 255:
            intensity_groups.append([intensity, intensity + 1, intensity + 2, intensity + 3])
            intensity_dict[intensity]=intensity+2
            intensity_dict[intensity+1]=intensity+2
            intensity_dict[intensity+2]=intensity+2
            intensity=intensity+4
    # print(intensity_dict)
    return intensity_dict

def image_transformation(array,intensity_dict):
    i=0
    while(i!=len(array)):
        for key in intensity_dict.keys():
            if key==array[i]:
                 array[i]=np.array(intensity_dict[key]).astype(np.uint8)
        i=i+1
    print(array)
    return array

def compress_intensity(image_path, compression_factor,output_path):
    original_image = Image.open(image_path)
    image_array = np.array(original_image)
    compressed_array = image_array * compression_factor
    compressed_array = np.clip(compressed_array, 0, 255)
    compressed_image = Image.fromarray(compressed_array.astype('uint8'))
    compressed_image.save(output_path)


def code(url):
    img = Image.open(url)
    width=img.size[0]
    height=img.size[1]
    image_array = np.array(img)
    red_list = image_array[:, :, 0].flatten()
    green_list = image_array[:, :, 1].flatten()
    blue_list = image_array[:, :, 2].flatten()
    list_intensities=create_intensity_groups()
    red_array=image_transformation(red_list,list_intensities).reshape((image_array[:,:,0].size,1))
    blue_array=image_transformation(blue_list,list_intensities).reshape((image_array[:,:,0].size,1))
    green_array=image_transformation(green_list,list_intensities).reshape((image_array[:,:,0].size,1))
    image_array = np.concatenate((red_array, green_array, blue_array), axis=1)
    image = image_array.reshape((height, width, 3))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('anamithra.jpg', image)
    compress_intensity('anamithra.jpg',0.9,'anamithra.jpg')
