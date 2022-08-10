import numpy as np
import sys
from sklearn.metrics.pairwise import cosine_similarity

from MovieBot.intent import phrases
from MovieBot.utils.normalization import normalize


class IntentFinder():
    def __init__(self, model=None):
        if model != None:
            self.model = model
            their_greetings = ['hi', 'hello', 'good morning']
            their_goodbyes = ['goodbye', 'bye', 'good-bye', 'see you later', 'cya']
            their_howareyou = ['How are you?', 'How are you doing?', 'Whats up?']

            their_recommendation = ['Could you recommend me a movie similar to movie?', 'Do you have any suggestions for me?',
                              'Do you have any recommendations?',
                              'Can you advise me a movie?', 'I need your advice']
            their_score = ['What is the movie rating?', 'What is the movie score?', 'How was the movie scored?']
            their_review = ['What is your opinion on this movie?', 'What is your impression?',
                      'What do you think about the movie?',
                      'What is your point of view on this movie?', 'Can you give me a movie review?']

            self.types = {}
            self.types['greetings'] = their_greetings
            self.types['goodbyes'] = their_goodbyes
            self.types['howareyou'] = their_howareyou
            self.types['score'] = their_score
            self.types['recommendation'] = their_recommendation
            self.types['review'] = their_review

            # Create vectors
            self.types_vectors = self.get_vectors(self.types)

    def get_vectors(self, train):
        """ Creates dictionary of vectors for each intent. """
        vectors = {}
        for k in train:
            clean_train_reviews = []
            for review in train[k]:
                clean_train_reviews.append(normalize(review).split())

            trainDataVecs = self.getAvgFeatureVecs(clean_train_reviews, self.model, self.model.vector_size)

            vectors[k] = trainDataVecs
        return vectors

    def model_distance(self, message, treshold_distance=0.7):
        """ Takes message as input and returns the most probable intent type. """
        if message == '':
            return False
        else:
            message_vec = self.makeFeatureVec(message.split(), self.model, self.model.vector_size)  # do normalization of input vector?
            intent_scores = {}

            # For each intent
            for intent_name in self.types:
                intent_score = 0
                # For each example intent
                for intent_vector in self.types_vectors[intent_name]:
                    # Calculate the distance between the message and example intent
                    score = 1 - cosine_similarity(message_vec.reshape(1, -1), intent_vector.reshape(1, -1))
                    print(score)

                    # increase intent score if smaller than 0.7
                    if float(score) < treshold_distance:
                        intent_score += 1    # do normalization by length
                intent_scores[intent_name] = intent_score / len(self.types_vectors[intent_name])

            for i in intent_scores:
                print(i, intent_scores[i])

            # Choose intent with the highest score
            # If the score is too small - ask the user to rephrase the query
            print(max(intent_scores, key=intent_scores.get))
            if intent_scores[max(intent_scores, key=intent_scores.get)] > 0.2:
                return max(intent_scores, key=intent_scores.get)
            return False

    def makeFeatureVec(self, words, model, num_features):
        # Function to average all of the word vectors in a given
        # paragraph

        # Pre-initialize an empty numpy array (for speed)
        featureVec = np.zeros((num_features,), dtype="float32")

        nwords = 0

        # Index2word is a list that contains the names of the words in
        # the model's vocabulary. Convert it to a set, for speed
        index2word_set = set(model.index2word)

        # Loop over each word in the review and, if it is in the model's
        # vocaublary, add its feature vector to the total
        for word in words:
            if word in index2word_set:
                nwords = nwords + 1
                featureVec = np.add(featureVec, model[word])

        # Divide the result by the number of words to get the average
        featureVec = np.divide(featureVec, nwords)
        return featureVec

    def getAvgFeatureVecs(self, message, model, num_features):
        # Given a set of reviews (each one a list of words), calculate
        # the average feature vector for each one and return a 2D numpy array

        # Initialize a counter
        counter = 0

        # Preallocate a 2D numpy array, for speed
        reviewFeatureVecs = np.zeros((len(message), num_features), dtype="float32")

        # Loop through the reviews
        for review in message:

            # Print a status message every 1000th review
            if counter % 1000 == 0:
                print("Review %d of %d" % (counter, len(message)))

            # Call the function (defined above) that makes average feature vectors
            reviewFeatureVecs[counter] = self.makeFeatureVec(review, model, num_features)

            # Increment the counter
            counter = counter + 1
        return reviewFeatureVecs
