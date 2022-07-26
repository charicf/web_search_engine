# Web Search Engine for UIC domain - InformationRetrieval
Implementation of a web search engine for the UIC domain as a part of the Information Retrieval class. The Information Retrieval (IR) field seeks to develop methods to find the right material to satisfy an information need. A web search engine is a “software system that is designed to search the WWW in a systematic way for particular information specified in a textual web search query”. These engines have been used to index the web and find information that an Internet user is requesting. 

The goal for this project is to design and implement a search engine that includes components for web crawling, web page processing, indexing and search engine. To do so, a web crawler is constructed to retrieve the pages within the University of Illinois at Chicago (UIC) domain. The pages, or documents, received are then sent to an IR system based on the  Vector Space Model (VSM) to retrieve the relevant pages according to the user’s query.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

```python
python main.py <args>

"-p", "--files_path", required = False, default = "cranfieldDocs", help="path to input documents"
"-q", "--query_path", required = False, default = "queries.txt", help="path to the query file"
"-r", "--relevance_path", required = False, default = "relevance.txt", help="path to the relevance file"
"-td", "--top_documents", required = False, default = 500, help="top t documents to take into account"
"-t", "--testing_mode", required = False, default = 0, help="Testing mode. True or False"

```

By default, it searches the pages in the domain "https://www.cs.uic.edu/" and the first 3000 pages. To change this behavior, you should change these values in the main.py file.

## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)