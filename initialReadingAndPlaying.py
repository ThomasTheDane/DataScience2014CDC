import csv
import bisect
import copy
import logging
import math
import random
import thinkplot

import numpy
import scipy.stats
from scipy.special import erf, erfinv
import matplotlib
import matplotlib.pyplot as pyplot
import thinkstats2

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
		total += float(dataPiece.percent)
	print 'total of percent: ' + str(total)
	return total

def calcTotalInstances(theData):
	total = 0
	for dataPiece in theData:
		total += float(dataPiece.instances)
	print 'total of instances:' + str(total)
	return total

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
	listOfInstances = [];
	for AData in theData:
		listOfInstances += [AData.instances]

	pyplot.plot(listOfInstances)
	pyplot.xscale('log')
	pyplot.yscale('log')
	pyplot.show()
	# pmf = thinkstats2.MakePmfFromList(listOfInstances)
	# cdf = thinkstats2.MakeCdfFromList(listOfInstances)

	# pdf = thinkstats2.EstimatedPdf(listOfInstances)
	# low, high = min(listOfInstances), max(listOfInstances)
	# xs = numpy.linspace(low, high, 101)
	# kde_pmf = pdf.MakePmf(xs)

	# bin_data = BinData(listOfInstances, low, high, 51)
	# bin_pmf = thinkstats2.MakePmfFromList(bin_data)

	# thinkplot.SubPlot(2, 2, 1)
	# thinkplot.Hist(pmf, width=0.1)
	# thinkplot.Config(title='Naive Pmf')

	# thinkplot.SubPlot(2, 2, 2)
	# thinkplot.Hist(bin_pmf)
	# thinkplot.Config(title='Binned Hist')

	# thinkplot.SubPlot(2, 2, 3)
	# thinkplot.Pmf(kde_pmf)
	# thinkplot.Config(title='KDE PDF')

	# thinkplot.SubPlot(2, 2, 4)
	# thinkplot.Cdf(cdf)
	# thinkplot.Config(title='CDF')

	# thinkplot.Show()

	# calcTotalPercent(theData)
	# calcTotalInstances(theData)

if __name__ == '__main__':
    main()

