import nltk
from nltk.corpus import reuters, brown, gutenberg
import re

words = []

for corp in nltk.corpus.gutenberg.fileids():
	print('\t', corp, len(gutenberg.words(corp)))
	words += set(w.lower() for w in gutenberg.words(corp))

# corpus van miljoenen woorden van Reuters en Brown
for corp in [reuters.words(), brown.words()]:
	print('\t', corp, len(corp))
	words += [w.lower() for w in corp]

# alleen vijf letterigen
five_letter_words = list(set([word.lower() for word in words if len(word) == 5]))
word_dict = {}

# karakters vertalen naar cijfers, want lui
for word in five_letter_words:
	word_dict[word] = [ord(letter) for letter in word]

print('We have a database of %i possible five letter words' % len(word_dict))

good_response, finished = False, False

while finished == False:
	# collect guesses and responses and check if they're valid
	while good_response == False:
		print('Please type guess...')
		guess = input()

		print('Please type result of guess (gray = 0, green = 1, yellow = ?)...')
		response = input()

		# check input
		if len(response) != 5 or len(guess) != 5:
			print('\tResponse or guess has wrong length!')
		elif len(re.sub('[01?]', '', response)) != 0:
			print('\tIllegal character in response!')
		else:
			good_response = True

	# evaluate response
	delete = []
	for index, result in enumerate(zip(guess, response)):
		guessed_character, response = result[0], result[1]
		
		if response == '0':
			for word in word_dict:
				# forbidden letter in word: delete
				if ord(guessed_character) in word_dict[word]:
					delete.append(word)
		
		if response == '?':
			for word in word_dict:
				# maybe word not in word: delete
				if ord(guessed_character) not in word_dict[word]:
					delete.append(word)

				# maybe word in word, but on same position: delete
				if word_dict[word][index] == ord(guessed_character): 
					delete.append(word)

		if response == '1':
			for word in word_dict:
				# correct letter not on same position
				if word_dict[word][index] != ord(guessed_character):
					delete.append(word)

	# cull selection
	for d in delete:
		word_dict.pop(d, None)
	
	# print out remaining options
	print('%i options remaining' % len(word_dict))
	print(list(word_dict.keys()))

	# quit if done
	if len(word_dict) == 1:
		print('Correct guess found!')
		finished = True

	# or gather new guess and response
	good_response = False
