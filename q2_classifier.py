# -*- coding: utf-8 -*-
"""    
Usage: python q2_classifier.py -f1 <train_dataset> -f2 <test_dataset> -o <output_file>
"""

import argparse, sys
import numpy as np

#Command Line Arguments
parser=argparse.ArgumentParser(description="Classify email as spam or ham")

parser.add_argument('--f1', help='file name of train dataset')
parser.add_argument('--f2', help='file name of test dataset')
parser.add_argument('--o', help='output file name')

args=parser.parse_args()

args_dict = vars(args)
train_file = args_dict['f1']
test_file = args_dict['f2']
output_file = args_dict['o']

#initilization of counters and variables
freq={}
total_words_in_spam = 0.0
total_words_in_ham = 0.0
total_spam_emails = 0.0
total_ham_emails = 0.0
total_emails = 0.0
total_words = 0.0
alpha=1
total_unique_words_in_spam = 0.0
total_unique_words_in_ham = 0.0

#parse each line of train dataset where each line is an email  
with open(train_file) as fp:  
  line = fp.readline()
  cnt = 1
  while line:
    words = line.split(' ')    
    length = len(words)
    total_emails += 1 
    
    #if current email is labelled as ham
    if words[1]=='ham':        
        total_ham_emails += 1
    else:        
      total_spam_emails += 1
      
    i = 2
    while i < length:
      total_words += 1      
      key = (words[1],words[i]) #key is a tuple. eg : (spam,free), (spam,prize), (ham,hello), (ham,meeting)
      val = words[i+1]
      if key not in freq:
        freq[key] = float(val)
        if words[1]=='ham': #if this is new word not present in dictionary
            total_unique_words_in_ham += 1
        else:
            total_unique_words_in_spam += 1
      else:
        freq[key] += float(val)
      if words[1]=='ham':
        total_words_in_ham += 1        
      else:
        total_words_in_spam += 1        
      i+=2    
    
    line = fp.readline()
    cnt += 1

print "\nTraining Set Metrics : "    
print "total_words_in_ham : ",total_words_in_ham
print "total_words_in_spam : ", total_words_in_spam
print "total_words : ", total_words
print "total_unique_words_in_spam : ",total_unique_words_in_spam
print "total_unique_words_in_ham : ",total_unique_words_in_ham

prob_spam = float(float(total_words_in_spam) / float(total_words))
prob_ham = 1 - prob_spam

print "probability of spam : ",prob_spam
print "probability of ham : ",prob_ham

#Returns log( P(words|spam) ) + log( P(spam) )
def get_spam_probability(words):  
  i=2
  length = len(words)
  prob_product = float(1.0)
  prob_product += np.log10(prob_spam)
  while i<length:
    key = ('spam',words[i]) # eg: key : (spam,free)
    if key in freq:
        val = float(freq[key])
        #Since probabilities are small quantities, we take sum of logs instead of direct multiplication as it ensures better precision.
        prob_product += np.log10(float(val/float(total_words_in_spam)))*float(words[i+1])
    else:
        #Laplace Smoothing : Assigning a small probability instead of 0 to words which are not present in dictionary
        prob_product += np.log10(alpha / float(total_words_in_spam + total_unique_words_in_spam*alpha))    
    i+=2  
  return prob_product

#Returns log( P(words|ham) ) + log( P(ham) )
def get_ham_probability(words):  
  i=2
  length = len(words)
  prob_product = float(1.0)
  prob_product += np.log10(prob_ham)
  while i<length:
    key = ('ham',words[i]) # eg: key : (ham,hello)
    if key in freq:
        val = float(freq[key])
        #Since probabilities are small quantities, we take sum of logs instead of direct multiplication as it ensures better precision.
        prob_product += np.log10(float(val/float(total_words_in_ham)))*float(words[i+1])
    else:
        #Laplace Smoothing : Assigning a small probability instead of 0 to words which are not present in dictionary
        prob_product += np.log10(alpha / float(total_words_in_ham + total_unique_words_in_ham*alpha))
    i+=2
  return prob_product
  
#init of mttrics
correct = 0
total = 0  
actual_ham = 0
actual_spam = 0
correct_pred_spam = 0
correct_pred_ham = 0
total_pred_spam = 0
total_pred_ham = 0

fp_pred = open(output_file,"w")

with open(test_file) as fp:  
  line = fp.readline()
  cnt = 1
  while line:
    words = line.split(' ')
    total_emails += 1
    actual_label = words[1]
    if actual_label=='spam':
        actual_spam += 1
    else:
        actual_ham += 1
    p_spam = get_spam_probability(words)
    p_ham = get_ham_probability(words)
    if p_spam > p_ham:
      predicted_label = 'spam'      
      fp_pred.write(words[0]+", spam"+"\n")      
      total_pred_spam += 1
    else:
      predicted_label = 'ham'
      fp_pred.write(words[0]+", ham"+"\n")      
      total_pred_ham += 1
    if predicted_label == actual_label:
      correct += 1
      if actual_label == 'spam':
        correct_pred_spam += 1
      else:
        correct_pred_ham += 1
    total += 1         
    line = fp.readline()
    cnt += 1
    
fp_pred.close()
print "\n\nTest Set Metrics : "
print "Number of emails correctly classified : ",correct
print "Total emails classified : ", total
print "Accuracy is : ", float(correct*1.0/total * 100.0), "%"
print "Precision is : " , float(correct_pred_spam*1.0/total_pred_spam)*100,"%"
print "Recall is : ", float(correct_pred_spam*1.0/actual_spam)*100,"%"