from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
import os

rootfolder = r'C:\Users\arnol\Desktop\newproject'
Y, Y_train, Y_test = {}, {}, {}
begin_column_feature = 0            # remember python starts counting at 0
end_column_feature = 8

begin_column_label = 8
end_column_label = 11               # change this line to add more classes

# load the dataset
dataset = pd.read_excel(os.path.join(rootfolder, r'featureclassification.xlsx'))

# split into input (X) and output (Y) variables
X = dataset.iloc[:, :end_column_feature]  # Up to and not including column 8
for i in range(begin_column_label, end_column_label):  # label columns
    Y[i] = dataset.iloc[:, i]

    # split in training and testset
    X_train, X_test, Y_train[i], Y_test[i] = train_test_split(X, Y[i], test_size=0.2)

    # define the keras model
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # compile the keras model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # fit the keras model on the training dataset
    model.fit(X_train, Y_train[i], epochs=150, batch_size=10)

    # make class predictions with the model for data X_test
    predictions = model.predict_classes(X_test)

    # give accuracy for all data input cases
    for j in range((len(X_test))):
        print('%s => %d (expected %d)' % (X_test.iloc[j].tolist(), predictions[j], Y_test[i].iloc[j]))

    # print confusion matrix
    print("Confusion matrix:\n", confusion_matrix(Y_test[i], predictions, labels=None, sample_weight=None,
                                                  normalize=None))
    # save models
    model.save('model ' + dataset.columns[i])

print("Saved models to disk")
