from gensim.models import KeyedVectors

from phrases import their_ask_score, their_ask_recommendation, their_ask_review

model = KeyedVectors.load_word2vec_format('D:/Data/word2vec/GoogleNews-vectors-negative300.bin', binary=True)

phrases_to_match = [their_ask_score, their_ask_recommendation, their_ask_review]
for p in phrases_to_match:
    for pp in p:
        print("Phrase: {}".format(pp))
        print("Most similar ones:".format(pp))
        most_similar = model.most_similar(pp, topn=10)
        print(most_similar)
