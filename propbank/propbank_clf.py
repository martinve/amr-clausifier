import sklearn
import sklearn.model_selection
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import metrics
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv("propbank_ args.tsv", sep="\t")
print(data.head())

train_data, dev_data = sklearn.model_selection.train_test_split(data, test_size=0.3, random_state=0)
train_data.shape, dev_data.shape

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train_data['Descr'])`
X_dev_counts = count_vect.transform(dev_data['Descr'])

y_train = train_data['Func']
y_dev = dev_data['Func']

clf = MultinomialNB().fit(X_train_counts, y_train)

predicted = clf.predict(X_dev_counts)
print(clf.score(X_dev_counts, y_dev))

print(metrics.classification_report(y_dev, predicted))

cm = metrics.confusion_matrix(y_dev, predicted)
print(cm)

import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_estimator(clf, X_dev_counts, y_dev)
plt.show()