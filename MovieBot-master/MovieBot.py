# -*- coding: utf-8 -*-

import sys
import random
import ujson

import telebot
from telebot import types

from gensim.models import KeyedVectors

from MovieBot.find_title import find_title
from MovieBot.intent import phrases
from MovieBot.intent.find_intent import IntentFinder
from MovieBot.intent.phrases import questions_answers
from MovieBot.utils.normalization import normalize
from MovieBot.config import telebot_config, tmdb_config

import tmdbsimple as tmdb

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Set up Telegram bot
bot = telebot.TeleBot(telebot_config)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row('/info')

# Set up tmdb
tmdb.API_KEY = tmdb_config
search = tmdb.Search()

# Load data
movie_names = open('./MovieBot/data/movie_names.txt', 'r').read().split('\n')
movie_db = ujson.load(open('./MovieBot/data/amazon_movies.json', 'r'))

# Load embeddings
model = KeyedVectors.load_word2vec_format('./MovieBot/embeddings/GoogleNews-vectors-negative300.bin', binary=True)

intent_finder = IntentFinder(model)

print("Bot started")

@bot.message_handler(commands=['start'])
def send_message(message):
    bot.send_message(message.chat.id, "You can ask me about your favorite movie review score, recommendations for other movies or a sample review!", reply_markup=markup)


@bot.message_handler(commands=['info'])
def send_message(message):
    bot.send_message(message.chat.id, "You can ask me about your favorite movie review score, recommendations for other movies or a sample review!", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def respond(message):
    text = message.text

    movie = find_title(text, movie_names)
    logging.debug('Extracted movie: {}'.format(movie))

    # Normalize text
    clean_text = normalize(text)  # for intent
    logging.debug('Clean text: {}'.format(clean_text))

    # Calculate Intent
    extracted_intent = intent_finder.model_distance(clean_text)
    logging.debug('Calculated intent: {}'.format(extracted_intent))
    response = None
    if extracted_intent == 'greetings':
        response = random.choice(phrases.my_greetings)

    elif extracted_intent == 'goodbyes':
        response = random.choice(phrases.my_goodbyes)

    elif extracted_intent == 'howareyou':
        response = random.choice(phrases.my_howareyou)

    elif extracted_intent == 'review':
        if not movie:
            response = "I do not know about that movie."
        else:
            print('Review')
            response = random.choice(movie_db[movie]['review'])[2]

    elif extracted_intent == 'score':
        if not movie:
            response = "I do not know about that movie."
        else:
            print('Score')

            logging.debug('Score:')
            search = tmdb.Search()
            query = search.movie(query=movie)

            first = query['results'][0]

            popularity = first['vote_average']
            response = random.choice(phrases.my_score).format(popularity)
            logging.debug('Popularity: {}'.format(popularity))
            logging.debug('{} {} {}'.format(first['title'], first['id'], first['release_date']))

    elif extracted_intent == 'recommendation':
        if not movie:
            response = "Sorry, I do not know about that movie."
        else:
            logging.debug('Recommendation:')
            search = tmdb.Search()
            query = search.movie(query=movie)
            first = query['results'][0]
            tmdb_movie = tmdb.Movies(first['id'])
            print(tmdb_movie)
            if tmdb_movie.recommendations()['total_results'] != 0:
                print(random.choice(phrases.my_recommendation).format(tmdb_movie.recommendations()))
                print(random.choice(tmdb_movie.recommendations()['results'])['title'])
                response = random.choice(phrases.my_recommendation).format(random.choice(tmdb_movie.recommendations()['results'])['title'])
                logging.debug('Other films: {}'.format(random.choice(tmdb_movie.recommendations()['results'])['title']))
            else:
                response = "Sorry, I don't have recommendations for this movie"
    else:
        response = random.choice(phrases.my_confusion)

    bot.send_message(message.chat.id, response)

if __name__ == '__main__':
     bot.polling(none_stop=True)
