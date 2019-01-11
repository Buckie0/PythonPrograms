print 'Welcome to the PygLatin Translator!'
pyg = 'ay'

# Ask the user to input a word.
original = raw_input('Enter a word: ')

# Check that the word contains only letters with no spaces and change to lower
# case.
# Then move the first letter to the end and add "ay"
if len(original) > 0 and original.isalpha():
    word = original.lower()
    first = word[0]
    new_word = word + first + pyg
    new_word = new_word[1:len(new_word)]
    print new_word

# If a character that is not a letter is found or nothing is typed, print the
# below
else:
    print 'Please type a word containing only letters!'
