import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pdb

class UICSpider(CrawlSpider):
	name = "UIC_spider"

	allowed_domains = ['uic.edu']

	start_urls = [
		'https://www.cs.uic.edu/'
	]

	rules = [Rule(LinkExtractor(canonicalize=True, unique=True),
			follow=False,
			callback="parse_items"
		)]

	#def __init__(self):
	#	self.links = []

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url, callback=self.parse, dont_filter=True)

	# def parse(self, response):

	# 	self.links.append(str(response.url))
	# 	print('The LINKS are: ', self.links)
	# 	#for href in response.css('a::attr(href)'):

	def parse_items(self, response):
		#pdb.set_trace()
		# The list of items that are found on the particular page
		items = []
		# Only extract canonicalized and unique links (with respect to the current page)
		links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
		for link in links:
			# Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
			is_allowed = False
			for allowed_domain in self.allowed_domains:
				if allowed_domain in link.url:
					is_allowed = True
			# If it is allowed, create a new item and add it to the list of found items
			if is_allowed:
				
				items.append({'from': response.url, 'to': link.url})
		# Return all the found items
		print('los Links SON: ', items)
		return items