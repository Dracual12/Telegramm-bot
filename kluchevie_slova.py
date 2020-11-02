from collections import OrderedDict
import numpy as np
import spacy
from nltk.corpus import stopwords

nlp = spacy.load('en_core_web_sm')

stop_words = stopwords.words('russian')
class TextRank4Keyword():
    """Extract keywords from text"""

    def __init__(self):
        self.d = 0.85  # damping coefficient, usually is .85
        self.min_diff = 1e-5  # convergence threshold
        self.steps = 10  # iteration steps
        self.node_weight = None  # save keywords and its weight

    def set_stopwords(self, stopwords):
        """Set stop words"""
        for word in stop_words:
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True

    def sentence_segment(self, doc, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences

    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab

    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i + 1, i + window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs

    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())

    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1

        # Get Symmeric matrix
        g = self.symmetrize(g)

        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm != 0)  # this is ignore the 0 element in norm

        return g_norm

    def get_keywords(self, number=10):
        """Print top number keywords"""
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            print(key + ' - ' + str(value))
            if i > number:
                break

    def analyze(self, text,
                candidate_pos=['NOUN', 'PROPN'],
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""

        # Set stop words
        self.set_stopwords(stopwords)

        # Pare text by spaCy
        doc = nlp(text)

        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower)  # list of list of words

        # Build vocabulary
        vocab = self.get_vocab(sentences)

        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)

        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)

        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))

        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1 - self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr)) < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]

        self.node_weight = node_weight


"""text = 'The Wandering Earth, described as China’s first big-budget science fiction thriller, quietly made it onto ' \
       'screens at AMC theaters in North America this weekend, and it shows a new side of Chinese filmmaking — ' \
       'one focused toward futuristic spectacles rather than China’s traditionally grand, massive historical epics.' \
       ' At the same time, The Wandering Earth feels like a throwback to a few familiar eras of American filmmaking.' \
       ' While the film’s cast, setting, and tone are all Chinese, longtime science fiction fans are going to see a ' \
       'lot on the screen that reminds them of other movies, for better or worse.'
       
science - 1.798260689279155
fiction - 1.7791314730093135
China - 1.4462558888396955
Earth - 1.4059858425980583
filmmaking - 1.1017439574314576
tone - 1.1013378017184836
fans - 1.1013378017184836
Wandering - 1.0937062139249636
budget - 1.049677380542437
North - 1.0467124368686869
theaters - 1.005387626262626
AMC - 1.0015524235865145
"""

"""text = 'Of course, you can directly download en_core_web_sm, using the command: python -m spacy download en_core_web_' \
       'sm, or you can even link the name en to other models as well. For example, you could do python -m spacy ' \
       'download en_core_web_lg and then python -m spacy link en_core_web_lg en. That would make en a name for en_core_' \
       'web_lg, which is a large spaCy model for the English language.'
download - 1.889948390151515
spacy - 1.409694365530303
python - 1.389667850378788
en_core_web_sm - 1.0096349431818181
en_core_web_lg - 1.0
model - 1.0
language - 1.0
en - 0.826880918560606
-m - 0.8243655303030303
command - 0.6696590909090909
link - 0.6696590909090909
example - 0.6562450284090909"""
text = 'Публикация очередного рейтинга РИА Новости побудила меня на написание своего отзыва. Этот своего рода взгляд' \
       ' в прошлое, потому что все оценки "по горячим следам" мне кажутся бессмысленными, нет жизненного опыта. Я ' \
       'закончил факультет КиБ (наверное Институт интеллектуальных киберентических систем и есть КиБ, но эта смена' \
       ' названий откровенно странная) в 2013 году. И ребятушки, конечно МИФИ раем не назовёшь. Преподы жесткие, халява' \
       ' скорее редкость, чем практика, первые два года учёбы - вообще тотальный ад. Потом становится попроще, ' \
       'возможно, в силу того, что предметы начинаются профильные, а не абы какие. Но и с профильными тоже не просто.' \
       ' Рыбина - вообще на все времена отпечаталась в моей голове, как самый худший кошмар, причём кошмар бесполезный.' \
       ' Но зато после окончания оказывается, что ты умеешь самое главное - думать. У тебя есть логика, которая ' \
       'позволяет рассуждать лучше и качественнее большинства. Ты можешь освоить любой язык программирования, хотя ' \
       'казалось бы, на предметах сами по себе языки практически не учили. Когда я учился, в аудиториях было холодно, ' \
       'ремонт убогий, вай-фай - не слышали о таком. Был на встрече выпускников в сентября - совсем другой университет.' \
       ' Окна - пластиковые, оформление и дизайн появились, регистрация по номеру телефона в сети вай-фай и без рекламы.' \
       ' Нет, это конечно не определяющее, но внутренние ощущения кардинально отличаются от момента окончания. Видно, ' \
       'что в универ вкладываются. И смотря на своё образование, я понимаю почему. Жалко только одно. Рыбина всё ещё ' \
       'на месте и всё так же гробит в студентах любое желание учится. В общем, я спустя 5 лет после выпуска могу точно' \
       ' сказать - МИФИ того стоит. Единственное, что меня напрягает, это бешенный пиар какой-то, а также создание' \
       ' нового по принципу переименования старого. А ещё нет нормальной ассоциации выпускников. Ну может всему своё ' \
       'время, не знаю...'
tr4w = TextRank4Keyword()
tr4w.analyze(text, candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
tr4w.get_keywords(10)
