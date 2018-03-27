#!/usr/bin/env python2
# Trying to implement Naive Bayes
# Copyright 2018, Aswin Babu Karuvally

# get the serious stuff
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
import csv
import numpy as np

# prepare the dataset
def prepare_dataset(csv_file):
    # read the file and prepare csv object
    dataset_file = open(csv_file, 'rb')
    csv_object = csv.reader(dataset_file)

    # load the dataset to a list
    dataset = [row for row in csv_object]

    # remove the header and empty lines
    dataset = dataset[2::2]

    # encode color to numbers
    color = preprocessing.LabelEncoder()
    color.fit([row[4] for row in dataset])
    encoded_colors = color.transform([row[4] for row in dataset])

    # encode model to numbers
    model = preprocessing.LabelEncoder()
    model.fit([row[1] for row in dataset])
    encoded_models = model.transform([row[1] for row in dataset])

    # encode transmission to numbers
    transmission = preprocessing.LabelEncoder()
    transmission.fit([row[5] for row in dataset])
    encoded_transmissions = transmission.transform([row[5] for row in
    dataset])

    # insert the encoded data into the dataset
    for i in range(0, len(dataset)):
        dataset[i][4] = encoded_colors[i]
        dataset[i][1] = encoded_models[i]
        dataset[i][5] = encoded_transmissions[i]

    # separate price from other values
    characteristics = []
    for i in range(0, len(dataset)):
        characteristics.append([dataset[i][0], dataset[i][1], dataset[i][3],
        dataset[i][4], dataset[i][5]])

    price = [int(row[2]) for row in dataset]

    # convert characteristics and price to integers
    int_characteristics = []
    for row in characteristics:
        int_characteristics.append(np.array(row).astype(np.int))
        
    # return the prepared data
    return int_characteristics, price


# test the accuracy of classifier
def test_accuracy(predictions, actual_price):
    # find the deviation between predicted and actual values
    deviation_list = []
    for i in range(0, len(predictions)):
        deviation_list.append(abs(int(predictions[i]) - int(actual_price[i]))) 

    # return the mean deviation
    return sum(deviation_list)/len(deviation_list)


# the main function
def main():
    # prepare the dataset for training
    characteristics, price = prepare_dataset("usedcars.csv")

    # create classifier and train
    classifier = GaussianNB().fit(characteristics, price)

    # prepare the testing dataset
    test_characters, test_price = prepare_dataset("test.csv")

    # do the predictions
    predictions = classifier.predict(test_characters)

    # test for accuracy
    deviation = test_accuracy(predictions, test_price)

    # print the mean deviation
    print("the mean deviation is " + str(deviation))


# call the main function
main()
