# 6.0001 Problem Set 3
# The 6.0001 Word Game

import math
import random
import os

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


# WORDLIST_FILENAME = "words.txt"
dir_path = os.path.dirname(os.path.realpath(__file__))
WORDLIST_FILENAME = dir_path + "/" + "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

def get_word_score(word:str, n:int):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    word = word.lower()
    # First component: sum of the values of each letter used
    comp1 = sum([(SCRABBLE_LETTER_VALUES[letter]) for letter in word])
    # Second componen​t: the special computation that rewards 
    # a player for playing a longer word, and penalizes them 
    # for any left over letters.
    comp2 = max(1, 7 * len(word) - 3 * (n - len(word)))
    return comp1 * comp2


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    returns a string
    """
    
    display = list()

    for letter in hand.keys():
        for j in range(hand[letter]):
            display.append(letter)
    return ' '.join(display)


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    hand['*'] = 1

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Update a hand by removing letters
#
def update_hand(hand:dict, word:str):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    word = word.lower()
    new_hand = hand.copy()
    for letter in word:
        new_hand[letter] =  new_hand.get(letter, 0) - 1
    # filter out elements in dictionary if value <= 0
    new_hand = dict(filter(lambda elem: elem[1] > 0, new_hand.items()))
    return new_hand


#
# Test word validity
#
def is_valid_word(word:str, hand:dict, word_list:list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    
    word = word.lower()
    word_in_word_list = word in word_list
    if '*' in word:
        for letter in VOWELS:
            guess_word = word.replace('*', letter)
            if guess_word in word_list:
                word_in_word_list = True
                break
    word_dict = get_frequency_dict(word)
    word_in_hand = all(word_dict[k] <= hand.get(k, 0) for k in word_dict.keys())
    return word_in_word_list and word_in_hand


def calculate_handlen(hand:dict):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return sum(hand.values())

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    score = 0
    while calculate_handlen(hand) > 0:
        print('\nCurrent Hand:', display_hand(hand))
        word = input('Please enter word, or "!!" to indicate that you are finished: ')
        
        if word == '!!':
            print('Total score for this hand:', score, 'points')
            break
        
        if is_valid_word(word, hand, word_list):
            score += get_word_score(word, calculate_handlen(hand))
            print('"' + word + '" earned', \
            get_word_score(word,calculate_handlen(hand)), \
            'points. Total:', score, 'points')
        else:
            print('That is not a valid word. Please choose another word.')
        
        hand = update_hand(hand, word)
    
    if calculate_handlen(hand) == 0:
        print('\nRan out of letters. \nTotal score for this hand:', 
        score, 'points\n----------')
    
    return score
            


def substitute_hand(hand:dict, letter:str):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    
    letters_pool = VOWELS + CONSONANTS
    letters_pool = letters_pool.replace(letter, '')
    for l in hand.keys():
        letters_pool = letters_pool.replace(l, '')
    new_letter = random.choice(letters_pool)
    if letter in hand.keys():
        new_hand = hand.copy()
        x = hand[letter]
        new_hand[new_letter] = x
        del new_hand[letter]
        return new_hand
    else:
        return hand


    
def play_game(word_list:list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    sub_status = False
    replay_status = False
    total_hand = int(input('Enter total number of hands: '))
    total_score = 0

    while total_hand > 0:
        hand = deal_hand(HAND_SIZE)
        print('Current hand:', display_hand(hand))
        hand_score = 0
        replay_score = 0
        
        if not sub_status:
            substitute = input('Would you like to substitue a letter? ')
            if substitute.lower() == 'yes':
                replace_letter = input('Which letter would you like to replace: ')
                hand = substitute_hand(hand, replace_letter)
                sub_status = True

        hand_score = play_hand(hand, word_list)       

        if not replay_status:
            replay = input('Would you like to replay the hand? ')
            if replay.lower() == 'yes':
                replay_score = play_hand(hand, word_list)
                hand_score = max(hand_score, replay_score)
                replay_status = True
        
        total_hand -= 1
        total_score += hand_score
    
    print('Total score over all hands:', total_score)
        



if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

