from uic_crawler import *
from vector_space_IR_sys import *

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--start_url", required = False, default = "https://www.cs.uic.edu/", help="URL from crawl starts")

args = vars(ap.parse_args())
start_url = args["start_url"]

spider = UICCrawler()
links, pages = spider.run_crawler(start_url)
query = 'Computer science master of science program'
run_IR_system(links, pages, query)
#pdb.set_trace()
#print(links, pages)	