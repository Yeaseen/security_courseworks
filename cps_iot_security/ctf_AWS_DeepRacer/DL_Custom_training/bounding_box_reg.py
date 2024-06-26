# -*- coding: utf-8 -*-
"""Bounding_Box.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lbXb2rh8zBtxFVbLtpdcFBeLoiawMUTK
"""

!unzip /content/data_cal.zip

!pip install imutils

import os
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model

data = []
target = []
file_names = []

ann_path = "/content/data_cal/annotations.txt"
rows = open(ann_path).read().strip().split("\n")

for idx, row in enumerate(rows):

    row = row.split(",")

    file_name = row[0]
    file_name = file_name.split(".")[0]
    file_name = file_name.split("_")[1]
    file_name = "image_" + file_name + ".jpg"

    coords = row[1]
    coords = coords.split(" ")

    if (idx != 63):
        coords = coords[1:-1]
    else:
        coords = coords[1:]

  
    coords = [int(c) for c in coords]

   
    path = "/content/data_cal/stop_sign/"
    full_path = path + file_name
    img = cv2.imread(full_path)
    (h, w) = img.shape[:2]


    Xmin = float(coords[0]) / w
    Ymin = float(coords[1]) / h
    Xmax = float(coords[2]) / w
    Ymax = float(coords[3]) / h

   
    img = load_img(full_path, target_size=(224, 224))
    img = img_to_array(img)

    data.append(img)
    target.append((Xmin, Ymin, Xmax, Ymax))
    file_names.append(file_name)

data = np.array(data, dtype="float32") / 255.0

target = np.array(target, dtype="float32")

data.shape

target.shape

split = train_test_split(data, target, file_names, test_size=0.10, random_state=42)

(train_imgs, test_imgs) = split[:2]
(train_target, test_target) = split[2:4]
(train_filenames, test_filenames) = split[4:]

print(train_filenames)

f = open("/content/data_cal/test_images.txt", "w")
f.write("\n".join(test_filenames))
f.close()

vgg_model = VGG16(weights="imagenet",
                  include_top=False,
                  input_tensor=Input(shape=(224, 224, 3)))

vgg_model.trainable = False
flatten = vgg_model.output
flatten = Flatten()(flatten)

bbox_head = Dense(128, activation="relu")(flatten)
bbox_head = Dense(64, activation="relu")(bbox_head)
bbox_head = Dense(32, activation="relu")(bbox_head)
bbox_head = Dense(4, activation="sigmoid")(bbox_head)

model = Model(inputs=vgg_model.input, outputs=bbox_head)

LEARNING_RATE = 1e-4
EPOCHS = 70
BATCH_SIZE = 32

opt = Adam(lr=LEARNING_RATE)
model.compile(loss="mse", optimizer=opt)
print(model.summary())

model.fit(train_imgs,
              train_target,
              validation_data=(test_imgs, test_target),
              batch_size=BATCH_SIZE,
              epochs=EPOCHS,
              verbose=1)

plt.style.use("ggplot")

plt.figure()

plt.plot(np.arange(0, EPOCHS),
         H.history["loss"],
         label="train_loss")

plt.plot(np.arange(0, EPOCHS),
         H.history["val_loss"],
         label="val_loss")


plt.title("Bounding Box Regression Loss")
plt.xlabel("Epoch №")
plt.ylabel("Loss")
plt.legend()
plt.savefig("/content/stop_sign_model_loss_plot.png")

model.save("/content/model_stop_signs", save_format="h5")

file_names = open("/content/data_cal/test_images.txt").read().strip().split("\n")
img_paths = []
for f in file_names:
    p = os.path.sep.join([path, f])
    img_paths.append(p)

loaded_model = load_model("/content/model_stop_signs")

loaded_model.fit(train_imgs,
              train_target,
              validation_data=(test_imgs, test_target),
              batch_size=BATCH_SIZE,
              epochs=75,
              initial_epoch=70,
              verbose=1)

num_layers = len(loaded_model.layers)
print(f"Number of layers in the model: {num_layers}")

for img_path in img_paths:

    img = load_img(img_path, target_size=(224, 224))

    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    
    preds = loaded_model.predict(img)[0]

   
    img = cv2.imread(img_path)
    img = imutils.resize(img, width=600)
    (h, w) = img.shape[:2]

    preds[0] = int(preds[0] * w)
    preds[1] = int(preds[1] * h)
    preds[2] = int(preds[2] * w)
    preds[3] = int(preds[3] * h)

 
    preds = [int(p) for p in preds]

    
    cv2.rectangle(img,
                  (preds[0], preds[1]),
                  (preds[2], preds[3]),
                  (0, 255, 0), 3)

    imgplot = plt.imshow(cv2.cvtColor(img,
                                      cv2.COLOR_BGR2RGB))

    plt.show()