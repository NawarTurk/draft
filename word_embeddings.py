# pip install gensim
# Run this in the terminal and do not include it in the code if you are using an IDE

# pip show gensim
# Use it to make sure that you have downloaded Gensim library properly

import gensim.downloader as api
import json
import random

models = {
    "word2vec-google-news-300": None, 
    "glove-wiki-gigaword-300": None,  # trained on Wikipedia + Gigaword.
    "fasttext-wiki-news-subwords-300": None,  # trained on Common Crawl.
    "glove-twitter-50": None,  # trained on a dataset composed of tweets. 
    "glove-twitter-25": None  # trained on a dataset composed of tweets. 
}

for model_name in models.keys():
  models[model_name] = api.load(model_name)
  print(f'{model_name} has been successfylly downloaded')


with open('data_set/synonym.json', 'r') as file:
  data_set = json.load(file)

with open('analysis.csv', 'w') as file:
  file.write('Model Name,Size of Vocabulary,#Correct Labels,Model Accuracy\n')

model_stats = {}

for model_name, model in models.items():
  with open(f'{model_name}-details.csv', 'w') as file:
    file.write("#,question_word,correct_answer_word,system_guess_word,label\n")
    i = 1
    correct_guesses_counter = 0
    wrong_guesses_counter = 0

    for entry in data_set:
      question_word = entry["question"]
      choices = entry["choices"]
      correct_answer_word = entry["answer"]
      label = "guess"
      similarities = {}

      if question_word in model:
        for choice in choices:
          if choice in model:
            similarities[choice] = model.similarity(question_word, choice)
        if  len(similarities) > 0:
          system_guess_word = max(similarities, key=similarities.get)
          if system_guess_word == correct_answer_word:
            label = 'correct'
            correct_guesses_counter += 1
          else:
            label = 'wrong'
            wrong_guesses_counter += 1

      if label == 'guess':
        system_guess_word = random.choice(choices)

      file.write(f"{i},{question_word},{correct_answer_word},{system_guess_word},{label}\n")
      i+=1
  print(f'{model_name}-details.csv has been sucessfully generated')


  vocab_size = len(model.key_to_index)
  model_accuracy = 0
  if (correct_guesses_counter + wrong_guesses_counter) > 0:
    model_accuracy = correct_guesses_counter / (correct_guesses_counter + wrong_guesses_counter) 

  model_stats[model_name] = {"accuracy": model_accuracy, "total_model_guesses": correct_guesses_counter + wrong_guesses_counter} # for analyzing the data later

  with open('analysis.csv', 'a') as file:
    file.write(f'{model_name},{vocab_size},{correct_guesses_counter},{model_accuracy*100:.1f}%\n')

print(f'The analysis.csv has been sucessfully generated')
