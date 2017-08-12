# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 11:13:25 2017

@author: HRUDAY KUMAR
"""

import sys
import math
import os
import codecs
from pprint import pprint

def calculateCandidateNgrams(n):
    size = n
    #print size
    ngrams=[]
    with codecs.open(pathC,'r',encoding = 'utf-8') as file:
        lines = file.readlines()
        
        
        for each in lines:
            ngrams_line={}
            words = each.strip().split()
            
            if len(words)<size:
                ngram = ' '.join(words).strip()
                if ngram in ngrams_line:
                    ngrams_line[ngram] = ngrams_line[ngram]+1
                else:
                    ngrams_line[ngram] = 1
            else:
                end = len(words)-n
                for i in range (end+1):
                    part = words[i:i+size]
                    ngram = ' '.join(part).strip()
                    
                    if ngram in ngrams_line:
                        ngrams_line[ngram] = ngrams_line[ngram]+1
                    else:
                        ngrams_line[ngram] = 1
            
            ngrams.append(ngrams_line)
    return ngrams
                        
                    
def BP(wordCount_candidate,wordCount_reference):
    if wordCount_candidate<=wordCount_reference:
        ratio = float(wordCount_reference)/float(wordCount_candidate)
        bp = math.exp(1-ratio)
    else:
        bp =1
    return bp

def calculateReferenceNgrams(n,multipleReferences):
    size = n
    #print size
    ngrams=[]
        
    if multipleReferences==0:
        with codecs.open(pathR,'r',encoding = 'utf-8') as file:
            lines = file.readlines()
        
        
            for each in lines:
                ngrams_line={}
                words = each.strip().split()
                
                if len(words)<size:
                    ngram = ' '.join(words).strip()
                    if ngram in ngrams_line:
                        ngrams_line[ngram] = ngrams_line[ngram]+1
                    else:
                        ngrams_line[ngram] = 1
                else:
                    end = len(words)-n
                    for i in range (end+1):
                        part = words[i:i+size]
                        ngram = ' '.join(part).strip()
                    
                        if ngram in ngrams_line:
                            ngrams_line[ngram] = ngrams_line[ngram]+1
                        else:
                            ngrams_line[ngram] = 1
            
                ngrams.append(ngrams_line)
    
    else:
        
        for root, dirs, files in os.walk(pathR, topdown=False):
            #print files
            
            ngrams_list=[]
            for name in files:
                ngrams=[]
                #print name
                pathr = os.path.join(root,name)
                with codecs.open(pathr,'r',encoding = 'utf-8') as file:
                    lines = file.readlines()
                    for each in lines:
                        ngrams_line={}
                        words = each.strip().split()
                
                        if len(words)<size:
                            ngram = ' '.join(words).strip()
                            if ngram in ngrams_line:
                                ngrams_line[ngram] = ngrams_line[ngram]+1
                            else:
                                ngrams_line[ngram] = 1
                        else:
                            end = len(words)-n
                            for i in range (end+1):
                                part = words[i:i+size]
                                ngram = ' '.join(part).strip()
                                
                                if ngram in ngrams_line:
                                    ngrams_line[ngram] = ngrams_line[ngram]+1
                                else:
                                    ngrams_line[ngram] = 1
            
                        ngrams.append(ngrams_line)
                ngrams_list.append(ngrams)
                #print ngrams_list
                #print (len(ngrams_list))
            ngrams = ngrams_list
    return ngrams
                
                
        

#pathR = "test"
#pathC = "candidate-4.txt"

pathR = sys.argv[2]
pathC = sys.argv[1]

multipleReferences = 0
if os.path.isdir(pathR):
    multipleReferences = 1

n = 5

counterC = 0
counterR = 0
scores =[]
for i in range(1,n):
    cand_ngrams = calculateCandidateNgrams(i)
    ref_ngrams = calculateReferenceNgrams(i,multipleReferences)
    #print ref_ngrams
   
    wordCount_candidate = 0
    wordCount_reference = 0
    for each in cand_ngrams:
        wordCount_candidate = wordCount_candidate+sum(each.values())
    if i==1:
        counterC = wordCount_candidate
            
    #print wordCount_candidate
        
    
    if multipleReferences==0:
        for each in ref_ngrams:
            wordCount_reference = wordCount_reference+sum(each.values())
        #print wordCount_reference
        if i==1:
            counterR = wordCount_reference
    else:
        for index in range(len(cand_ngrams)):
            words = []
            for refer in ref_ngrams:
         #       print len(refer)
                count = 0
                for word, counter in refer[index].items():
                    count = count+counter
                words.append(count)
            wordCount_reference = wordCount_reference+ min(words)
        if i==1:
            counterR = wordCount_reference
    
    if multipleReferences==0:
        ngramBLEU = 0
        for index, line in enumerate(cand_ngrams):
            lineBLEU = 0
            ref_line = ref_ngrams[index]
            for ngram, counter in line.items():
                if ngram in ref_line:
                    count = min(counter, ref_line[ngram])
                    lineBLEU = lineBLEU + count
            ngramBLEU = ngramBLEU + lineBLEU
            
        result = float(ngramBLEU)/float(wordCount_candidate)
        #print result
        scores.append(result)
        #print scores
    else:
        ngramBLEU=0
        for index, line in enumerate(cand_ngrams):
            lineBLEU = 0.0
            for ngram, count in line.items():
                maxCount=-1
                for ref in ref_ngrams:
                    ref_line = ref[index]
                    
                    if ngram in ref_line:
                        counting = min(count, ref[index][ngram])
                        if counting>maxCount:
                            maxCount = counting
                else:
                    if maxCount>0:
                        lineBLEU = lineBLEU + float(maxCount)
            ngramBLEU = ngramBLEU + lineBLEU
        #print ngramBLEU
        #print wordCount_candidate
        result =float(ngramBLEU)/float(wordCount_candidate)
        scores.append(result)
        #print scores
        
    
BLEUScore = 0
#print scores
for score in scores:
    pn = math.log(score)
    wn = (1.00/len(scores))
    BLEUScore = BLEUScore+(pn*wn)

BLEUScore = math.exp(BLEUScore)
BLEUScore = BLEUScore * BP(counterC,counterR)
print BLEUScore

f = open('bleu_out.txt','w')
f.write(str(BLEUScore))
f.close()



                        
    

             
                
            
            
        
    

