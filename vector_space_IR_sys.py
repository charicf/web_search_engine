from preprocessing_assg1 import *
import re
import math
import pdb
from nltk.probability import FreqDist

def tokenize_docs(documents):

	tokenized_docs = []

	for doc in documents:
		doc_tokens = get_tokens_by_space(doc)
		preprocess_doc = preprocessing(doc_tokens)
		
		tokenized_docs.append(preprocess_doc)

	return tokenized_docs

def preprocessing(tokens):

	stopwords_rem = remove_stopwords(tokens)
	stemmed_words = get_porter_stemmer(stopwords_rem) # This method performs stemming and then stopword removing

	final_words = [word for word in stemmed_words if len(word) > 2]

	return final_words

def index_docs(tokenized_docs):

	docs_index = {}

	#pdb.set_trace()
	for doc_id, doc in enumerate(tokenized_docs):
		doc_id = doc_id + 1

		try:
			most_freq_term = FreqDist(doc).most_common(1)[0][1]
		except:
			most_freq_term = 1

		for term in doc:
			if term in docs_index:
				#pdb.set_trace()
				if "d"+str(doc_id) in docs_index[term][1]:
					docs_index[term][1]["d"+str(doc_id)] += 1/most_freq_term
				else:
					docs_index[term][1]["d"+str(doc_id)] = 1/most_freq_term
					docs_index[term][0] = len(docs_index[term][1])
			else:
				# Creates term and its dictionary
				docs_index[term] = [1, {"d"+str(doc_id): 1/most_freq_term}]

	return docs_index

def index_query(tokenized_docs, tokenized_query):

	docs_index = {}

	for doc_id, doc in enumerate(tokenized_docs):
		doc_id = doc_id + 1

		terms_freq = FreqDist(doc)

		for term in tokenized_query:
			if term in doc:
				if term in docs_index:
					#pdb.set_trace()
					docs_index[term][1]["d"+str(doc_id)] = terms_freq[term]
					docs_index[term][0] = len(docs_index[term][1])
				else:
					# Creates term and its dictionary
					docs_index[term] = [1, {"d"+str(doc_id): terms_freq[term]}]
			else:
				continue

	return docs_index

def get_weithgs_and_lenghts(inverted_index, N):

	doc_lenghts = {}
	tf_idf = {}

	for i in range(N):
		doc = "d"+str(i+1)
		doc_lenghts[doc] = 0

		
		for term, l in inverted_index.items():
			try:
				weight = (inverted_index[term][1][doc]) * (math.log2(N/inverted_index[term][0]))
				#tf_idf2[doc, term] = weight
				doc_lenghts[doc] = doc_lenghts[doc] + weight**2
				try:
					tf_idf[doc][term] = weight
				except:
					tf_idf[doc] = {term: weight}
			except:
				continue
		doc_lenghts[doc] = math.sqrt(doc_lenghts[doc])

	#pdb.set_trace()
	return tf_idf, doc_lenghts

# Performs Cosine Similarity and retrieves ranked docs
def retrieve_similar_docs(weights, doc_lenghts, inverted_index, query_inv_index, q_lenghts, N):

	cos_sim = {}
	#query_lenght = 0
	#for query_inv_index

	#pdb.set_trace()
	# for q_term, q_df_tf in query_inv_index.items():
	# 	if q_term not in inverted_index: continue
	# 	w = q_df_tf[1]['d1'] * math.log2(N/inverted_index[q_term][0])
	# 	query_lenght = query_lenght + w**2
	# query_lenght = math.sqrt(query_lenght)

	for term, df_tf in query_inv_index.items():

		if term not in inverted_index: 
			print('term not in doccs', term)
			continue

		#pdb.set_trace()
		for doc, tf in inverted_index[term][1].items():

			if doc in cos_sim:
				dot_p = inverted_index[term][1][doc] * df_tf[1][doc] * (math.log2(N/inverted_index[term][0]))**2
				cos_sim[doc] += dot_p/math.sqrt(doc_lenghts[doc]*q_lenghts[doc])
			else:
				dot_p = inverted_index[term][1][doc] * df_tf[1][doc] * (math.log2(N/inverted_index[term][0]))**2
				cos_sim[doc] = dot_p/math.sqrt(doc_lenghts[doc]*q_lenghts[doc])

	sorted_docs = [k for k, v in sorted(cos_sim.items(), reverse=True, key=lambda item: item[1])]

	return sorted_docs


# Read queries file and returns the tokens for each query
def get_queries(path):

	if os.path.isfile(path):

		text = open(path, "r").read().lower()
		queries = [t.strip() for t in text.split(' .')]
		queries = list(filter(None, queries)) # Removes any empty string in the list

	return queries

def get_docs(text_files_dir):	

	vocabulary = []

	
	if text_files_dir[-1] != "\\": text_files_dir = text_files_dir + '\\'
	for filename in os.listdir(text_files_dir):
		#if filename.endswith(".txt"):
		with open(text_files_dir+filename, "r") as input_file:
			vocabulary.append(get_text_of_interest(input_file))

	return vocabulary

def get_text_of_interest(file):

	text = file.read()
	title_re = re.compile('<TITLE>(.*)</TITLE>', re.DOTALL).search(text)
	text_re = re.compile('<TEXT>(.*)</TEXT>', re.DOTALL).search(text)

	text_oi = title_re.group(1) #+ text_re.group(1)

	return text_oi

def get_relevance_info(relevance_path):

	relevance = [None]*10
	if relevance_path[-1] != "\\" and not os.path.isfile(relevance_path): relevance_path = relevance_path + '\\'
	with open(relevance_path,'r') as r:
		for l in r:
			if l:
				x = l.split(' ')
				if relevance[int(x[0])-1] == None:
					relevance[int(x[0])-1] = ['d'+x[1].rstrip()]
				else:
					relevance[int(x[0])-1].append('d'+x[1].rstrip())
			else:
				continue
	return relevance

def run_IR_system(links, pages, query, relevance_path, n_top_docs):

	N = len(pages)

	tokenized_docs = tokenize_docs(pages)
	inverted_index = index_docs(tokenized_docs)

	tokenized_query = tokenize_docs(query)

	#tokenized_query = tokenize_docs([query])
	#query_inv_index = index_docs(tokenized_query, True)

	weights, doc_lenghts = get_weithgs_and_lenghts(inverted_index, N)
	#sorted_docs = retrieve_similar_docs(weights, doc_lenghts, inverted_index, query_inv_index, N)

	# tem = {}
	# for doc, terms in weights.items():
	# 	for i in sorted (weights[doc].keys()):
	# 		tem[i] = inverted_index[i]
	# 	pdb.set_trace()

	avg_precision = 0
	avg_recall = 0
	relevance = get_relevance_info(relevance_path)

	print("\nTop {} documents in rank list\n".format(n_top_docs))

	for i, qu in enumerate(tokenized_query):
		
		query_inv_index = index_query(tokenized_docs, qu)
		q_weights, q_lenghts = get_weithgs_and_lenghts(query_inv_index, N)
		#pdb.set_trace()
		sorted_docs = retrieve_similar_docs(weights, doc_lenghts, inverted_index, query_inv_index, q_lenghts, N)

		top_docs = sorted_docs[:n_top_docs]
		rel_docs_retrieved = len(set(top_docs) & set(relevance[i]))
		rel_docs = len(relevance[i])
		docs_ret = len(top_docs)

		recall = rel_docs_retrieved/rel_docs
		precision = rel_docs_retrieved/docs_ret

		avg_precision += precision
		avg_recall += recall


		print('Query: {}	Pr: {}		Re: {}'.format(i+1, precision, recall))

	print("Avg Precision: ", avg_precision/len(query))
	print("Avg Recall: ", avg_recall/len(query))


	#pdb.set_trace()
	
	return

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--files_path", required = True, default = "cranfieldDocs", help="path to input documents")
ap.add_argument("-q", "--query_path", required = True, default = "queries.txt", help="path to the query file")
ap.add_argument("-r", "--relevance_path", required = True, default = "relevance.txt", help="path to the relevance file")
ap.add_argument("-t", "--top_documents", required = True, default = 500, help="top t documents to take into account")

args = vars(ap.parse_args())
text_files_dir = args["files_path"]
query_path = args["query_path"]
relevance_path = args["relevance_path"]
n_top_docs = int(args["top_documents"])

pages =  get_docs(text_files_dir)
queries = get_queries(query_path)
links = ''

run_IR_system(links, pages, queries, relevance_path, n_top_docs)