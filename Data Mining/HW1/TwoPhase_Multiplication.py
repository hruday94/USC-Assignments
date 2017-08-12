from pyspark import SparkContext
from operator import add
import sys

sc = SparkContext(appName="inf553")

matrixA = sc.textFile(sys.argv[1],use_unicode=False)
matrixB = sc.textFile(sys.argv[2],use_unicode=False)



elements = matrixA.map(lambda x: x.split(',')).map(lambda x: (x[1],'A'+','+x[0]+','+x[2])).collect()
elementsB = matrixB.map(lambda x: x.split(',')).map(lambda x: (x[0],'B'+','+x[1]+','+x[2])).collect()

elements.extend(elementsB)
#print elements

totalData = sc.parallelize(elements)
reducedData = totalData.groupByKey().map(lambda x:(x[0],list(x[1])))

def multi(i):
    data =[]
    value = i[1]
    for j in value:
        if j.split(',')[0]=='A':
            key1 = j.split(',')[1]
            a = j.split(',')[2]
        else:
            a = 0
        for k in value:
            if k.split(',')[0]=='B':
                key2 = k.split(',')[1]
                b = k.split(',')[2]
                result = int(a)*int(b)
                if result!=0:         
                    data.append((key1+','+key2,result))
    return data


        
hello = reducedData.map(lambda x:multi(x)) 
finalResult = hello.flatMap(lambda x:x).map(lambda x:(x[0],x[1])).reduceByKey(add)
finalResult.map(lambda (k,v):"{0}\t{1}".format(k,v)).saveAsTextFile(sys.argv[3])
