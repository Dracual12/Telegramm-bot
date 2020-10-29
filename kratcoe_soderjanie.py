import re
import heapq
import nltk
from nltk.corpus import stopwords

text = 'Некоторые считают, что человек взрослеет в каком-нибудь определённом возрасте, например, в 18 лет, когда ' \
       'он становится совершеннолетним. Но есть люди, которые и в более старшем возрасте остаются детьми. Что же' \
       ' значит быть взрослым?Взрослость означает самостоятельность, то есть умение обходиться без чьей-либо помощи,' \
       ' опеки. Человек, обладающий этим качеством, всё делает сам и не ждёт поддержки от других. Он понимает, что' \
       ' свои трудности должен преодолевать сам. Конечно, бывают ситуации, когда человеку одному не справиться.' \
       ' Тогда приходится просить помощи у друзей, родственников и знакомых. Но в целом, самостоятельному, ' \
       'взрослому человеку не свойственно надеяться на других.Есть такое выражение: руке следует ждать помощи ' \
       'только от плеча. Самостоятельный человек умеет отвечать за себя, свои дела и поступки. Он сам планирует' \
       ' свою жизнь и оценивает себя, не полагаясь на чьё-то мнение. Он понимает, что многое в жизни зависит от' \
       ' него самого. Быть взрослым - значит отвечать за кого-то ещё. Но для этого тоже надо стать самостоятельным,' \
       ' уметь принимать решения. Взрослость зависит не от возраста, а от жизненного опыта, от стремления прожить' \
       ' жизнь без нянек.'
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

# взвешенная гистограмма
for key in word2count.keys():
    word2count[key] = word2count[key] / max(word2count.values())

best_three_sentences = heapq.nlargest(5, sent2score, key=sent2score.get)
print(*best_three_sentences)
