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
            documentId = line.split(';')[0]
            referencesList = line.split(';')[1].split(',')
            if max < len(referencesList):
                max = len(referencesList)
    outputCount = max

    # initialize for precision and recall
    precision = 0.0
    recall = 0.0

    # a count variance to get visual feedback on the document count when running program
    printCounter = 0
    notInDictionary = 0

    # loop through each document in the mention map
    for line in lines:

        # if semicolon is not there, there are no reference
        if (';') not in line:
            pass

        else:
            documentId = line.split(';')[0]
            documentId = documentId.lstrip("0")
            referencesList = line.split(';')[1].split(',')

            if ('' in referencesList):
                referencesList = filter(lambda a: a != '', referencesList)

            if (documentId in referencesList):
                referencesList = filter(lambda a: a != documentId, referencesList)

            try:
                modelOutput = model.most_similar(positive=[documentId], topn=outputCount)
            except KeyError:
                print documentId + " not in dictionary"
                notInDictionary = notInDictionary - 1
                printCounter = printCounter + 1
                continue

            # create a list of the documents only, returned by the model. Remove the vector values
            modelReturnedDocumentList = []
            for i in range(0, outputCount):
                modelReturnedDocumentList.append(str(modelOutput[i][0]))

            intersectionCount = 0
            for mentionCaseId in referencesList:
                if (mentionCaseId in modelReturnedDocumentList):
                    intersectionCount += 1

            precision += float(intersectionCount) / float(outputCount)

            referencesListLength = len(referencesList)
            if (referencesListLength != 0):
                recall += float(intersectionCount) / referencesListLength
                # print str(printCounter) + '/' + str(len(lines)), ' ; Recall = ' + str(float(intersectionCount) / referencesListLength)
            else:
                # If references list length is zero
                recall += 1.0
                # print str(printCounter) + '/' + str(len(lines)), ' ; Recall = ' + str(1.0)

        printCounter = printCounter + 1

    # calculate the final value for precision and recall
    precision = float(precision) / float(len(lines) - notInDictionary)
    recall = float(recall) / float(len(lines) - notInDictionary)

    # print "Precision = " + str(precision * 100),
    print "Recall = " + str(recall * 100)


alpha = ["a0.1", "a0.5", "a1", "a2", "a3"]
p_value = ["p250", "p500", "p750", "p1000", "p2000"]

for a in alpha:
    for p in p_value:
        print "Alpha: " + a + "\tP value: " + p,
        mentionMapPath = os.path.join("D:\Project", "fyp\word2vec\code\work12\cbwc\work1\drive")
        vectorFilePath = os.path.join("D:\Project", "fyp\word2vec\code\work12\cbwc\work1\drive\Serialized_folder",
                                      a, p)
        clculate(mentionMapPath, vectorFilePath)
