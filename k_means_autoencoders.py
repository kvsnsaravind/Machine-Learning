# -*- coding: utf-8 -*-
"""K-Means_project2_Autoencoders.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1taBj9oSnnuJgc0b9eTlx0cMHHvPhuwxt

**PART-1**
"""

#importing cifar10 data from Keras
from keras.datasets import cifar10

import numpy as np
import cv2

(X_train,Y_train),(X_test,Y_test) = cifar10.load_data()

X_train = np.array([cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) for image in X_train])
X_test = np.array([cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) for image in X_test])
# Understanding the Shape of Train and Test Data
print(X_train.shape)
print(Y_train.shape)
print(X_test.shape)
print(Y_test.shape)

X_train = X_train.astype('float32')/255
X_test = X_test.astype('float32')/255

import matplotlib.pyplot as plt

plt.figure(figsize = (10,9))

for k in range(9):
 plt.subplot(3,3,k+1)
 plt.imshow(X_train[k])

for k in range(5):
  print(Y_train[k])

#reshaping the Train and test set 
X_train = X_train.reshape(len(X_train),-1)
X_test = X_test.reshape(len(X_test),-1)

print(X_train.shape)
print(X_test.shape)

import numpy as np
from scipy.spatial.distance import cdist 
import matplotlib.pyplot as plt
#defining the K-Means Function
def kmeans(X,l,iterations):
    idx = np.random.choice(len(X), l, replace=False)
    centroids = X[idx, :]
     
    distances = cdist(X, centroids ,'euclidean')
     
    points = np.array([np.argmin(i) for i in distances])
    
    for _ in range(iterations): 
        centroids = []
        for idx in range(l):
            temp_cent = X[points==idx].mean(axis=0) 
            centroids.append(temp_cent)
 
        centroids = np.vstack(centroids)
         
        distances = cdist(X, centroids ,'euclidean')
        points = np.array([np.argmin(i) for i in distances])
         
    return points

#labeling the K-Means with 10 clusters/classes
label1=kmeans(X_test,10,250)

#Finding the silhouette value
from sklearn.metrics import silhouette_score
silhouette = silhouette_score(X_test,label1)
print(silhouette)

#Taking a list to check the clusters
list1=[10,15,20,30,40,45]

asclis=[]
for x in list1:
  label = kmeans(X_test,x,250) 
  asclis.append(silhouette_score(X_test,label))
#ploting values for the different sizes of clusters and ASC-Value 
plt.plot(list1,asclis)
plt.title('Different Clusters and ASC-VALUE')

!pip install validclust

#finding the dunn Index value
from sklearn.metrics import pairwise_distances
from validclust import dunn
dist = pairwise_distances(X_test)
dunn(dist,label1)

"""**PART-2**"""

import keras
from keras import layers

# This is the size of our encoded representations
encoding_dim = 32

# This is our input image
input_img = keras.Input(shape=(1024,))
# Encoded and decoded layers of Neural networks
encoded_layer1 = layers.Dense(1024, activation='relu')(input_img)
#drop1=layers.Dropout(0.5)(encoded_layer1)
encoded_layer2 = layers.Dense(64, activation='relu')(encoded_layer1)
#drop2=layers.Dropout(0.5)(encoded_layer2)
encoded_layer3 = layers.Dense(32, activation='relu')(encoded_layer2)
#drop3=layers.Dropout(0.5)(encoded_layer3)
decoded_layer1 = layers.Dense(64, activation='relu')(encoded_layer3)
#drop4=layers.Dropout(0.5)(decoded_layer1)
decoded_layer2= layers.Dense(128, activation='relu')(decoded_layer1)
#drop5=layers.Dropout(0.5)(decoded_layer2)
decoded = layers.Dense(1024, activation='sigmoid')(decoded_layer2)
# This model maps an input to its reconstruction
autoencoder = keras.Model(input_img, decoded)

# This model maps an input to its encoded representation
encoder = keras.Model(input_img, encoded_layer3)

autoencoder = keras.Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
#fitting the tarin data with epochs
autoencoder.fit(X_train, X_train,
                epochs=50,
                batch_size=256,
                shuffle=True)

#Pushing the predicting encoded test into encoding imgs 
encoded_imgs = encoder.predict(X_test)
lis=[10,15,20,30,40,45]

encoded_imgs

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=10, random_state=0).fit(encoded_imgs)
label=kmeans.predict(encoded_imgs)

encoded_imgs.shape

#finding out the silhouette score
from sklearn.metrics import silhouette_score
silhouette = silhouette_score(encoded_imgs,label)
print(silhouette)

#plotiing between the different clusters and ASC-Value
asclis=[]
from sklearn.cluster import KMeans
for x in lis:
  label2= KMeans(n_clusters=x, random_state=0).fit_predict(encoded_imgs)
  #print(silhouette_score(encoded_imgs,label2))
  asclis.append(silhouette_score(encoded_imgs,label2))
plt.plot(lis,asclis)
plt.title('Different Clusters VS ASC-VALUE')

from matplotlib import pyplot as plt
encoded_imgs = encoder.predict(X_test.reshape(10000,1024))
decoded_imgs = autoencoder.predict(X_test.reshape(10000,1024))
n = 10  # number of images to be displayed
plt.figure(figsize=(20, 4))
for i in range(n):
    # Display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(X_test[i].reshape(32, 32))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(32, 32))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

