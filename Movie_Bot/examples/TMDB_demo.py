import tmdbsimple as tmdb
import ujson
from MovieBot.config import telebot_config, tmdb_config

tmdb.API_KEY = tmdb_config

if __name__ == "__main__":
    movie = tmdb.Movies(603)
    response = movie.info()

    print(response['overview'])
    print(movie.title)
    print(movie.budget)
    print(movie.reviews()['results'][0])
    print(len(movie.reviews()['results']))

    print('Recommendations', movie.recommendations())

    with open('recommendation.json', 'w') as w:
        ujson.dump(movie.recommendations(), w)

    response = movie.releases()
    for c in movie.countries:
       if c['iso_3166_1'] == 'US':
            print(c['certification'])

    search = tmdb.Search()
    response = search.movie(query='The Bourne')
    for s in search.results:
        print(s['title'], s['id'], s['release_date'], s['popularity'])

    person = tmdb.People(1)
    print(person.info())
