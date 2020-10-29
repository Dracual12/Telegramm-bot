import requests
from bs4 import BeautifulSoup
import nltk

nltk.download('punkt')
from nltk import word_tokenize
from nltk.corpus import stopwords
from random import choice, sample
from string import punctuation


def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf8'
    return r.text


def get_head(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup


link = 'https://tabiturient.ru/vuzu/mifi/'
site_name = get_html(link)
site_data = get_head(site_name)
head = site_data.find('div').find_all(style="text-align:justify;", class_='font2')
heads = []
for i in head:
    heads.append(i.string)
heads = [e for e in heads if e is not None]
print(heads[0])

words = word_tokenize(heads[0])
words_no_punc = []
for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())
print(words_no_punc)

stopwords = stopwords.words('russian')
clean_words = []
for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)
print(clean_words)

s = clean_words


def generatetext():
    global s
    s1 = list(filter(lambda x: x not in punctuation, s))
    s2 = ((' '.join((sample(s1, choice(range(5, 20)))))).lower()).split()
    for i in s2:
        s2.insert(0, i[0].upper() + i[1:])
        break
    s2.remove(s2[1])
    for i in s2:
        if s2.count(i) != 1:
            del s2[' '.join(s2).rfind(i)]
    return ' '.join(s2) + '.'


def main():
    a = 5
    for i in range(a):
        flag = True
        while flag:
            try:
                print(generatetext())
                flag = False
            except IndexError:
                s = words


main()
