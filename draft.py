import json
from difflib import get_close_matches

data = json.load(open("data.json"))

def translate(word):
    word = word.lower() # making all the word fully into lowercase
    if word in data:
	    return data[word]
    elif w.title() in data: #if user entered "texas" this will check for "Texas" as well.
        return data[w.title()]
    elif w.upper() in data:   #If any user enters words such as USA and so on.
        return data[w.upper()]

    elif len(get_close_matches(word, data.keys())) > 0:

        check = input("Sorry, did you mean %s? Enter Y if yes, or N if no: " % get_close_matches(word, data.keys())[0])
        if (check == "Y" or "y"): return data[get_close_matches(word, data.keys())[0]]

        elif (check == "N" or "y"): return "Sorry the word you're looking for doesn't exist!"

        else: return "I did not understand the word you entered!"

    else: return "Sorry the word you're looking for doesn't exist!"

user = input("Please Enter your word: ",)

meaning_of_word = translate(user)

if (type(meaning_of_word) == list):
    for item in meaning_of_word:  # only lists
        print(item)
else:
print(translate(user))   # only the single meaning words.
