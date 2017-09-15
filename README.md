# Accuracy_Calculator_on_Trained_Vectors
This program can calculate the precision and recall using a word2vec model against a given golden standard.

Please set the following parametes before running the code

The following two files need to be in the same folder where this python file is contained
1) Word2vec model
2) and a text file as the golden standard (refer to the given text file named "mapAll.txt"

The parameters to be changed in code:
1) mentionMap = should be the name of the golden standard
2) vectorFileName = should be the name of the word2vec model file
3) model = KeyedVectors.load_word2vec_format(currentPath + '/' + vectorFileName, binary=True)
    in here, the binary value should be true if the model is a .bin file. Else it should be false
