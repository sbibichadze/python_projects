import random
import string

with open('words_hangman.txt') as f:
    words = f.readlines()

words = [word.rstrip('\n').strip() for word in words]
word = random.choice(words)
alphabet = set(string.ascii_lowercase)
unique_letters = set(word)
used_letters = []
moves = 0
life = 10
result = ''.join(['_' for _ in word])

while True:
    print(f'used letters {used_letters}')
    print('word to guess ' + ''.join([f'{l} ' for l in result]))
    print(f'lives: {life}')
    print('_'*(2*(len(result))+13))
    if len(unique_letters) < 1:
        print(f'game finished in {moves} moves')
        print('congrats')
        break
    if life < 1:
        print('you lost')
        break
        
    guess = input("Enter your guess: ")

    if guess not in alphabet:
        print('invalid input try again!')
    elif guess in used_letters:
        print('already used that letter')
    elif guess in unique_letters:
        print('good guess')
        result = ''.join([guess if guess == word[i] else result[i] for i in range(len(word))])
        unique_letters.remove(guess)
        
        used_letters.append(guess)
        moves += 1
    else:
        print('wrong guess')
        life -= 1
        used_letters.append(guess)
        moves += 1




