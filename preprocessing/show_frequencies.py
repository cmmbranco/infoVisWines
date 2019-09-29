import nltk
from nltk.collocations import *
from nltk.tokenize import RegexpTokenizer
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import sys
from itertools import tee
from collections import defaultdict
from operator import itemgetter
from math import log

file_content = open("descriptioncorpus.txt").read()
new_words = ["drink","like"]

def standart_text_normalize(source_text, costum_stopwords = []):

    stop_words = set(stopwords.words("english")).union(costum_stopwords)


    #Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', file_content)
     
    #Convert to lowercase
    text = text.lower()
     
    #remove tags
    text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
     
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
     
    ##Convert to list from string
    text = text.split()
     
    ##Stemming
    ##ps=PorterStemmer()
    
    #Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in stop_words]

    finaltext = " ".join(text)

    return finaltext

def pairwise(iterable):
    # from itertool recipies
    # is -> (s0,s1), (s1,s2), (s2, s3), ...
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def l(k, n, x):  # noqa: E743
    # dunning's likelihood ratio with notation from
    # http://nlp.stanford.edu/fsnlp/promo/colloc.pdf p162
    return log(max(x, 1e-10)) * k + log(max(1 - x, 1e-10)) * (n - k)

def score(count_bigram, count1, count2, n_words):
    """Collocation score"""
    if n_words <= count1 or n_words <= count2:
        # only one words appears in the whole document
        return 0
    N = n_words
    c12 = count_bigram
    c1 = count1
    c2 = count2
    p = c2 / N
    p1 = c12 / c1
    p2 = (c2 - c12) / (N - c1)
    score = (l(c12, c1, p) + l(c2 - c12, N - c1, p)
             - l(c12, c1, p1) - l(c2 - c12, N - c1, p2))
    return -2 * score

def process_tokens(words, normalize_plurals=True):
    """Normalize cases and remove plurals.
    Each word is represented by the most common case.
    If a word appears with an "s" on the end and without an "s" on the end,
    the version with "s" is assumed to be a plural and merged with the
    version without "s" (except if the word ends with "ss").
    Parameters
    ----------
    words : iterable of strings
        Words to count.
    normalize_plurals : bool, default=True
        Whether to try and detect plurals and remove trailing "s".
    Returns
    -------
    counts : dict from string to int
        Counts for each unique word, with cases represented by the most common
        case, and plurals removed.
    standard_forms : dict from string to string
        For each lower-case word the standard capitalization.
    """
    # words can be either a list of unigrams or bigrams
    # d is a dict of dicts.
    # Keys of d are word.lower(). Values are dicts
    # counting frequency of each capitalization
    d = defaultdict(dict)
    for word in words:
        word_lower = word.lower()
        # get dict of cases for word_lower
        case_dict = d[word_lower]
        # increase this case
        case_dict[word] = case_dict.get(word, 0) + 1
    if normalize_plurals:
        # merge plurals into the singular count (simple cases only)
        merged_plurals = {}
        for key in list(d.keys()):
            if key.endswith('s') and not key.endswith("ss"):
                key_singular = key[:-1]
                if key_singular in d:
                    dict_plural = d[key]
                    dict_singular = d[key_singular]
                    for word, count in dict_plural.items():
                        singular = word[:-1]
                        dict_singular[singular] = (
                            dict_singular.get(singular, 0) + count)
                    merged_plurals[key] = key_singular
                    del d[key]
    fused_cases = {}
    standard_cases = {}
    item1 = itemgetter(1)
    for word_lower, case_dict in d.items():
        # Get the most popular case.
        first = max(case_dict.items(), key=item1)[0]
        fused_cases[first] = sum(case_dict.values())
        standard_cases[word_lower] = first
    if normalize_plurals:
        # add plurals to fused cases:
        for plural, singular in merged_plurals.items():
            standard_cases[plural] = standard_cases[singular.lower()]
    return fused_cases, standard_cases

def unigrams_and_bigrams(words, normalize_plurals=True):
    n_words = len(words)
    # make tuples of two words following each other
    bigrams = list(pairwise(words))
    counts_unigrams, standard_form = process_tokens(
        words, normalize_plurals=normalize_plurals)
    counts_bigrams, standard_form_bigrams = process_tokens(
        [" ".join(bigram) for bigram in bigrams],
        normalize_plurals=normalize_plurals)
    # create a copy of counts_unigram so the score computation is not changed
    counts = counts_unigrams.copy()

    # decount words inside bigrams
    for bigram_string, count in counts_bigrams.items():
        bigram = tuple(bigram_string.split(" "))
        # collocation detection (30 is arbitrary):
        word1 = standard_form[bigram[0].lower()]
        word2 = standard_form[bigram[1].lower()]

        if score(count, counts[word1], counts[word2], n_words) > 30:
            # bigram is a collocation
            # discount words in unigrams dict. hack because one word might
            # appear in multiple collocations at the same time
            # (leading to negative counts)
            counts_unigrams[word1] -= counts_bigrams[bigram_string]
            counts_unigrams[word2] -= counts_bigrams[bigram_string]
            counts_unigrams[bigram_string] = counts_bigrams[bigram_string]
    words = list(counts_unigrams.keys())
    for word in words:
        # remove empty / negative counts
        if counts_unigrams[word] <= 0:
            del counts_unigrams[word]
    return counts_unigrams

def process_text(text, word_length = 0):
    
        flags = (re.UNICODE if sys.version < '3' and type(text) is unicode  # noqa: F821
                 else 0)
        regexp = r"\w[\w']+"

        words = re.findall(regexp, text, flags)

        # remove 's
        words = [word[:-2] if word.lower().endswith("'s") else word
                 for word in words]
        
        # remove short words
        if word_length:
            words = [word for word in words if len(word) >= word_length]

        word_counts = unigrams_and_bigrams(words, True)

        return word_counts

finaltext = standart_text_normalize(file_content,new_words)

counts = process_text(finaltext)

x = counts
sorted_x = sorted(x.items(), key=lambda kv: kv[1])

for row in sorted_x[::-1] :
    print( row )

#bigram_measures = nltk.collocations.BigramAssocMeasures()
#trigram_measures = nltk.collocations.TrigramAssocMeasures()


#tokens = nltk.wordpunct_tokenize(finaltext)
#finder = BigramCollocationFinder.from_words(tokens)
#scored = finder.score_ngrams(bigram_measures.raw_freq)
#r = sorted(bigram for bigram, score in scored)

#print(r)

#Word cloud

#from os import path
#from PIL import Image
#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#import matplotlib.pyplot as plt
#% matplotlib inline
#wordcloud = WordCloud(
#                      background_color='white',
#                      stopwords=[],
#                      max_words=1000,
#                      max_font_size=50,
#                      random_state=42
#                      ).generate(finaltext)
#print(wordcloud)
#fig = plt.figure(1)
#plt.imshow(wordcloud)
#plt.axis('off')
#plt.show()
#fig.savefig("word1.png", dpi=2000)


