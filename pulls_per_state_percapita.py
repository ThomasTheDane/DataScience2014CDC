# 2/13/14
# Charles O. Goddard

import pylab
import numpy
from matplotlib import cm
from matplotlib import pyplot
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap as Basemap

import apidata

m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
			projection='lcc',lat_1=33,lat_2=45,lon_0=-95, resolution=None)
# m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
shp_info = m.readshapefile('st99_d00', 'states', drawbounds=True)

state_populations = {'california': 38332521, 'texas': 26448193,
'new york': 19651127, 'florida': 19552860, 'illinois': 12882135,
'pennsylvania': 12773801, 'ohio': 11570808, 'georgia': 9992167,
'michigan': 9895622, 'north carolina': 9848060, 'new jersey': 8899339,
'virginia': 8260405, 'washington': 6971406, 'massachusetts': 6692824,
'arizona': 6626624, 'indiana': 6570902, 'tennessee': 6495978,
'missouri': 6044171, 'maryland': 5928814, 'wisconsin': 5742713,
'minnesota': 5420380, 'colorado': 5268367, 'alabama': 4833722,
'south carolina': 4774839, 'louisiana': 4625470, 'kentucky': 4395295,
'oregon': 3930065, 'oklahoma': 3850568, 'puerto rico': 3615086,
'connecticut': 3596080, 'iowa': 3090416, 'mississippi': 2991207,
'arkansas': 2959373, 'utah': 2900872, 'kansas': 2893957,
'nevada': 2790136, 'new mexico': 2085287, 'nebraska': 1868516,
'west virginia': 1854304, 'idaho': 1612136, 'hawaii': 1404054,
'maine': 1328302, 'new hampshire': 1323459, 'rhode island': 1051511,
'montana': 1015165, 'delaware': 925749, 'south dakota': 844877,
'alaska': 735132, 'north dakota': 723393, 'district of columbia': 646449,
'vermont': 626630, 'wyoming': 582658}

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

for state in state_pulls:
	state_pulls[state] /= float(state_populations[state])

minp, maxp = min(state_pulls.values()), max(state_pulls.values())

print('%d total pulls' % (total_pulls, ))
print('%d unknown registrants' % (len(unknown),))
print('%d unknown state names (%d pulls)' % (len(unknown_state), u_pulls))
print('(min, max) = (%d, %d)' % (minp, maxp))

cmap = pyplot.get_cmap('Greens')
ax = pyplot.gca()
for i, sd in enumerate(m.states_info):
	state = sd['NAME'].lower()
	pulls = state_pulls[state]
	color = rgb2hex(cmap((pulls - minp) / (1.0 * maxp - minp))[:3])
	poly = Polygon(m.states[i], facecolor=color)
	ax.add_patch(poly)

m.drawparallels(numpy.arange(25,65,20),labels=[1,0,0,0])
m.drawmeridians(numpy.arange(-120,-40,20),labels=[0,0,0,1])

cax = cm.ScalarMappable(cmap=cmap)
cax.set_array(state_pulls.values())
pyplot.colorbar(cax)
pyplot.title('Code Pulls per Capita for CY2013')
pyplot.show()
