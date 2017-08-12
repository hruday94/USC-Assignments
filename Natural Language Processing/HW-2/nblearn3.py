import sys
import math

path1 = sys.argv[1]
path2 = sys.argv[2]

label_dictionary = {}
stop_words={'a','an','the','that','this','those','and','is','hotel','me','my','there','stayed','on','it','couldn\'t','have','been','was','were','they','had','some','on','to','was','this','I\'d','it','elevator','but','only','many','out','before','after','any','having','from','while','which','what','why','where','business','meeting','just','even','if','at','months','building','stay','town','location','smoke'}
punctuation = {'.',',','?','/','@','$','%','^','&','*','-','+','=','\'','>','<',}

stop_words={'a','an'}
with open(path2,'r') as labels:
    for line in labels:
        value = " ".join(line.split()[1:])
        key  = " ".join(line.split()[0:1])
        label_dictionary[key] = value

review_dictionary={}
with open(path1,'r') as reviews:
    for line in reviews:
        key  = " ".join(line.split()[0:1])
        value = " ".join(line.split()[1:]).lower()
        for ch in punctuation:
            value = "".join(value.replace(ch,''))
        review_dictionary[key] = value

word_count={}
count_truthful=0
count_positive=0
count_negative=0
count_deceptive=0

count_positive_words=0
count_negative_words=0
count_truthful_words=0
count_deceptive_words=0
for key, value in label_dictionary.items():
    String = label_dictionary[key].split()
    if String[0]==  "truthful":
        count_truthful +=1
        
    if String[0]==  "deceptive":
        count_deceptive +=1
        
    if String[1]==  "positive":
        count_positive +=1
        
    if String[1]==  "negative":
        count_negative +=1
        

    for word in review_dictionary[key].split():
        if word not in word_count and word not in stop_words:
            word_count[word] = [0,0,0,0]
        if word in word_count:
            if String[0] == "truthful":
                count_truthful_words+=1
                word_count[word][0]+=1
                
            else:
                word_count[word][1]+=1
                count_deceptive_words+=1
                
            if String[1] == "positive":
                word_count[word][2]+=1
                count_positive_words+=1
                
            else:
                word_count[word][3]+=1
                count_negative_words+=1
                

model = open("nbmodel.txt",'w')
total_no_of_data = len(label_dictionary.keys())
total_no_of_words = len(word_count)
prior_truthful = math.log(count_truthful/total_no_of_data)
prior_deceptive = math.log(count_deceptive/total_no_of_data)
prior_positive = math.log(count_positive/total_no_of_data)
prior_negative = math.log(count_negative/total_no_of_data)
model.write("##This file contains the data of prior probabilities of the classes and the log values of the probabilities of each feature in their respective class before smoothing and after smoothing#\n#\n")
String_pt = "prior_truthful\t"+str(prior_truthful)+"\n"
String_pd = "prior_deceptive\t"+str(prior_deceptive)+"\n"
String_pp = "prior_positive\t"+str(prior_positive)+"\n"
String_pn = "prior_negative\t"+str(prior_negative)

model.write(String_pt)
model.write(String_pd)
model.write(String_pp)
model.write(String_pn)


model.write("\n#\n#probabilities after smoothing")
model.write("\n#WORD\t\tTRUTHFUL\t\t\tDECEPTIVE\t\t\tPOSITIVE\t\tNEGATIVE")
for key, value in word_count.items():
    probs_truthful = math.log((word_count[key][0]+1)/(count_truthful_words+total_no_of_words))
    probs_deceptive = math.log((word_count[key][1]+1)/(count_deceptive_words+total_no_of_words))
    probs_positive = math.log((word_count[key][2]+1)/(count_positive_words+total_no_of_words))
    probs_negative = math.log((word_count[key][3]+1)/(count_negative_words+total_no_of_words))
    
    model.write("\n"+key+"\t"+str(probs_truthful)+"\t"+str(probs_deceptive)+"\t"+str(probs_positive)+"\t"+str(probs_negative))
model.close()
     
   
    
    
    

    
    

            

        
        
         
