# -*- coding: utf-8 -*-
"""Lab2_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18hbOoEeeZCBuXLPUWU3D0b9_LcAVdO81

**Лабораторна робота №2**

Завдання 2.1. Класифікація за допомогою машин опорних векторів (SVM)
"""

#Імпортуємо бібліотеки
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

#Підключаємо вхідний файл, який містить дані
input_file = '/content/income_data.txt'

#Перетворюємо вхідний файл у датафрейм
df = pd.read_csv(input_file, header=None)

#Виведемо перші 10 рядків
df.head(10)

#Виводимо інформацію по даних у датафремі
df.info()

# Ініціалізуємо змінні для збереження даних та обмеження розміру вибірки
X = []
y = []
count_class1 = 0
count_class2 = 0
max_datapoints = 25000

# Зчитуємо дані з текстового файлу пострічково, набираємо достатньо прикладів кожного класу та розділяємо їх на 2 класи
with open(input_file, 'r') as f:
    for line in f.readlines():
        if count_class1 >= max_datapoints and count_class2 >= max_datapoints:
            break

        if '?' in line:
            continue

        data = line[:-1].split(',')

        if data[-1] == ' <=50K' and count_class1 < max_datapoints:
            X.append(data)
            count_class1 += 1

        if data[-1] == ' >50K' and count_class2 < max_datapoints:
            X.append(data)
            count_class2 += 1

# Перетворення на масив numpy
X = np.array(X)

# Кодуємо всі текстові ознаки у числові значення
label_encoder = []
X_encoded = np.empty(X.shape)
for i, item in enumerate(X[0]):
    if item.isdigit():
        X_encoded[:, i] = X[:, i]
    else:
        label_encoder.append(preprocessing.LabelEncoder())
        X_encoded[:, i] = label_encoder[-1].fit_transform(X[:, i])

# Розділяємо ознаки (X) та мітки (y)
X = X_encoded[:, :-1].astype(int)
y = X_encoded[:, -1].astype(int)

#Створюємо модель SVМ-класифікатора
classifier = OneVsRestClassifier(LinearSVC(random_state=0))

#Навчання класифікатора
classifier.fit(X, y)

# Розбиваємо дані на навчальну та тестову вибірки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

# Повторно створюємо та навчаємо класифікатор вже на тренувальних даних
classifier = OneVsRestClassifier(LinearSVC(random_state=0))
classifier.fit(X_train, y_train)

# Передбачаємо результати на тестовій вибірці
y_test_pred = classifier.predict(X_test)

# Обчислення F-міри для SVМ-класифікатора
f1 = cross_val_score(classifier, X, y, scoring='f1_weighted', cv=3)
print('F1 score: ' + str(round(100*f1.mean(), 2)) + '%')

# Передбачення результату для тестової точки даних
input_data = ['37', ' Private', ' 215646', ' HS-grad', ' 9', ' Never-married', ' Handlers-cleaners', ' Not-in-family', ' White', ' Male', ' 0', ' 0', ' 40', ' United-States']

# Кодування тестової точки даних
input_data_encoded = [-1] * len(input_data)
count = 0
for i, item in enumerate(input_data):
    if item.isdigit():
        input_data_encoded[i] = int(item)
    else:
        input_data_encoded[i] = label_encoder[count].transform([item])[0]
        count += 1

input_data_encoded = np.array(input_data_encoded).reshape(1, -1)

# Використання класифікатора для кодованої точки даних та виведення результату
predicted_class = classifier.predict(input_data_encoded)
print(label_encoder[-1].inverse_transform(predicted_class)[0])

# Додаткові метрики для оцінки моделі на тестових даних
f1 = f1_score(y_test, y_test_pred, average='weighted')
precision = precision_score(y_test, y_test_pred, average='weighted')
accuracy = accuracy_score(y_test, y_test_pred)
recall = recall_score(y_test, y_test_pred, average='weighted')

print(f'F1: {f1*100:.2f}%')
print(f'Precision: {precision*100:.2f}%')
print(f'Accuracy: {accuracy*100:.2f}%')
print(f'Recall: {recall*100:.2f}%')