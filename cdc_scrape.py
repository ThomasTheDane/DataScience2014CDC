# 4/1/2014
# Charles O. Goddard

import requests
from bs4 import BeautifulSoup


"gv-col-title"

def top_pages():
	for i in range(1, 7):
		with open('toppages/page%d.html' % (i,), 'r') as f:
			html = f.read()
		soup = BeautifulSoup(html, "html5lib")
		for a in soup.find_all("a", "gv-col-title"):
			yield a.get('href')


def url2fn(url):
	return url[url.index('cdc.gov/')+8:].replace('/','$')


def scrape_page(url):
	r = requests.get(url)
	if r.status_code != 200:
		raise ValueError(r.status_code)

	soup = BeautifulSoup(r.text, "html5lib")

	with open('toppages/scraped/' + url2fn(url) + '.html', 'w') as f:
		f.write('<!DOCTYPE html><body>\n')
		for div in soup.find_all("div", "syndicate"):
			f.write(str(div)+"\n")
		f.write("</body></html>\n")
	print 'done'


def main(num_pages=600):
	i = 0
	for url in top_pages():
		print url
		try:
			scrape_page(url)
		except Exception, e:
			print e
			print 'failed to scrape'
			print

		i += 1
		if i >= num_pages:
			break

if __name__ == '__main__':
	main()
