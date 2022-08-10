their_greetings = ['hi', 'hello', 'good morning']
my_greetings = ['Hi!', 'Hello!', 'Good morning!']
their_howareyou = ['How are you?', 'How are you doing?', 'Whats up?']
my_howareyou = ['I am good, thank you', 'Thanks, I am fine']
their_goodbyes = ['goodbye', 'bye', 'good-bye', 'see you later', 'cya']
my_goodbyes = ['Goodbye!', 'Bye!']
my_confusion = ['Can you rephrase that please?', 'Sorry, I did not understand that query, could you rephrase?']
their_score = ['score', 'rating', 'grade', 'average', 'socre', 'ratings', 'averge', 'avearge']
my_score = ['The score for that movie is {}']
their_recommendation = ['recommend', 'recommendation', 'suggest', 'suggestion', 'propose', 'advise','reccomend', 'similar']
my_recommendation = ['My recommendations for similar movies are {}', 'You might also like {}']
their_review = ['review', 'opinion', 'impression', 'view', 'think', 'opionion', 'veiws']
my_review = ['{}']

questions_answers = [(their_greetings, my_greetings),
                     (their_goodbyes, my_goodbyes),
                     (their_score, my_score),
                     (their_recommendation, my_recommendation),
                     (their_review, my_review),
                     (their_howareyou, my_howareyou)]

recommendation = ['Could you recommend me a movie similar to movie?',
                  'Do you have any suggestions for me?', 'Do you have any recommendations?',
                  'Can you advise me a movie?', 'I need your advice', 'Do you have any recommendations for this movie?',
                  'Do you know any movie similar to this?', 'Do you know something similar to this movie?', 'What would you recommend?',
                  'What could you recommend?', 'Which film could you recommend me?']
score = ['What is the movie rating?', 'What is the movie score?', 'How was the movie scored?']
review = ['What is your opinion on this movie?', 'What is your impression?', 'What do you think about the movie?',
          'What is your point of view on this movie?', 'Can you give me a movie review?', 'Could you give me the review?',
          'Could you share the review for this film?']
