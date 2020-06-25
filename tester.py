# load and evaluate a saved model
import os

from keras.models import load_model
import pandas as pd
import shutil

rootfolder = r'C:\Users\arnol\Desktop\newproject'

begin_column_feature = 0  # remember python starts counting at 0
end_column_feature = 8

begin_column_label = 8
end_column_label = 11  # change this line to add more classes

positivenrlist = []
qspname = open('filelocationlist.txt', 'r')
qsp_data = qspname.readlines()

for i in range(begin_column_label, end_column_label):

    # load dataset
    dataset_uncut = pd.read_excel(os.path.join(rootfolder, r'featureclassification.xlsx'))
    dataset = dataset_uncut.iloc[:, :end_column_feature]

    # load model
    model = load_model('model ' + dataset_uncut.columns[i])

    # evaluate the model
    predictions = model.predict_classes(dataset)

    for j in range((len(dataset))):
        if predictions[j] == 1:
            positivenrlist.append(str(j + 2))  # + 2 so 0 becomes 2 to correspond to features.xlsx file rows
    print("The following rows were tested positive for " + dataset_uncut.columns[i]
          + ': ' + ', '.join(positivenrlist))
    print("The corresponding .qsp filenames are stored in Positive " + dataset_uncut.columns[i] +
          ' and copied to the Positives folder.')

    positivenamelist = open('Positive ' + dataset_uncut.columns[i] + '.txt', 'w+')
    for number in positivenrlist:
        positivenamelist.write(qsp_data[int(number) - 2])  # - 2 to account for previous + 2
    positivenamelist.close()

    # copy all the .qsp files that were tested positive to their designated folders
    target = os.path.join(rootfolder, r'SAFARI TES data\Selection\positives', dataset_uncut.columns[i])
    if not os.path.exists(target):
        os.mkdir(target)

    positivenamelist = open('Positive ' + dataset_uncut.columns[i] + '.txt', 'r+')
    for line in positivenamelist.readlines():
        shutil.copy(line.strip(), target)
    positivenamelist.close()

    positivenrlist.clear()

qspname.close()
