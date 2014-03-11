#Thomas Nattestad
#3/3/2014
# class registrant:
	# def __init__(self):

import pylab
import numpy
from matplotlib import cm
from matplotlib import pyplot
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap as Basemap

import csv
import apidata

m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
			projection='lcc',lat_1=33,lat_2=45,lon_0=-95, resolution=None)

def readRegistrants():
	m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
			projection='lcc',lat_1=33,lat_2=45,lon_0=-95, resolution=None)
	# m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
	shp_info = m.readshapefile('st99_d00', 'states', drawbounds=True)

	with open('../data/CY2013Registrants.csv', 'r') as fd:
		registrant_list = list(apidata.read_csv(fd, 'Registrant'))
	registrants = dict((r.registration_token, r) for r in registrant_list)

	print('%d registrants known' % (len(registrants),))

	unknown = set()
	unknown_state = set()
	u_pulls = 0
	total_pulls = 0

	state_pulls = dict((sd['NAME'].lower(), 0) for sd in m.states_info)

	with open('../data/CY2013CodePulls.csv', 'r') as fd:
		pulls = apidata.read_csv(fd, 'CodePull')
		for pull in pulls:
			token = pull.registration_token
			if not token in registrants:
				unknown.add(token)
			else:
				state = registrants[token].state.lower()
				if not state in state_pulls:
					unknown_state.add(state)
					u_pulls += 1
				else:
					state_pulls[state] += 1
			total_pulls += 1

	#read in the populations for us
	populations = {}
	with open('../data/NST_EST2013_ALLDATA.csv', 'r') as fd:
		spamreader = csv.reader(fd)
		for row in spamreader:
			#puerto rico special case:
			if(row[4] == "Puerto Rico Commonwealth"):
				populations["puerto rico"] = row[10]
			else:
				populations[row[4].lower()] = row[10]
			# print row[4], " ", row[10]
	pullsPerCapita = {}
	for i, sd in enumerate(m.states_info):
		state = sd['NAME'].lower()
		# print state
		# print "pulls for state", state_pulls[state]
		# print "population for state", populations[state]
		# print "pulls per capita", float(state_pulls[state]) / float(populations[state])
		if(state_pulls[state]):
			pullsPerCapita[state] = float(state_pulls[state]) / float(populations[state])
		else:
			pullsPerCapita[state] = 0

	for aPull in pullsPerCapita:
		print aPull, " ", pullsPerCapita[aPull]

	minp, maxp = min(pullsPerCapita.values()), max(pullsPerCapita.values())

	print('%d total pulls' % (total_pulls, ))
	print('%d unknown registrants' % (len(unknown),))
	print('%d unknown state names (%d pulls)' % (len(unknown_state), u_pulls))
	print('(min, max) = (%f, %f)' % (minp, maxp))

	cmap = pyplot.get_cmap('Greys_r')
	ax = pyplot.gca()
	
	for i, sd in enumerate(m.states_info):
		state = sd['NAME'].lower()
		pulls = pullsPerCapita[state]
		color = rgb2hex(cmap( ((pulls - minp) / (1.0 * maxp - minp)) )[:3])
		poly = Polygon(m.states[i], facecolor=color)
		ax.add_patch(poly)

	m.drawparallels(numpy.arange(25,65,20),labels=[1,0,0,0])
	m.drawmeridians(numpy.arange(-120,-40,20),labels=[0,0,0,1])

	cax = cm.ScalarMappable(cmap=cmap)
	cax.set_array(state_pulls.values())
	pyplot.colorbar(cax)
	pyplot.title('Code Pulls per State per Capita for CY2013')
	pyplot.show()


readRegistrants()

