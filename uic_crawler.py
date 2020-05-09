from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request 
import sys
import argparse
import pdb
from domain import *
import re
import time
from socket import timeout
import ssl
import http.client

class UICCrawler:

	def __init__(self):
		# Create queue
		self.urls_queue = deque([])

		# Maintains list of visited pages
		self.traversed_links = []
		self.uic_domain = 'uic.edu'
		self.pages = []

	def canonicalize_url(self, complete_url, visited=True):

		sub_url = ''
		parsed = urlparse(complete_url)
		#scheme = "%s://" % parsed.scheme
		#temp_url = parsed.geturl().replace(scheme, '', 1)
		if parsed.scheme in ['https', 'http']:
			if visited:
				temp_url = parsed.netloc + parsed.path
			else:
				temp_url = parsed.scheme + '://' + parsed.netloc + parsed.path

			sub_url = re.sub(r'www.', '', temp_url)
			if sub_url and (sub_url[-1] == '/'): sub_url = sub_url[:-1] 
		return sub_url

	def split_URLs_by_space(self, invalid_url):

		#pdb.set_trace()
		urls = invalid_url.split()
		separated = []
		#urls = list(filter(lambda x: all([urlparse(x).scheme, urlparse(x).netloc]), urls))
		for url in urls:
			parsed_url = urlparse(url)
			if all([parsed_url.scheme, parsed_url.netloc]):
				separated.append(url)

		return separated

	def validate_addition_url(self, complete_url):	

		return (self.canonicalize_url(complete_url)) and (self.canonicalize_url(complete_url, False) not in self.urls_queue) and (self.canonicalize_url(complete_url) not in self.traversed_links) and (get_domain(complete_url) == self.uic_domain)
		
		#if (self.canonicalize_url(complete_url)) and (self.canonicalize_url(complete_url, False) not in self.urls_queue) and (self.canonicalize_url(complete_url) not in self.traversed_links) and (get_domain(complete_url) == self.uic_domain):
		#	self.urls_queue.append(self.canonicalize_url(complete_url, False))

		#return 

	def crawl(self, current_url):

		text = ''
		print(len(self.traversed_links))

		if self.canonicalize_url(current_url) not in self.traversed_links:
			self.traversed_links.append(self.canonicalize_url(current_url))
		else:
			return

		if len(self.traversed_links) == 474: pdb.set_trace()

		try:
			req = urllib.request.Request(current_url)
			req.add_header('User-Agent', 'Mozilla/5.0')
			url_init = urllib.request.urlopen(req, timeout=10)
			#url_init = urllib.request.urlopen(url, timeout=10)
			bsoup = BeautifulSoup(url_init.read(), features="lxml")
			#pdb.set_trace()
			urls = bsoup.findAll('a', href=True)
			#bsoup.findAll(text=True)
			text = bsoup.getText(' ', strip=True)

			for i in urls:

				# Complete relative URLs and strip trailing slash
				complete_url = urljoin(current_url, i["href"]).rstrip('/')

				# if ' ' in complete_url:
				# 	new_urls = self.split_URLs_by_space(complete_url)
				# 	for j in new_urls:
				# 		#complete_url = urljoin(current_url, j["href"]).rstrip('/')
				# 		self.validate_addition_url(j)

				# else:
				# 	self.validate_addition_url(complete_url)

				#cs-events/calendar
				if self.validate_addition_url(complete_url):
					self.urls_queue.append(self.canonicalize_url(complete_url, False))

		except urllib.error.HTTPError as exception:
			self.traversed_links.pop()
			print(current_url, exception)
			return

		except urllib.error.URLError as exception:
			self.traversed_links.pop()
			print(current_url, exception)
			return

		except http.client.HTTPException as exception: # Catch if invalid url names exist
			self.traversed_links.pop()
			print(current_url, exception)
			urls = self.split_URLs_by_space(current_url)
			for u in urls:
				if self.validate_addition_url(u):
					self.urls_queue.appendleft(self.canonicalize_url(u, False))
			return

		except ssl.SSLCertVerificationError as exception:
			self.traversed_links.pop()
			print(current_url, exception)
			return

		except timeout:
			self.traversed_links.pop()
			print(current_url, 'timed out')
			return

		return text

#'engineeringalumni.uic.edu/contact', 'uofi.uic.edu/sb/sec/1860547', 'admissions.uic.edu/graduate-professional', 'engineering.uic.edu/\n                                      https:/engineering.uic.edu/about/faculty/teaching-resources/online-teaching-essentials/\n                                  ']
#deque(['http://engineering.uic.edu/\n                                      https:/go.uic.edu/COE-fund\n                                  ', 'http://engineering.uic.edu/\n                                      https:/today.uic.edu/coronavirus', 'https://engineering.uic.edu/news-stories/professors-haiti-work-brings-real-world-experience-to-students', 'https://engineering.uic.edu/news-stories/brent-stephens-receives-nsf-career-award-for-work-in-computer-science', 'https://engineering.uic.edu/news-stories/five-cme-student-awarded-asce-scholarships', 'http://fimweb.fim.uic.edu/Images/Maps/Visitor%20East%20Side.pdf', 'http://fimweb.fim.uic.edu/Images/Maps/Visitor%20West%20Side.pdf', 'http://fimweb.fim.uic.edu/Images/Maps/Accessibility%20East%20Side.pdf', 'http://fimweb.fim.uic.edu/Images/Maps/Accessibility%20West%20Side.pdf', 'http://maps.uic.edu/Maps/UIC_COM_Rockford_Campus_Map.pdf', 'http://maps.uic.edu/Maps/UIC_COM_Peoria_Campus_Map.pdf', 'http://peoria.medicine.uic.edu/about/visiting', 'http://rockford.medicine.uic.edu/about/visiting', 'https://cs.uic.edu/~brents', 'https://cs.uic.edu/~elena'
	def run_crawler(self, start_url):

		
		self.urls_queue.append(self.canonicalize_url(start_url, False))

		while len(self.urls_queue) > 0 and len(self.traversed_links) < 5:

			#time.sleep(1)
			#url = 'http://engineering.uic.edu/\n                                      https:/today.uic.edu/coronavirus'
			#page_text = self.crawl(url)
			#self.split_URLs_by_space(url)
			#pdb.set_trace()
			current_url = self.urls_queue.popleft()
			page_text = self.crawl(current_url)
			
			if (page_text) and (page_text is not None): self.pages.append(page_text)

		return self.traversed_links, self.pages
