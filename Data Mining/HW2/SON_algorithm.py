from pyspark import SparkContext
from operator import add
import sys
import collections
from collections import defaultdict

sc = SparkContext(appName="inf553")

baskets = sc.textFile(sys.argv[1],use_unicode=False)
baskets1 =list( baskets.collect())
#print baskets1
supportRatio = float(sys.argv[2])
support =float(supportRatio*baskets.count())
print supportRatio

def combinations(noOfElements,itemset):
    return set([one.union(two) for one in itemset for two in itemset if len(one.union(two))==noOfElements])


def Apriori(iterator,supportRatio):
    minSupport = supportRatio
    items, TList = itemsFromData(iterator)
    freqSet = freqItem(items,TList,minSupport)
    return list(freqSet)

def itemsFromData(iterator):
    itemS = set()
    TList = []
    for row in iterator:
        TList.append(frozenset(row))
        for item in row:
            if item:
                itemS.add(frozenset([item]))
    return itemS, TList

def freqItem(items,TList,minSupport):
    items1 = {}
    noOfElements=1
    while (1==1):
        if noOfElements>1:
            items = combinations(noOfElements,items2)
        items2 = calSupport(TList,items,minSupport)
        if items2:
            items1.update(items2)
            noOfElements=noOfElements+1
        else:
            break
    return items1

def calSupport(TList, items,minSupport):
    lengthTList = len(TList)
    l = [(item, float(sum(1 for row in TList if item<=(row)))/lengthTList)for item in items]
    return dict([(item, support) for item, support in l if support>=minSupport])
    
def Counter(x,dataOne):
    for bucket in x:
        for fset in dataOne:
            content= fset.split(',')
            if set(content)<=(set(bucket)):
                yield(fset,1)

inter =baskets.map(lambda x: x.split(',')).mapPartitions(lambda x:Apriori(x,supportRatio),True)
inter  = inter.map(lambda x:'{}'.format(tuple(x),1))
inter = inter.map(lambda x:(x,1)).reduceByKey(lambda x,y:x*y)
inter1 = inter.collect()
f = open(sys.argv[3],'w')
for i in inter1:
    f.write(str(i[0]).replace('\'','').replace(' ','').strip('()').rstrip(',')+'\n')
f.close()
freqData = sc.textFile('output.txt',use_unicode=False)
interim = freqData.collect()
inter2 = baskets.map(lambda x:x.split(',')).mapPartitions(lambda x:Counter(x,interim),True).reduceByKey(add)
inter2 = inter2.filter(lambda x:x[1]>=support)
inter2 = inter2.collect()
output= open(sys.argv[3],'w')
for element in inter2:
    output.write(str(element[0])+'\n')
output.close()
