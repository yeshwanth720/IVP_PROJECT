from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os


class node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

class pixel_node:
    
    def __init__(self,right=None,left=None, parent=None, weight=0, code=None):
        self.left = left 
        self.right = right 
        self.parent = parent 
        self.weight = weight 
        self.code = code 
 
#  printing all the nodes
def printNodes(node, val=''):
    newVal = val + str(node.huff)
    if(node.left):
        printNodes(node.left, newVal)
    if(node.right):
        printNodes(node.right, newVal)
    if(not node.left and not node.right):
        print(f"{node.symbol} -> {newVal}")

# code of vatti

def pixel_frequency(pxl_lst):
    pxl_freq = {}
    for i in pxl_lst:
        if i not in pxl_freq.keys():
            pxl_freq[i] = 1
        else:
            pxl_freq[i] += 1
    return pxl_freq

def bitsperpixel(width,height,input_text): 
    length=width*height*24
    file_size_bytes =os.path.getsize(input_text)
    return length/file_size_bytes 

def construct_node(pixel):
    node_lst = []
    for i in range(len(pixel)):
        node_lst.append(pixel_node(weight = pixel[i][1], code=str(pixel[i][0])))
    return node_lst

def construct_tree(node_lst):
    node_lst = sorted(node_lst ,key=lambda pixel_node:pixel_node.weight) 
    while(len(node_lst) != 1):
        node0, node1 = node_lst[0], node_lst[1]
        merge_node = pixel_node(left=node0, right=node1, weight=node0.weight + node1.weight)
        node0.parent = merge_node
        node1.parent = merge_node
        node_lst.remove(node0)
        node_lst.remove(node1)
        node_lst.append(merge_node)
        node_lst = sorted(node_lst ,key=lambda pixel_node:pixel_node.weight) 
    return node_lst

def huffman_encoding(pixel_lst):
    pixel_freq = pixel_frequency(pixel_lst)
    pixel_freq = sorted(pixel_freq.items(), key=lambda item:item[1])
    node_lst = construct_node(pixel_freq)
    huff_tree_head = construct_tree(node_lst)[0]
    encoding_table = {}

    for x in node_lst:
        curr_node = x
        encoding_table.setdefault(x.code, "")
        while(curr_node != huff_tree_head):
            if curr_node.parent.left == curr_node:
                encoding_table[x.code] = "1" + encoding_table[x.code]
            else:
                encoding_table[x.code] = "0" + encoding_table[x.code]
            curr_node = curr_node.parent
    return encoding_table

def encoded_list(pixel_lst,encoding_table):
    decoded_list=""
    dict={}
    j=0
    while(j!=len(pixel_lst)):
     dict[j]=pixel_lst[j]
     j=j+1
    
    for i in dict.keys():
        for key in encoding_table.keys():
            if dict[i] == int(key): 
                decoded_list=decoded_list+(encoding_table[key]) 
    return decoded_list
    


def decoding(w,h,encoding_table, coding_res):
    code_read_now = ''
    new_pixel =[] 
    i = 0
    while (i != len(coding_res)):
        code_read_now = code_read_now + coding_res[i]
        for key in encoding_table.keys():
            if code_read_now == encoding_table[key]: 
                new_pixel.append(int(key))
                code_read_now = ''
                break
        i +=1
    return new_pixel


def convert_channels_to_image(red_list, green_list, blue_list, width, height, output_file='decoded_img.jpg'):
    array_length = len(red_list)

    red_array = np.array(red_list, dtype=np.uint8).reshape((array_length, 1))
    green_array = np.array(green_list, dtype=np.uint8).reshape((array_length, 1))
    blue_array = np.array(blue_list, dtype=np.uint8).reshape((array_length, 1))

    image_array = np.concatenate((red_array, green_array, blue_array), axis=1)
    image = image_array.reshape((height, width, 3))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(output_file, image)



def savefile(array,filename):
    t=open(filename,'w')
    t.write(str(array))
    t.close()
    return




img = Image.open('blue_score.jpg')
image_array = np.array(img)

red_list = image_array[:, :, 0].flatten().tolist()
green_list = image_array[:, :, 1].flatten().tolist()
blue_list = image_array[:, :, 2].flatten().tolist()
blue_table=huffman_encoding(blue_list)
red_table=huffman_encoding(red_list)
green_table=huffman_encoding(green_list)
# plt.hist(green_table)
# plt.show()
savefile(green_table,'greentable.txt')
savefile(blue_table,'bluetable.txt')
savefile(red_table,'redtable.txt')
red_file=encoded_list(red_list,red_table)
savefile(red_file,'red_encoded_list.txt')
savefile(encoded_list(green_list,green_table),'green_encoded_list.txt')
savefile(encoded_list(blue_list,blue_table),'blue_encoded_list.txt')

red_dlist=decoding(img.size[0],img.size[1],red_table,encoded_list(red_list,red_table))
green_dlist=decoding(img.size[0],img.size[1],green_table,encoded_list(green_list,green_table))
blue_dlist=decoding(img.size[0],img.size[1],blue_table,encoded_list(blue_list,blue_table))
convert_channels_to_image(red_dlist,green_dlist,blue_dlist,img.size[0],img.size[1],'decode.jpg')
# convert_channels_to_image(green_dlist,red_dlist,red_dlist,img.size[0],img.size[1],'blue.jpg')




# # print("the width and height are\n")
# # print("the total number of pixels in the image :")
# # plt.hist(g)
# # plt.show()

# premium_func(g,p)
# decoding(img.size[0],img.size[1],p,premium_func(g,p))
# t=open('encoded_img.txt','w')
# t.write(str(g))
# t.close()
# f = open('file.txt', 'w')
# f.write(str(p))
# f.close()
# print("ended")
