import sys
import math
import itertools as it
from decimal import Decimal
import codecs

path = 'raw_tag.txt'

word_tag_count = {}
transition = {}


def grouper(input_list, n=2):
    for i in range(len(input_list) - (n - 1)):
        yield input_list[i:i + n]


with open(path, 'r',encoding="utf8") as sentences:
#with open(path, 'r') as sentences:
    tag_list = []
    tag_counter = {}
    lines = []
    for line in sentences:
        tags=[]
        lines.append(line)
        observations = line.split()
        for each in observations:
            tag = each.split('/')[-1]
            tag_list.append(tag)
            tags.append(tag)

            word = each[0:-3]
            if word not in word_tag_count:
                word_tag_count[word] = {}
            if tag not in word_tag_count[word]:
                word_tag_count[word][tag] = 1
            else:
                word_tag_count[word][tag] += 1

        for first,second in grouper(tags, 2):
            if first not in transition:
                transition[first]={}
            if second not in transition[first]:
                transition[first][second] = 1
            else:
                transition[first][second] += 1

    for tag in tag_list:
        if tag not in tag_counter:
            tag_counter[tag] = 1
        else:
            tag_counter[tag] += 1

    for tag1 in set(tag_list):
        if tag1 not in transition:
            transition[tag1]={}
        for tag2 in set(tag_list):
            if tag2 not in transition[tag1]:
                transition[tag1][tag2]=1
            else:
                transition[tag1][tag2] += 1


    #print (tag_counter)
    #print (len(set(tag_list)))


    transition['start'] = {}
    for tag in set(tag_list):
        transition['start'][tag] = 1
    #print (transition)

    lastCounter={}
    for line in lines:
        observation = line.split()[-1]
        tag = observation.split('/')[-1]
        if tag not in lastCounter:
            lastCounter[tag]=1
        else:
            lastCounter[tag]+=1

    counter={}
    for line in lines:
        observation = line.split()[0]
        # print (observation)
        tag = observation.split('/')[-1]
        transition['start'][tag] += 1
        counter['start'] = sum(transition['start'].values())

    for each in word_tag_count.keys():
        for tag in word_tag_count[each].keys():
            #word_tag_count[each][tag] = (float(word_tag_count[each][tag])/float(tag_counter[tag]))
            word_tag_count[each][tag] = math.log(float(word_tag_count[each][tag])/float(tag_counter[tag]))
    
    for tag in set(tag_list):
        counter[tag]=-1
    for each in transition.keys():
        for tag,count in transition[each].items():
            counter[tag] = counter[tag]+count
    for tag in counter:
        if tag in lastCounter:
            counter[tag] = counter[tag]-lastCounter[tag]
    #print ('counter\n')
    #print (counter)
    #print ('\n')
    for each in transition.keys():
        for tag,count in transition[each].items():
            #transition[each][tag] = ((float(transition[each][tag])/float(counter[each])))
            transition[each][tag] = math.log((float(transition[each][tag])/float(counter[each])))

    
    #model = codecs.open('hmmmodel.txt','w','utf-8')
    #model = codecs.open('hmmmodel1.txt','w','utf-8')
    model = codecs.open('hmmmodel2.txt','w','utf-8')
    #model = open('hmmmodel.txt','w')
    #print (transition)
    #print (word_tag_count)
    model.write('tag_list ')
    model.write(str(list(set(tag_list))).strip('[]').replace(',','').replace('\'','')+'\n')
    model.write('# transistion probabilities'+'\n')
    for key,value in transition.items():
        model.write('TProb '+str(key)+' ** '+str(value).strip('{}').replace('\'','').replace(',','').replace(': ',':')+'\n')

    model.write('# emission probabilities'+'\n')
    for key,value in word_tag_count.items():
        model.write('EProb '+str(key)+' ** '+str(value).strip('{}').replace('\'','').replace(',','').replace(': ',':')+'\n')
    model.close()

    #print (transition)

    ########### count of observations:::::
    #print (word_tag_count)

