from uic_crawler import *
from searcher_gui import *
import csv
from os import path
import pdb

def save_crawler_results(links, pages):

	with open('crawler_results.csv', 'w', encoding='utf-8', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(zip(links, pages))

def open_crawler_results(text_files_dir):

	pages = []
	links = []

	
	if text_files_dir[-1] != "\\": text_files_dir = text_files_dir + '\\'
	for filename in sorted(os.listdir(text_files_dir), key=lambda f: int(f.split('.')[0])):
		#if filename.endswith(".txt"):
		with open(text_files_dir+filename, "r", encoding="utf8", newline='') as input_file:
			#vocabulary.append(get_text_of_interest(input_file))
			reader = csv.reader(input_file)
			try:
				data = list(reader)
			except:
				pdb.set_trace()

		for pair in data:
			links.append(pair[0])
			pages.append(pair[1])

	return links, pages

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--start_url", required = False, default = "https://www.cs.uic.edu/", help="URL from crawl starts")
ap.add_argument("-n", "--number_pages", required = False, default = 3000, help="number of pages to crawl")

args = vars(ap.parse_args())
start_url = args["start_url"]
number_pages = int(args["number_pages"])
print(args)

if path.exists("crawled_pages/0.csv"):
#if False:
	links, pages = open_crawler_results('crawled_pages')
else:
	print('Begining crawler, please wait this might take a while :)')
	spider = UICCrawler()
	links, pages = spider.run_crawler(start_url, number_pages)
	#save_crawler_results(links, pages)
	print('Crawling has ended')

app = QApplication(sys.argv)
view = App(links, pages)
sys.exit(app.exec_())

#print(links, pages)	