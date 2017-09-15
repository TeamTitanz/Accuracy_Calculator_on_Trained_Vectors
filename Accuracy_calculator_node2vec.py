from gensim.models.keyedvectors import KeyedVectors
import os

# enter file input name
mentionMap = 'finalMentionMap.txt'

# enter word2vec bin file name
vectorFileName = 'numwalk10k_Large_cases_large_10k.emd'

# get Current path of this file
currentPath = os.getcwd()

# load word2vec file. Check whether the file is a Binary or not and set the boolean accordingly
model = KeyedVectors.load_word2vec_format(currentPath + '/' + vectorFileName, binary=False)

# Start reading the file in separate lines
with open(currentPath + '/' + mentionMap) as f:
    lines = f.readlines()
    # stripping the newline character
    lines = [x.strip() for x in lines]

# set the number of similar documents expected to return from the word2vec file
# use the maximum reference document count for a given document in the mention map
max = 0
for line in lines:
    if (';') in line:
        document = line.split(';')[0]
        referencesList = line.split(';')[1].split(',')
        if max < len(referencesList):
            max = len(referencesList)
outputCount = max

# initialize for precision and recall
precision = 0.0
recall = 0.0

# a count varianle to get visual feedback on the document count when running program
printCounter = 0

# loop through each document in the mention map
for line in lines:

    # if semicolon is not there, there are no reference
    if (';') not in line:
        pass

    else:
        document = line.split(';')[0]
        document = document.lstrip("0")
        referencesList = line.split(';')[1].split(',')

        newReferencesList = []
        for reference in referencesList:
                newReferencesList.append(str(int(reference)))

        try:
            modelOutput = model.most_similar(positive=[document], topn=outputCount)
            #print modelOutput
        except KeyError:
            print document + " not in dictionary"
            continue
        
        # create a list of the documents only, returned by the model. Remove the vector values
        documentList = []
        for i in range(0, outputCount):
            documentList.append(modelOutput[i][0])

        intersectionCount = len(list(set(documentList).intersection(newReferencesList)))

        precision += float(intersectionCount) / float(outputCount)
        recall += float(intersectionCount) / float(len(newReferencesList))

    
    print str(printCounter) + '/' + str(len(lines)) + ' : Pre = ' + str(precision) + ' / Recall = ' + str(recall)
    printCounter = printCounter + 1

# calculate the final value for precision and recall
precision = float(precision) / float(len(lines))
recall = float(recall) / float(len(lines))

print "Precision = " + str(precision*100)
print "Recall = " + str(recall*100)

