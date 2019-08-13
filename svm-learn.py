import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn import svm

digits=datasets.load_digits()



clf = svm.SVC(gamma=0.0001 , C=1000)

x,y = digits.data [:-1], digits.target[:-1]
clf.fit (x,y)

prediction = clf.predict(digits.data[-6].reshape(1,-1))
print ("prediction : " + str (prediction))

plt.imshow(digits.images[-6], cmap=plt.cm.gray_r, interpolation="nearest")
plt.show()