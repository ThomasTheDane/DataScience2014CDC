import operator

interestingWordsAndCount = {}

def loadInCommonWords():
	fin = open('100MostCommonWords.txt')
	for line in fin:
		return set(line.split(', '))

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def getIntPart(val):
	toReturn = ""
	for char in val:
		if(RepresentsInt(char)):
			toReturn += char
	return int(toReturn)

def makeGoInteresting(commonWords):
	fin = open('wordsLogFile.txt')
	for line in fin:
		for word in line.split('{')[1].split(','):
			if not word.split(':')[0] in commonWords:
				if(len(word.split(':')) == 2):
					if(word.split(':')[0] in interestingWordsAndCount):
						if(RepresentsInt(word.split(':')[1])):
							interestingWordsAndCount[word.split(':')[0]] += int(word.split(':')[1])
					else:
						if(RepresentsInt(word.split(':')[1])):
							interestingWordsAndCount[word.split(':')[0]] = int(word.split(':')[1])

	import operator
	interestingWordsAndCountSorted = sorted(interestingWordsAndCount.iteritems(), key=operator.itemgetter(1))
	return interestingWordsAndCountSorted

def saveDictionary(dictionary):
	import csv
	w = csv.writer(open("interestingWords.csv", "w"))
	for key in dictionary:
	    w.writerow(key)

if __name__ == '__main__':
	saveDictionary(makeGoInteresting(loadInCommonWords()))


