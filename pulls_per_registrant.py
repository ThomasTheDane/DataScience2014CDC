# 2/21/14
# Charles O. Goddard

import apidata

import thinkstats2
import thinkplot

pullct = {}

with open('../data/CY2013CodePulls.csv', 'r') as fd:
	pulls = apidata.read_csv(fd, 'CodePull')
	for pull in pulls:
		token = pull.registration_token
		if not token in pullct:
			pullct[token] = 0
		pullct[token] += 1

pullct_prob = {}
for key, value in pullct.items():
	if value not in pullct_prob:
		pullct_prob[value] = 0
	pullct_prob[value] += 1
pmf = thinkstats2.Pmf(pullct_prob)

s = 1
N = len(pullct_prob)
zipf1 = thinkstats2.Pmf(dict((x, x**(-s) / sum(n**(-s) for n in range(1, N+1))) for x in range(1, N+1)))
s = 2
zipf2 = thinkstats2.Pmf(dict((x, x**(-s) / sum(n**(-s) for n in range(1, N+1))) for x in range(1, N+1)))


transform = 'pareto'

scale = thinkplot.Cdf(pmf.MakeCdf(), transform=transform)
thinkplot.Cdf(zipf1.MakeCdf(), transform=transform)
#thinkplot.Cdf(zipf2.MakeCdf(), transform=transform)
thinkplot.Show(**scale)
