from pyspark import SparkContext
from operator import add
import sys
import collections
from operator import itemgetter

sc = SparkContext(appName="inf553")

data = sc.textFile(sys.argv[1],use_unicode=False)
totalData = data.collect()
number_of_bands = 5
number_of_rows = 4
dictData={}
for row in totalData:
    line = row.split(',')
    dictData[int(line[0].strip('U'))]=line[1:]

def findLsh(x):
    userDict={}
    userDict[x[0]] = x[1]
    signatures=[]
    signature = [[min((3*int(x)+13*(i))%100 for x in userDict[user]) for i in range(0,20)] for user in userDict]
    for value in signature:
        signatures.append((int(x[0].strip('U')),value))
    return signatures

def findJaccard(similarSets):
    jaccardUser=[]
    for user1 in similarSets:
        for user2 in similarSets:
            if(user1!=user2):
                jaccard = float(len(list(set(dictData[user1])&set(dictData[user2]))))/float(len(list(set(dictData[user1])|set(dictData[user2]))))
                jaccardUser.append((user1,(jaccard,user2)))
    return jaccardUser    

data = data.map(lambda x:x.split(',')).map(lambda x:(x[0],x[1:])).map(lambda x:findLsh(x))
Total=sc.parallelize([])
for i in range(number_of_bands):
    band = data.map(lambda x:(tuple(x[0][1][0+number_of_rows*i:number_of_rows+number_of_rows*i]),x[0][0])).groupByKey().map(lambda x:list(x[1])).filter(lambda x:len(x)>1).flatMap(lambda x:findJaccard(x))
    Total = sc.union([band,Total])


Total = Total.map(lambda x:(x[0],x[1])).groupByKey()
Total = Total.map(lambda x:(x[0],list(set(list(x[1]))))).sortByKey()
Total = Total.map(lambda x:(x[0],sorted(x[1],key=lambda x:x[1])))
Total = Total.map(lambda x:(x[0],sorted(x[1],key=lambda x:x[0],reverse=True)[:5]))
Total = Total.map(lambda x:(x[0],sorted(x[1],key=lambda x:x[1])))

Total= Total.map(lambda x:(x[0],[each[1] for each in x[1]])).collect()

f = open(sys.argv[2],'w')
for i in Total:
    f.write('U'+str(i[0])+':'+str(['U'+str(each) for each in i[1]]).strip('[]').replace('\'','').replace(' ','')+'\n')
f.close
