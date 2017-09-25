import os

from gensim.models.keyedvectors import KeyedVectors


def clculate(mentionMapPath, vectorFilePath):
    # enter file input name
    mentionMap = 'MentionMap.txt'

    # enter word2vec bin file name
    vectorFileName = 'DocVector_in_word2vec.txt'

    # load word2vec file. Check whether the file is a Binary or not and set the boolean accordingly
    model = KeyedVectors.load_word2vec_format(os.path.join(vectorFilePath, vectorFileName), binary=False)

    # Start reading the file in separate lines
    with open(os.path.join(mentionMapPath, mentionMap)) as f:
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
    outputCount = 100

    # initialize for precision and recall
    precision = 0.0
    recall = 0.0

    # a count varianle to get visual feedback on the document count when running program
    printCounter = 0
    notInDictionary = 0

    # loop through each document in the mention map
    for line in lines:

        # if semicolon is not there, there are no reference
        if (';') not in line:
            pass

        else:
            document = line.split(';')[0]
            referencesList = line.split(';')[1].split(',')

            try:
                modelOutput = model.most_similar(positive=[document], topn=outputCount)

            except KeyError:
                print document + " not in dictionary"
                notInDictionary = notInDictionary - 1
                printCounter = printCounter + 1
                continue

            # create a list of the documents only, returned by the model. Remove the vector values
            documentList = []
            for i in range(0, outputCount):
                documentList.append(modelOutput[i][0])

            intersectionCount = len(list(set(documentList).intersection(referencesList)))

            precision += float(intersectionCount) / float(outputCount)
            recall += float(intersectionCount) / float(100)

        # print str(printCounter) + '/' + str(len(lines)) + ' : Pre = ' + str(precision) + ' / Recall = ' + str(recall)
        printCounter = printCounter + 1

    # calculate the final value for precision and recall
    precision = float(precision) / float(len(lines) - notInDictionary)
    recall = float(recall) / float(len(lines) - notInDictionary)

    print "Precision = " + str(precision * 100),
    print "Recall = " + str(recall * 100)


alpha = ["a0.1", "a0.5", "a1", "a2", "a3"]
p_value = ["p250", "p500", "p750", "p1000"]

for a in alpha:
    for p in p_value:
        print "Alpha: " + a + "\tP value: " + p,
        mentionMapPath = os.path.join("D:\Project", "fyp\word2vec\code\work12\cbwc\work1\drive")
        vectorFilePath = os.path.join("D:\Project", "fyp\word2vec\code\work12\cbwc\work1\drive\Serialized_folder",
                                      a, p)
        clculate(mentionMapPath, vectorFilePath)
