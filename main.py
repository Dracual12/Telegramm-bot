import re
import heapq
import nltk
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup

nltk.download('stopwords')


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

text = ''
for e in heads:
    text += e
sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
clean_text = text.lower()
word_tokenize = clean_text.split()

stop_words = set(stopwords.words('russian'))

word2count = {}
for word in word_tokenize:
    if word not in stop_words:
        if word not in word2count.keys():
            word2count[word] = 1
        else:
            word2count[word] += 1
sent2score = {}
for sentence in sentences:
    for word in sentence.split():
        if word in word2count.keys():
            if 28 > len(sentence.split(' ')) > 9:
                if sentence not in sent2score.keys():
                    sent2score[sentence] = word2count[word]
                else:
                    sent2score[sentence] += word2count[word]

for key in word2count.keys():
    word2count[key] = word2count[key] / max(word2count.values())

best_three_sentences = heapq.nlargest(5, sent2score, key=sent2score.get)
print(*best_three_sentences)
