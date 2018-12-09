# Spam-Classification-Using-Naive-Bayes

Command:
python q2_classifier.py --f1 train --f2 test --o output.csv


Output:

Training Set Metrics :

total_words_in_ham : 511369.0
total_words_in_spam : 618110.0
total_words : 1129479.0
total_unique_words_in_spam : 983.0
total_unique_words_in_ham : 1000.0
probability of spam : 0.547252317219
probability of ham : 0.452747682781

Test Set Metrics :

Number of emails correctly classified : 868
Total emails classified : 1000
Accuracy is : 86.8 %
Precision is : 90.8759124088 %
Recall is : 85.8620689655 %


Parameters Used to improve accuracy:

1. Laplace Smoothing (alpha=1) is used to assign a small probability instead of zero to words in test set not present in dictionary. This improved the accuracy.

2. To compute the product of conditional probabilities, sum of log of individual conditional probability is used. This also improved the accuracy.
