# -*- coding: utf-8 -*-
"""self driving object detection

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/142tXBV8W9wjXhWhOcSOHrFLr83zwL0OA
"""

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/ultralytics/yolov5
!pip install -qr yolov5/requirements.txt
# %cd yolov5

import torch
from IPython.display import Image, clear_output
from utils.google_utils import gdrive_download

clear_output()

# Commented out IPython magic to ensure Python compatibility.
# %cd /content
!curl -L "YOUR LINK HERE" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip

!mkdir train/
!mkdir train/images
!mkdir train/labels
!mkdir valid/
!mkdir valid/images
!mkdir valid/labels
!mkdir test/
!mkdir test/images
!mkdir test/labels

import os
import shutil

# allImages = glob.glob("/export/images/*.jpg")
allImages = []
for filename in os.listdir("export/images/"):
    if filename.endswith(".jpg"):
      allImages.append(filename)
trainImages = []
valImages = []
trainLabels = []
valLabels = []
testImages = []
testLabels = []
print(len(allImages))
testCount = int(0.2 * len(allImages)/10)
trainCount = len(allImages)/10 - testCount-1
valCount = int(0.2 * trainCount)
trainCount = trainCount - valCount-1

print(trainCount, valCount, testCount)

# create training Dataset
j = 0
k = 0
for i in range(0,int(len(allImages)/10)):
  if i < trainCount: # create training images
    trainImages.append(allImages[i])
  elif i >= trainCount and i<(valCount + trainCount):
    valImages.append(allImages[i])
    # j += 1
  else:
    testImages.append(allImages[i])
    # k += 1

print(len(trainImages), len(valImages), len(testImages))

# moving training images
source = "export/images/"
destination = "train/images/"
for fileT in trainImages:
  shutil.move(source+fileT , destination+fileT)

source = "export/images/"
destination = "valid/images/"
for fileT in valImages:
  shutil.move(source+fileT , destination+fileT)

source = "export/images/"
destination = "test/images/"
for fileT in testImages:
  shutil.move(source+fileT , destination+fileT)

# moving labels
source = "export/labels/"
destination = "train/labels/"
for fileT in trainImages:
  fileT = fileT.replace(".jpg",".txt")
  shutil.move(source+fileT , destination+fileT)

source = "export/labels/"
destination = "valid/labels/"
for fileT in valImages:
  fileT = fileT.replace(".jpg",".txt")
  shutil.move(source+fileT , destination+fileT)

source = "export/labels/"
destination = "test/labels/"
for fileT in testImages:
  fileT = fileT.replace(".jpg",".txt")
  shutil.move(source+fileT , destination+fileT)

# Commented out IPython magic to ensure Python compatibility.
#extracting information from the roboflow file
# %cat data.yaml

# define number of classes based on data.yaml
import yaml
with open("data.yaml", 'r') as stream:
    num_classes = str(yaml.safe_load(stream)['nc'])

# Commented out IPython magic to ensure Python compatibility.
# %cat /content/yolov5/models/yolov5s.yaml

#customize iPython writefile so we can write variables
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))

# Commented out IPython magic to ensure Python compatibility.
# %%writetemplate /content/yolov5/models/custom_yolov5s.yaml
# 
# # parameters
# nc: {num_classes}  # number of classes
# depth_multiple: 0.33  # model depth multiple
# width_multiple: 0.50  # layer channel multiple
# 
# # anchors
# anchors:
#   - [10,13, 16,30, 33,23]  # P3/8
#   - [30,61, 62,45, 59,119]  # P4/16
#   - [116,90, 156,198, 373,326]  # P5/32
# 
# # YOLOv5 backbone
# backbone:
#   # [from, number, module, args]
#   [[-1, 1, Focus, [64, 3]],  # 0-P1/2
#    [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
#    [-1, 3, BottleneckCSP, [128]],
#    [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
#    [-1, 9, BottleneckCSP, [256]],
#    [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
#    [-1, 9, BottleneckCSP, [512]],
#    [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
#    [-1, 1, SPP, [1024, [5, 9, 13]]],
#    [-1, 3, BottleneckCSP, [1024, False]],  # 9
#   ]
# 
# # YOLOv5 head
# head:
#   [[-1, 1, Conv, [512, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 6], 1, Concat, [1]],  # cat backbone P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 13
# 
#    [-1, 1, Conv, [256, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 4], 1, Concat, [1]],  # cat backbone P3
#    [-1, 3, BottleneckCSP, [256, False]],  # 17 (P3/8-small)
# 
#    [-1, 1, Conv, [256, 3, 2]],
#    [[-1, 14], 1, Concat, [1]],  # cat head P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 20 (P4/16-medium)
# 
#    [-1, 1, Conv, [512, 3, 2]],
#    [[-1, 10], 1, Concat, [1]],  # cat head P5
#    [-1, 3, BottleneckCSP, [1024, False]],  # 23 (P5/32-large)
# 
#    [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
#   ]

# Commented out IPython magic to ensure Python compatibility.
# # train yolov5s on custom data for 100 epochs
# # time its performance
# %%time
# %cd /content/yolov5/
# !python train.py --img 416 --batch 16 --epochs 100 --data '../data.yaml' --cfg ./models/custom_yolov5s.yaml --weights '' --name yolov5s_results  --cache

!python detect.py --weights runs/exp0_yolov5s_results/weights/best.pt --img 416 --conf 0.4 --source ../test/images

import glob
from IPython.display import Image, display

for imageName in glob.glob('/content/yolov5/inference/output/*.jpg'):
    display(Image(filename=imageName))
    print("\n")

!python detect.py --weights runs/exp0_yolov5s_results/weights/best.pt --source ../video3.mp4 --conf 0.4