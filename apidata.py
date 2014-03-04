# 2/12/14
# Charles O. Goddard

from collections import namedtuple
import csv


def decamel(s):
	res = [s[0].lower()]
	for c in s[1:]:
		if c.isupper():
			res.append('_')
			res.append(c.lower())
		else:
			res.append(c)
	return ''.join(res)


def make_rectype(name, fields):
	pynames = map(decamel, fields)
	c2p = dict(zip(fields, pynames))
	base = namedtuple(name, ' '.join(pynames))
	class InnerClass(base):
		def __new__(cls, *args, **kw):
			mapped = {}
			for key, arg in zip(pynames, args):
				mapped[key] = arg
			for key in kw:
				if key in c2p:
					key = c2p[key]
				mapped[key] = kw[key]
			return super(InnerClass, cls).__new__(cls, **mapped)

	InnerClass.__name__ = name
	return InnerClass


def read_csv(fd, typename):
	r = csv.reader(fd)
	header = r.next()
	if '' in header:
		header = header[:header.index('')]
	Record = make_rectype(typename, header)

	for row in r:
		yield Record(*row)
