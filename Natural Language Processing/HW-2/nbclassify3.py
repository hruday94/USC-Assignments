import sys
import math

path2 = sys.argv[1]

path1 = 'nbmodel.txt'

model_dictionary = {}
prior_truthful=0
prior_deceptive=0
prior_positive=0
prior_negative=0
with open(path1,'r') as model:
    for line in model:
        if '#' not in line:
            if "prior_truthful" in line:
                data = line.split()
                prior_truthful = data[1]
            elif "prior_deceptive" in line:
                data = line.split()
                prior_deceptive = data[1]
            elif "prior_positive" in line:
                data = line.split()
                prior_positive = data[1]
            elif "prior_negative" in line:
                data = line.split()
                prior_negative = data[1]
            else:
                probs = line.split()
                model_dictionary[probs[0]] = [probs[1],probs[2],probs[3],probs[4]] 
                
            


output = " "

to_be_classified_dictionary = {}
stop_words={'a','an','the','that','this','those','and','is','hotel','me','my','there','stayed','on','it','couldn\'t','have','been','was','were','they','had','some','on','to','was','this','I\'d','it','elevator','but','only','many','out','before','after','any','having','from','while','which','what','why','where','business','meeting','just','even','if','at','months','building','stay','town','location','smoke'}
punctuation = {'.',',','?','/','@','$','%','^','&','*','-','+','=','\'','>','<',}
nboutput = open("nboutput.txt",'w')
with open(path2,'r') as to_be_classified:
    for line in to_be_classified:
        key  = " ".join(line.split()[0:1])
        value = " ".join(line.split()[1:]).lower()
        for ch in punctuation:
            value = "".join(value.replace(ch,''))
        to_be_classified_dictionary[key] = value
        prob_tru=float(prior_truthful)
        prob_dec=float(prior_deceptive)
        prob_pos=float(prior_positive)
        prob_neg= float(prior_negative)
        for word in to_be_classified_dictionary[key].split():
            
            if word in model_dictionary and word not in stop_words:
                prob_tru = prob_tru+(float(model_dictionary[word][0]))
                prob_dec = prob_dec+(float(model_dictionary[word][1]))
                prob_pos = prob_pos+(float(model_dictionary[word][2]))
                prob_neg = prob_neg+(float(model_dictionary[word][3]))
            
       
       
        if(prob_tru > prob_dec):
            output = key+" truthful"
        else:
            output = key+" deceptive"
        if(prob_pos > prob_neg):
            output = output+" positive"
        else:
            output = output+" negative"
        nboutput.write(output+"\n")
nboutput.close()
   



         
