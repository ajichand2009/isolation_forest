#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

# Generate random seed.
rng = np.random.RandomState(42)

num_samples = 100
num_features = 3

# Generate training data.
X = 0.3 * rng.randn(num_samples,num_features)
X_train = np.r_[X+2,X-2]

# Generate some regular novel observations.
X = 0.3 * rng.randn(20,num_features)
X_test = np.r_[X+2,X-2]

# Generate some abnormal observations.
X_outliers = rng.uniform(low=-4,high=4,size=(20,num_features))

# Fit the model.
clf = IsolationForest(max_samples=100,random_state=rng)
clf.fit(X_train)

# Predict using the trained classifier
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
y_pred_outliers = clf.predict(X_outliers)

X_all = np.r_[X_train,X_test,X_outliers]
anomaly_score = clf.decision_function(np.r_[X_train,X_test,X_outliers])

# Multiplying array 'anomaly_score' by '-1', in order to sort in descending order.
example_indices = np.argsort(-anomaly_score)

#write_data = np.c_[X_all,anomaly_score.reshape(-1,1)]

write_data = np.c_[X_all[example_indices[:10]],anomaly_score[example_indices[:10]]]

np.savetxt('data.txt',write_data,fmt='%f',delimiter=' ',newline='\n')

print(write_data)

print("MAX SCORE : %f" %np.max(anomaly_score))

#========================================================================
# DIMENSIONALITY REDUCTION
#========================================================================

# TODO : Perform dimensionality reduction to 2, if number of features is more than two.
# This is for visualization purposes. Use PCA package in Scikit-learn to do this.

# Take care that maximum variance is preserved while performing PCA, so that the 
# resulting graphs represent the data with reasonable accuracy.

# Ideally, 99.99% of the variance should be preserved.

pca = PCA(n_components=2)

X_pca_train = pca.fit_transform(X_train)
X_pca_test = pca.fit_transform(X_test)
X_pca_outliers = pca.fit_transform(X_outliers)

X_pca_all = np.r_[X_pca_train,X_pca_test,X_pca_outliers]

variance_ratio = pca.explained_variance_ratio_
singular_values = pca.singular_values_

print(variance_ratio)
print(singular_values)


#========================================================================
# PLOT DATA
#========================================================================

# Plot the line, samples and nearest vectors to the plane
#xx,yy = np.meshgrid(np.linspace(-5,5,50),np.linspace(-5,5,50))
#Z = clf.decision_function(np.c_[xx.ravel(),yy.ravel()])

#Z = Z.reshape(xx.shape)

#plt.title("Isolation Forest")
#plt.contourf(xx,yy,Z,cmap=plt.cm.Blues_r)

#b1 = plt.scatter(X_train[:,0],X_train[:,1],c='white',s=20,edgecolor='k')
#b2 = plt.scatter(X_test[:,0],X_test[:,1],c='green',s=20,edgecolor='k')
#c = plt.scatter(X_outliers[:,0],X_outliers[:,1],c='red',s=20,edgecolor='k')

#plt.axis('tight')
#plt.xlim((-5,5))
#plt.ylim((-5,5))
#plt.legend([b1,b2,c],["training observations","new regular observations","new abnormal observations"],
#			loc="upper left")

#plt.show()
#========================================================================
# 3D Scatter Plot
#========================================================================

#fig = plt.figure()
#ax = Axes3D(fig)
#
#ax.scatter(xx,yy,Z)
#plt.show()
