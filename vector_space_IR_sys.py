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
		
		#token_freq_doc = get_TF_values(preprocess_doc)

		tokenized_docs.append(preprocess_doc)

	return tokenized_docs

def preprocessing(tokens):

	stopwords_rem = remove_stopwords(tokens)
	stemmed_words = get_porter_stemmer(stopwords_rem) # This method performs stemming and then stopword removing

	final_words = [word for word in stemmed_words if len(word) > 2]

	return final_words

def get_TF_values(toeknized_doc): # Receives a list of dictionaries

	pdb.set_trace()
	token_freq = FreqDist(toeknized_doc).most_common(1)[0][1]
	return token_freq
	#pdb.set_trace()
	# TF_doc_collection = []
	# for document_dic in doc_collection:
	# 	total = max(document_dic.values()) # Maximum frequency in the document
	# 	if total != 0:
	# 		document_dic = {word: freq / total for word, freq in document_dic.items()}
	# 	#pdb.set_trace()

		
	# 	TF_doc_collection.append(document_dic)

	# return TF_doc_collection

def index_docs(tokenized_docs, query=False):

	docs_index = {}
	most_freq_term = 1

	for doc_id, doc in enumerate(tokenized_docs):

		if not query: 
			most_freq_term = FreqDist(doc).most_common(1)[0][1]
		for term in doc:
			if term in docs_index:
				#pdb.set_trace()
				if "d"+str(doc_id) in docs_index[term][1]:
					docs_index[term][1]["d"+str(doc_id)] += 1/most_freq_term
				else:
					docs_index[term][0] = len(docs_index[term][1])
					docs_index[term][1]["d"+str(doc_id)] = 1/most_freq_term

			else:
				# Creates term and its dictionary
				docs_index[term] = [1, {"d"+str(doc_id): 1/most_freq_term}]

	return docs_index

def get_weithgs_and_lenghts(inverted_index, N):

	doc_lenghts = {}
	tf_idf = {}

	for i in range(N):
		doc = "d"+str(i)
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
def retrieve_similar_docs(weights, doc_lenghts, inverted_index, query_inv_index, N):

	cos_sim = {}
	query_lenght = 0
	#for query_inv_index

	for q_term, q_df_tf in query_inv_index.items():
		w = q_df_tf[1]['d0'] * math.log2(N/inverted_index[q_term][0])
		query_lenght = query_lenght + w**2
	query_lenght = math.sqrt(query_lenght)

	for term, df_tf in query_inv_index.items():

		for doc, tf in inverted_index[term][1].items():

			if doc in cos_sim:
				dot_p = inverted_index[term][1][doc] * df_tf[1]['d0'] * (math.log2(N/inverted_index[term][0]))**2
				cos_sim[doc] += dot_p/math.sqrt(doc_lenghts[doc]*query_lenght)
			else:
				dot_p = inverted_index[term][1][doc] * df_tf[1]['d0'] * (math.log2(N/inverted_index[term][0]))**2
				cos_sim[doc] = dot_p/math.sqrt(doc_lenghts[doc]*query_lenght)

	sorted_docs = [k for k, v in sorted(cos_sim.items(), reverse=True, key=lambda item: item[1])]

	return sorted_docs

def run_IR_system(links, pages, query):

	N = len(pages)

	tokenized_docs = tokenize_docs(pages)
	inverted_index = index_docs(tokenized_docs, False)

	tokenized_query = tokenize_docs([query])
	query_inv_index = index_docs(tokenized_query, True)

	weights, doc_lenghts = get_weithgs_and_lenghts(inverted_index, N)
	sorted_docs = retrieve_similar_docs(weights, doc_lenghts, inverted_index, query_inv_index, N)

	pdb.set_trace()
	
	return