import csv

class urlData(object):
	def __init__(self, dataRow):
		self.index = dataRow[0]
		self.address = dataRow[1]
		self.instances = dataRow[2]
		self.percent = dataRow[3].split('%')[0]


	def printData(self):
		print('index: ' + self.index)
		print('address: ' + self.address)
		print('instances: ' + self.instances)
		print('percent: ' + self.percent)

def calcTotalPercent(theData):
	total = 0
	for dataPiece in theData:
		print dataPiece.printData()
		total += float(dataPiece.percent)
	print 'total of percent: ' + str(total)

def calcTotalInstances(theData):
	total = 0
	for dataPiece in theData:
		total += float(dataPiece.instances)
	print 'total of instances:' + str(total)

def readDataIn(fileName):
	theData = []
	with open("..\data\\" + fileName, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)
		i = 0
		for row in spamreader:
			#skip the header part
			if i < 25:
				i = i + 1
			else:
				if(row != []):
					theData += [urlData(row)]
	return theData

def main():
	# theData = readDataIn('Page+URLs+(t46)+Report+for+CDC+Internet+-+2013.csv')
	theData = readDataIn('Content+Source+URLs+(t1)+Report+for+CDC+New+Media+-+2013.csv')
	calcTotalPercent(theData)
	# calcTotalInstances(theData)

if __name__ == '__main__':
    main()

