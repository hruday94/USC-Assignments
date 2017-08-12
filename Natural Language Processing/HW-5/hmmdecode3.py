import sys
import math
import codecs
import operator
import  collections

path = 'hmmmodel2.txt'
rawPath = 'raw.txt'
transition={}
emission={}
tags = []
model = open('hmmoutput.txt','w')

with open(path,'r',encoding="utf8") as sentences:
#with open(path,'r') as sentences:
    for line in sentences:
        #print (line)
        if 'tag_list ' in line:
            line = line.replace('tag_list','')
            tags = line.split()
            #print (tags)
            
        if '#' not in line:
            if 'TProb ' in line:
                line = line.replace('TProb','')
                line = line.split('**')
                first = line[0]
                if first not in transition:
                    transition[first]={}
                second = line[1].split()
                for element in second:
                    element = element.split(':')
                    if element[0] not in transition[first]:
                        transition[first][element[0]]= element[1]

            if 'EProb ' in line:
                line = line.replace('EProb','')
                line = line.split('**')
                first = line[0].strip()
                if first not in emission:
                    emission[first] = {}
                second = line[1].split()
                for element in second:
                    element = element.split(':')
                    if element[0] not in emission[first]:
                        emission[first][element[0]]=element[1]
    #print (emission)
    #print (transition)
    #print (emission['eat']['VB'])

    #for key, value in transition.items():
    #    model.write(str(key) + ' ' + str(value) + '\n')
    #for key, value in emission.items():
    #    model.write(str(key) + ' ' + str(value) + '\n')

#####applying the algorithm
final_output=[]    
with codecs.open(rawPath,'r','utf-8') as sentences:
    probability = collections.defaultdict(lambda: collections.defaultdict(lambda: -float("inf")))
    backpointer = collections.defaultdict(lambda: collections.defaultdict(lambda: None))
    
    for line in sentences:
        words = line.split()
        total = len(words)
        #print (total)
        for tag in tags:
            if words[0] in emission:
                if tag in emission[words[0]]:
                    probability[tag][0] = float(transition[' start '][tag])+float(emission[words[0]][tag])
            else:
                probability[tag][0] = float(transition[' start '][tag])
            backpointer[tag][0] = ' start '
            #print (backpointer)
        #print (probability)
        for i in range(1,total):
            for tag1 in tags:
                maxVal = -float("inf")
                for tag2 in tags:
                    if words[i] in emission:
                        if tag1 in emission[words[i]]:
                            prob = float(probability[tag2][i-1])+float(transition[' '+str(tag2)+' '][tag1])+float(emission[words[i]][tag1])
                        else:
                            prob = -float('inf')
                    else:
                        prob = float(probability[tag2][i-1])+float(transition[' '+str(tag2)+' '][tag1])
                    if prob>maxVal:
                        maxVal = prob
                probability[tag1][i] = maxVal
                minTag, maxVal = None, -float('inf')
                for tag2 in tags:
                    prob = float(probability[tag2][i-1])+float(transition[' '+str(tag2)+' '][tag1])
                    if prob>maxVal:
                        maxVal = prob
                        minTag = tag2
                backpointer[tag1][i] = minTag
        maxVal = -float('inf')
        for tag2 in tags:
            prob = probability[tag2][total-1]
            #print (prob)
            if prob>maxVal:
                keyTag = tag2
        final = str(backpointer[keyTag].values()).strip('dict_values').strip('[()]').replace('\'','').replace(',','').replace('start','')+' '+keyTag
        final_tag = final.split()
        out = ''
        
        for i in range(len(words)):
            out = out + words[i]+'/'+final_tag[i]+' '
        final_output.append(out)
for i in final_output:
    model.write(i+'\n')
model.close()
        
            
                
            #for key in backpointer.keys():
            #    for i in range(0,total):
            #        print (backpointer[key][i])
            #    print (key)
            
                
                
                
                
'''with codecs.open(rawPath,'r','utf-8') as sentences:
    probability = collections.defaultdict(lambda: collections.defaultdict(lambda: -float('inf')))
    backpointer = collections.defaultdict(lambda: collections.defaultdict(lambda: None))
    for line in sentences:
        words = line.split()
        for tag in tags:
            if words[0] in emission:
                if tag in emission[words[0]]:
                    probability[tag][0] = float(transition[' start '][tag])*float(emission[words[0]][tag])
            else:
                probability[tag][0] = float(transition[' start '][tag])
            if tag not in backpointer:
                backpointer[tag][0] = ' start '
        for i in range(1,len(words)):
            for tag1 in tags:
                prob = 0
                maxVal = -float('inf')
                for tag2 in tags:
                    if words[i] in emission:
                        if tag1 in emission[words[i]]:
                        #print (emission[words[i]]['NN'])
                        #print (float(probability[tag2][0]))
                        #print (float(transition[' '+str(tag2)+' ']['NN']))
                        #print (float(emission[words[i]]['NN']))
                        #print (emission[words[i]])
                            prob = float(probability[tag2][i-1])*float(transition[' '+str(tag2)+' '][tag1])*float(emission[words[i]][tag1])
                            #print(prob)
                    else:
                        prob = float(probability[tag2][i-1])*float(transition[' '+str(tag2)+' '][tag1])
                        #print (prob)
                    if prob > maxVal:
                        maxVal = prob
                probability[tag1][i] = maxVal
            print (probability)
                #minT, maxVal = None,-float('inf')
                #for tag2 in tags:
                #    prob = float(probability[tag2][i-1])+float(transition[' '+str(tag2)+' '][tag1])
                #    if prob>maxVal:
                #        maxVal = prob
                #        minT = tag2
                #    backpointer[tag1][i]=tag2
            

    #print (probability)'''
                
            

'''with codecs.open(rawPath,'r','utf-8') as sentences:
#with open(rawPath,'r') as sentences:
    for line in sentences:
        words = line.split()
        
        bestTag =[]
        maxValue = -100
        if words[0] in emission:
            for key in emission[words[0]].keys():
                if float(emission[words[0]][key])>float(maxValue):
                    maxValue = emission[words[0]][key]
                    tag = key
            bestTag.append(tag)
            
        else:
            for key in transition[' start '].keys():
                if (float(transition[' start '][key])>float(maxValue)):
                    maxValue = transition[' start '][key]
                    tag = key
            bestTag.append(tag)
            
        for i in range(1,len(words)):
            maxValue = -100
            if words[i] in emission:
                for key in emission[words[i]].keys():
                    if float(emission[words[i]][key])>float(maxValue):
                        maxValue = emission[words[i]][key] 
                        tag = key
                bestTag.append(tag)
            else:
                for key in transition[str(' '+bestTag[-1]+' ')].keys():
                    if float(transition[str(' '+bestTag[-1]+' ')][key])>float(maxValue):
                        maxValue = transition[str(' '+bestTag[-1]+' ')][key]
                        tag = key
                bestTag.append(tag)
        output = ''
        #print (len(bestTag))
        for i in range(len(words)):
            output = output+' '+(str(words[i]+'/'+bestTag[i]))
        model.write(output.strip()+'\n')'''
                
