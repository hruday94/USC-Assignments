 # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
import math
from collections import defaultdict
from scipy.sparse import csr_matrix
import heapq
from datetime import datetime

def calculate_cosine_similarity(original_dataset):
    result = []
    size = len(original_dataset)
    for i in range(size-1):
        for j in range(i+1,size):
            similarity = cosine(original_dataset[i]["tf_idf"], original_dataset[j]["tf_idf"])
            result.append((similarity,[similarity,[[i],[j]]]))
    return result

def cosine(data_point_one,data_point_two):
    val1 = math.sqrt((data_point_one.multiply(data_point_one)).sum())
    val2 = math.sqrt((data_point_two.multiply(data_point_two)).sum())
    similarity = (data_point_one.multiply(data_point_two)).sum()/(val1*val2)
    return -1*similarity

def check_node(heap_node,existing_clusters):
    paired_docs = heap_node[1]
    for each in existing_clusters:
        if each in paired_docs:
            return 0
    return 1

def calculate_centroid(original_dataset,doc_id):
    size = len(doc_id)
    centroid = original_dataset[doc_id[0]]["tf_idf"]
    for i in range (1,len(doc_id)):
        centroid += original_dataset[doc_id[i]]["tf_idf"]
    centroid = centroid/size
    return centroid
    
        
#path  = 'temp_500.txt'
#path = 'docword.enron_small.txt'
path = sys.argv[1]
#path  = 'tcl.txt'
word_dict = defaultdict(list)
idf_dict = {}
with open(path,'r') as f:
    content = f.readlines()
    no_of_doc = int(content[0])
    no_of_voc = int(content[1])
    no_of_words = int(content[2])
    row =[]
    col =[]
    val = []
    data_matrix = csr_matrix((no_of_doc,no_of_voc))
    
    i=3
    while i<len(content):
        data = content[i].split(' ')
        word_dict[data[1]].append(data[0])
        i=i+1
        
    for key, value in word_dict.items():
        counter = len(word_dict[key])
        idf = math.log((no_of_doc+1),2) - math.log((counter+1),2)
        idf_dict[key] = idf
    
    i=3
    while i < len(content):
        data = content[i].split(' ')
        row.append(int(data[0])-1)
        col.append(int(data[1])-1)
        val.append(float(data[2])*idf_dict[data[1]])
        i=i+1
        
    data_matrix = csr_matrix((val,(row,col)))
    i=0    
    while i < no_of_doc:
        value = math.sqrt(data_matrix[i].multiply(data_matrix[i]).sum())
        data_matrix[i] = data_matrix[i]/float(value)
        i=i+1    
##loading data
    #k = 3
    k=int(sys.argv[2])
    original_dataset = []
    clusters = {}
    id = 0
    i=0
    while i<no_of_doc:
    #for i in range(no_of_doc):
        row_data = {}
        row_data.setdefault("doc_id",id)
        row_data.setdefault("tf_idf",data_matrix[i])
        original_dataset.append(row_data)
        clusters_key = str([id])
        clusters.setdefault(clusters_key,{})
        clusters[clusters_key].setdefault("centroid",data_matrix[i])
        clusters[clusters_key].setdefault("points",[id])
        id = id+1
        i+=1
        
    past_clusters = []
    heap = calculate_cosine_similarity(original_dataset)

#heapifying the heap    
    heapq.heapify(heap)
    heapified_heap = heap
    
    present_clusters = clusters
    
    while len(present_clusters)>k:
       dist, pop_node = heapq.heappop(heapified_heap)
       paired_nodes = pop_node[1]
       #print paired_nodes
       
       if check_node(pop_node,past_clusters)==0:
           continue
       
       n_cluster = {}
       n_cluster_data=[]
       
       for each in paired_nodes:
           for element in each:
               n_cluster_data.append(element)
       n_cluster_centroid = calculate_centroid(original_dataset,n_cluster_data)
       n_cluster.setdefault("centroid",n_cluster_centroid)
       n_cluster.setdefault("points",n_cluster_data)
       
       for pair_item in paired_nodes:
           past_clusters.append(pair_item)
           del present_clusters[str(pair_item)]
# adding a new element in heap
       for e_cluster in present_clusters.values():
           combined_node= []
           similarity = cosine(e_cluster["centroid"], n_cluster["centroid"])
           combined_node.append(similarity)
           combined_node.append([n_cluster["points"],e_cluster["points"]])
           heapq.heappush(heap,(similarity,combined_node))
       
       present_clusters[str(n_cluster_data)] = n_cluster
       #print "c_clusters"
       #print c_clusters[str(n_cluster_data)]
    
    for key,values in present_clusters.items():
        result_dict = present_clusters[key]
        print str([each+1 for each in result_dict["points"]]).strip('[]')
    
    
           
