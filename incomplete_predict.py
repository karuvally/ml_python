#!/usr/bin/env python2
# Trying to implement KNN
# Copyright 2018, Aswin Babu Karuvally

# get the serious stuff
from sklearn import neighbors, preprocessing
import csv

# prepare the dataset
def prepare_dataset(dataset):
    # remove the header and empty lines
    if len(dataset) > 1:
        dataset = dataset[2::2]

    # encode color to numbers
    if dataset[0][4] != "":
        color = preprocessing.LabelEncoder()
        color.fit([row[4] for row in dataset])
        encoded_colors = color.transform([row[4] for row in dataset])
        
        for i in range(0, len(dataset)):
            dataset[i][4] = encoded_colors[i]


    # encode model to numbers
    if dataset[0][1] != "":
        model = preprocessing.LabelEncoder()
        model.fit([row[1] for row in dataset])
        encoded_models = model.transform([row[1] for row in dataset])

        for i in range(0, len(dataset)):
            dataset[i][1] = encoded_models[i]

    # encode transmission to numbers
    if dataset[0][5] != "":
        transmission = preprocessing.LabelEncoder()
        transmission.fit([row[5] for row in dataset])
        encoded_transmissions = transmission.transform([row[5] for row in
        dataset])

        for i in range(0, len(dataset)):
            dataset[i][5] = encoded_transmissions[i]

    # separate price from other values
    characteristics = []
    for i in range(0, len(dataset)):
        characteristics.append([dataset[i][0], dataset[i][1], dataset[i][3],
        dataset[i][4], dataset[i][5]])

    price = [row[2] for row in dataset]

    # return the prepared data
    return_dict = {
        'characteristics': characteristics,
        'price': price,
        'encoded_colors': color,
        'encoded_models': model,
        'endcoded_transmissions': transmission
        }
    return return_dict


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
    # set the number of neighbours
    no_neighbors = 15

    # read and prepare training dataset
    dataset_file = open("usedcars.csv", "rb")
    csv_object = csv.reader(dataset_file)
    dataset = [row for row in csv_object]
    
    prepared_dataset = prepare_dataset(dataset)
    dataset_file.close()

    # create classifier and train
    classifier = neighbors.KNeighborsClassifier().fit(
        prepared_dataset['characteristics'], prepared_dataset['price'])

    # prepare the testing dataset
    test_dataset_file = open("test.csv", "rb")
    test_object = csv.reader(test_dataset_file)
    test_dataset = [row for row in test_object]

    prepared_test_dataset = prepare_dataset(test_dataset)
    test_dataset_file.close()

    # do the predictions
    predictions = classifier.predict(prepared_test_dataset['characteristics'])

    new_prediction = classifier.predict([[-1,
        prepared_dataset['encoded_models'].transform(["SEL"])[0], 35000,
        -1, -1]])
    
    print(new_prediction)
    

# call the main function
main()
