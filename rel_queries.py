#Thomas Patasnis AM: 3318


import sys
import time
import ast
import math


def createData(transactions_filename):
	transactions_file = open(transactions_filename, 'r')
	transactions = []
	for line in transactions_file:
		array = ast.literal_eval(line)
		transactions.append(array)
	transactions_file.close()
	return transactions




def createQueries(queries_filename):
	queries_file = open(queries_filename, 'r')
	queries = []
	for line in queries_file:
		array = ast.literal_eval(line)
		queries.append(array)
	queries_file.close()
	return queries






def convertDictToArray(dictionary):
	array = []
	for key in dictionary:
		array.append([dictionary[key],key])
	return array



def naive(transactions,query):
	dictionary_1 = {}
	dictionary_2 = {}
	tt = len(transactions)
	rel = {}
	for q in query:
		total_counter = 0
		for t in range(len(transactions)):
			counter = 0
			for i in transactions[t]:
				if(q == i):
					counter+=1
			if(q not in dictionary_1 and counter>0):
				dictionary_1[q] = {t:counter}
			elif(counter>0):
				dictionary_1[q][t] = counter
		dictionary_2[q] = (tt/len(dictionary_1[q]))
	#print(dictionary_2)
	#print(dictionary_1)
	for key in dictionary_1:
		for t in dictionary_1[key]:
			val = dictionary_1[key][t]*dictionary_2[key]
			if t in rel:
				rel[t]+=val
			else:
				rel[t] = val
	res_array = convertDictToArray(rel)
	return res_array





def createInvertedIndex(transactions):
	inv_index = {}
	for i in range(len(transactions)):
		items = transactions[i]
		for item in items:
			if item not in inv_index:
				inv_index[item] = {i:1}
			else:
				flag = False
				if(i not in inv_index[item]):
					inv_index[item][i] = 1
				else:
					inv_index[item][i] += 1

	return inv_index	





def sortDict(dictionary):
    sort_tuple = sorted(dictionary.items(), key=lambda x: x[0])
    sort_dict = dict(sort_tuple)
    return sort_dict




def createTRFDict(sorted_inv_index,transactions):
	trf_dict = {}
	t = len(transactions)
	for key in sorted_inv_index:
		trf = len(sorted_inv_index[key])
		a = t/trf
		b = converListToArray(list(sorted_inv_index[key].items()))
		trf_dict[key] = [a,b]
	return trf_dict



def converListToArray(lst):
	array = []
	for i in lst:
		array.append([i[0],i[1]])
	return array


def converListToDict(lst):
	dict = {}
	for i in lst:
		dict[i[0]] = i[1]
	return dict




def merge(lst1,lst2):
	i=0
	j=0
	enwsh = []
	while i<len(lst1) and j<len(lst2):
		a = lst1[i]
		b = lst2[j]
		if a < b:
			enwsh.append(a)
			i+=1
		elif a > b:
			enwsh.append(b)
			j+=1
		else:
			enwsh.append(a)
			i+=1
			j+=1
	return enwsh



def relevance_Query(trf_dict,query):
	item1 = query[0]
	lst1 = trf_dict[item1][1]
	lst1 = matrixDReduction(lst1)
	#print(lst1)
	for i in range(1,len(query)):
		item2 = query[i]
		lst2 = trf_dict[item2][1]
		lst2 = matrixDReduction(lst2)
		lst1 = merge(lst1,lst2)
	return lst1




def matrixDReduction(lst):
	d1_array = []
	for i in lst:
		d1_array.append(i[0])
	return d1_array





def findRelevance(trf_dict,query,union,sorted_inv_index):
	relevance_array = []
	for trans in union:
		rel = 0
		for q in query:
			if trans in sorted_inv_index[q] :
				rel += trf_dict[q][0]*sorted_inv_index[q][trans]
		relevance_array.append([rel,trans])
	return relevance_array





def findTopK(sorted_rel_array,k):
	topk = []
	stop = k
	if(stop>len(sorted_rel_array)):
		stop = len(sorted_rel_array)
	#reverse iteration
	for i in range(stop):
		topk.append(sorted_rel_array[i])
	return topk





def writeInvertedIndex(trf_dict):
	output = open('invfileocc.txt', 'w')
	for key in trf_dict:
		output.write(str(key)+': '+str(trf_dict[key][0])+', '+str(trf_dict[key][1])+"\n")





def helper(query,trf_dict,sorted_inv_index,k):
	union = relevance_Query(trf_dict,query)
	#print(union)
	rel_array = findRelevance(trf_dict,query,union,sorted_inv_index)
	sorted_rel_array = sorted(rel_array,reverse=True)
	topk = findTopK(sorted_rel_array,k)
	return topk





def execute(trf_dict,sorted_inv_index,k,method,queries,qnum,transactions):
	types = ["Naive Method","Inverted File"]
	if(method == 0):
		start_t = time.time()
		for query in queries:
			if(qnum!=-1):
				rel_array = naive(transactions,query)
				sorted_rel_array = sorted(rel_array,reverse=True)
				results = findTopK(sorted_rel_array,k)
				break
			else:
				rel_array = naive(transactions,query)
				sorted_rel_array = sorted(rel_array,reverse=True)
				results = findTopK(sorted_rel_array,k)
	elif(method==1):
		start_t = time.time()
		for query in queries:
			if(qnum!=-1):
				results = helper(query,trf_dict,sorted_inv_index,k)
				break
			else:
				results = helper(query,trf_dict,sorted_inv_index,k)
	stop_t = time.time()
	total_time = stop_t - start_t
	if(qnum!=-1):
		print(types[method]+" result:\n"+str(results))
	print(types[method]+" computation time: "+str(total_time))








def main(argv):
	transactions_filename = argv[0]
	queries_filename = argv[1]
	qnum = int(argv[2])
	method = int(argv[3])
	k = int(argv[4])
	transactions = createData(transactions_filename)
	queries = createQueries(queries_filename)
	inv_index = createInvertedIndex(transactions)
	sorted_inv_index = sortDict(inv_index)
	trf_dict = createTRFDict(sorted_inv_index,transactions)
	writeInvertedIndex(trf_dict)
	if(qnum==-1):
		if method == -1:
			execute(trf_dict,sorted_inv_index,k,0,queries,qnum,transactions)
			execute(trf_dict,sorted_inv_index,k,1,queries,qnum,transactions)
		else:
			execute(trf_dict,sorted_inv_index,k,method,queries,qnum,transactions)			
	else:
		query = queries[qnum]
		if method == -1:
			execute(trf_dict,sorted_inv_index,k,0,queries,qnum,transactions)
			execute(trf_dict,sorted_inv_index,k,1,queries,qnum,transactions)
		else:
			execute(trf_dict,sorted_inv_index,k,method,queries,qnum,transactions)



if __name__ == '__main__':
	main(sys.argv[1:])
