import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from pydantic import BaseModel
PATH = "C:\\PM\\lab\\fastapi\\demoAPI\\"

#使用说明：需要替换PATH为存储路径，路径下为以用户ID分类的文件夹
#需求如下
#pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python

class MosaData(BaseModel):
    path:str
    ID:list[str]
    location_set:list[list[int]]
    style:int = 1
    mosasize:int = 30
##对有敏感字的区域进行全区域打码
#对单张图片处理
def mosa(name:str,location_set:list[list[int]],style:int = 1,mosasize:int = 30):
    lena = cv2.imread(name,cv2.IMREAD_COLOR)
    if lena:
        location_set[0]
        row, colume,color=lena.shape
        mask=np.zeros((row,colume,color),dtype=np.uint8)
        for e in location_set:
            # mask[e[0]:e[2],e[1]:e[3]]=1   #传入参数为 x1 y1 x2 y2
            mask[e[0]:e[0]+int(1.1*e[3]),e[1]-int(0.3*e[2]):e[1]+e[2]] = 1 # 传入参数top,left,width,height
   
    
        if style==1:#雪花屏
            key=np.random.randint(0,256,size=[row,colume,color],dtype=np.uint8)
            lenaXorKey=cv2.bitwise_xor(lena,key)
            encryptFace=cv2.bitwise_and(lenaXorKey,mask*255)
        if style==2:#纯白
            encryptFace=mask*255
        if style==3:#纯黑
            encryptFace=mask
        if style==4:#变模糊
            temp_img = cv2.resize(lena,dsize=(10,10))
            temp_img = cv2.resize(temp_img,dsize=(colume,row))
            encryptFace = cv2.bitwise_and(temp_img,mask*255)
        if style==5:#马赛克
            temp_img=lena[::mosasize,::mosasize]
            temp_img = cv2.resize(temp_img,dsize=(colume,row),interpolation=0)#最近邻差值
            # print(mask.shape)
            # print(row," ",colume)
            # print(temp_img.shape)
            encryptFace = cv2.bitwise_and(temp_img,mask*255)

               
    
        noFacel=cv2.bitwise_and(lena, (1-mask)*255)
        maskFace=encryptFace+noFacel

        # cv2.imshow("origin",lena)
        # cv2.imshow("after",maskFace)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        return maskFace
    return 0

#从input批量处理输出到output
def mul_mosaic(mosadata:MosaData):
    path= PATH +mosadata.path
    ID=mosadata.ID
    style=mosadata.style
    mosasize=mosadata.mosasize

    outpath = path + '\\' + "output"
    inpath = path + '\\' + "input"
    if not os.path.exists(outpath):
        os.makedirs(outpath)	# 创建文件夹
    i = 0
    for name in ID:
        i+=1
        out_pic=mosa(inpath+'\\'+name,mosadata.location_set,style,mosasize)
        # if not os.path.exists(outpath+'\\'+name):
        #     with open(name, 'w') as fp:
        #         None
        cv2.imwrite(outpath+'\\'+name,out_pic)
    return i
   


#测试用例
# name = r"C:\PM\lab\fastapi\demoAPI\input_123\1.jpg"
# name = r"input_123\1.jpg"
# name = "1.jpg"

mosadata = MosaData(path = "123",
# ID = ["1.jpg","2.jpg","3.jpg"],
ID = ["4.png"],
location_set = [[10,70,13,17],[42,53,14,18]],#2
# location_set = [[70,10,83,27],[53,42,67,60]],
# location_set = [[10,70,27,83],[42,53,60,67]],#1
style = 4,
mosasize=30)

mul_mosaic(mosadata)
# [[10,70,27,83],[42,53,60,67]]
# {
#   "path": "123",
#   "ID": [
#     "4.png"
#   ],
#   "location_set": [[10,70,27,83],[42,53,60,67]],
#   "style": 5,
#   "mosasize": 30
# }

# mosa(name,x1,y1,x2,y2,style,30)
