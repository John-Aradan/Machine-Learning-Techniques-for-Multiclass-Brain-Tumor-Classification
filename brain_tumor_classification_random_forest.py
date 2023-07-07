# -*- coding: utf-8 -*-
"""Brain-Tumor-Classification-Random_Forest.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vJut9G2AaLzikN9o-8mwZZ-LkveF2nNY
"""

from google.colab import drive
drive.mount('/content/drive')

"""  ### Load Modules"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

"""### Prepare/collect data"""

import os

train_path = "/content/drive/MyDrive/Brain_Tumor_Classification/brain-tumor-detection-master/brain_tumor/Training/"   # path to training set folder

classes = {'no_tumor':0, 'pituitary_tumor':1, 'glioma_tumor':2, 'meningioma_tumor':3} # define induvidual classes

import cv2
X = []
Y = []
for cls in classes:
    pth = train_path + cls
    for j in os.listdir(pth):
        img = cv2.imread(pth+'/'+j, 0)      # read image as x_train
        img = cv2.resize(img, (200,200))    # resize the image to 200 * 200
        X.append(img)                       # add the resized image to the list X
        Y.append(classes[cls])              # read and add number assosiated with class to which the image belongs to e.g.:'no_tumour' ->0 to list Y

X = np.array(X)   # convert list X to a numpy array
print(X.shape)
Y = np.array(Y)   # convert list Y to a numpy array (1222,)

X_updated = X.reshape(len(X), -1) # convert to 2D array (1222, 200, 200) -> (1222, 40000)
print(X_updated.shape)
print(Y.shape)

np.unique(Y)

pd.Series(Y).value_counts()   # cont of number of images beloning to each unique class

"""### Split Data"""

# X and Y are split to 2 sets called train and test. The ratio at which the sets are split is defined by test_size

xtrain, xtest, ytrain, ytest = train_test_split(X_updated, Y, random_state=10,test_size=.20)

# sanity check to ensure that there are no missing data

(xtrain.shape[0]==ytrain.shape[0]) & (xtest.shape[0]==ytest.shape[0])

"""### Feature Scaling"""

print(xtrain.max(), xtrain.min())   # normalising the data from 0->255 to 0->1
print(xtest.max(), xtest.min())
xtrain = xtrain/255
xtest = xtest/255
print(xtrain.max(), xtrain.min())
print(xtest.max(), xtest.min())

"""### Train Model"""

# import model to study

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100)  # You can choose different hyperparameters
rf.fit(xtrain, ytrain)

"""### Prediction"""

pred = rf.predict(xtest) # sv_pred -> prediction for each image(xtest) value

misclassified=np.where(ytest!=pred)    # array of images which were
misclassified

# print the prediction and true value for each misclassified sample for SVM {simillarly check for linear, logistic, etc.} by replacing 'sv_pred' in misclassified=np.where(ytest!=sv_pred)

print("Total Misclassified Samples: ",len(misclassified[0]))    # This information has value

# for i in misclassified[0]:
#   print(f"SVM {i} : prediction {sv_pred[i]}, true {ytest[i]}")

# sanity check
xtest.shape,pred.shape,ytest.shape

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(ytest, pred)
print(cm)
acc = accuracy_score(ytest, pred)
precision = precision_score(ytest, pred,average='micro')
recall = recall_score(ytest, pred,average='micro')
f1 = f1_score(ytest, pred,average='micro')
print("Accuracy: ", acc)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1-Score: ", f1)

"""### TEST MODEL

We will now test this model on unseen data
"""

test_path = "/content/drive/MyDrive/Brain_Tumor_Classification/brain-tumor-detection-master/brain_tumor/Testing/"   # path to training set folder

classes = {'no_tumor':0, 'pituitary_tumor':1, 'glioma_tumor':2, 'meningioma_tumor':3}

import cv2
X = []
Y = []
for cls in classes:
    pth = test_path + cls
    for j in os.listdir(pth):
        img = cv2.imread(pth+'/'+j, 0)      # read image as x_train
        img = cv2.resize(img, (200,200))    # resize the image to 200 * 200
        X.append(img)                       # add the resized image to the list X
        Y.append(classes[cls])

X = np.array(X)   # convert list X to a numpy array
Y = np.array(Y)   # convert list Y to a numpy array (1222,)

X_updated = X.reshape(len(X), -1) # convert to 2D array (1222, 200, 200) -> (1222, 40000)

pd.Series(Y).value_counts()

X_updated = X_updated/255
print(X_updated.max(), X_updated.min())

pred = rf.predict(X_updated)

cm = confusion_matrix(Y, pred)
print(cm)
acc = accuracy_score(Y, pred)
precision = precision_score(Y, pred, average='micro')
recall = recall_score(Y, pred, average='micro')
f1 = f1_score(Y, pred, average='micro')
print("Accuracy: ", acc)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1-Score: ", f1)

classes=np.unique(Y)
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title("Random Forest")
plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)

thresh = cm.max() / 2.
for i, j in np.ndindex(cm.shape):
    plt.text(j, i, cm[i, j],
             horizontalalignment="center",
             color="white" if cm[i, j] > thresh else "black")

plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()