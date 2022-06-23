from happytransformer import HappyTextToText, TTSettings
import string

def grammar(input):
    happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

    args = TTSettings(num_beams=5, min_length=1)

    # Add the prefix "grammar: " before each input
    result = happy_tt.generate_text(input, args=args)

    return(result.text) # This sentence has bad grammar.


def spell_check(s):
    dict = parse_dict("words.txt")
    punctuation = '''
!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
'''
    for i in s:
        if(i in punctuation):
            s.replace(i, "")
    s = s.split()
    error_counter = 0
    for string in s:
        if (not check_dict(string, dict)):
            error_counter += 1
            three_words = similar_words(string)
            print("You might have meant: " + "\n"+ three_words[0] + " [1] " + "\n" + three_words[1] + " [2] " + "\n" + three_words[2] + " [3] ")
            print("If you meant " + string + ", input [y]")
            response = input("If you meant any of the words above, input the corresponding number")
            if response == "y":
                file = open("words.txt", "a")
                file.write(string)
                file.close()
                error_counter -= 1
    print("You have " + str(error_counter) + " errors")
    return error_counter

def check_difference(s, word):
    difference = 0
    index = 0
    while(index < len(word)):
        if(s[index].lower() != word[index].lower()):
            difference += 1
        index += 1
    return difference

def similar_words(word):
    dict = parse_dict("words.txt")
    similar_words = []
    three_words = ["null"] *3
    for s in dict:
        if (len(s) == len(word)):
            difference = check_difference(s, word)
            if (difference <= 1):
                similar_words.append(s)
    i = 0
    while(i < 3 and i < len(similar_words)):
        three_words[i]=similar_words[i]
        i+=1
    return three_words


def parse_dict(file_name):
    try:
        f = open(file_name, "r")
        words = f.read().split()
        return words
    except:
        print("file not found")

def check_dict(word, list_words):
    index = 0
    while(index < len(list_words)):
        if (word.lower() == list_words[index].lower()):
            return True
        index+=1
    return False

def main():
    inp = input()
    error = 0
    if (grammar(inp) != inp):
        error+=1
    error += spell_check(inp)
    punctuation = '''
!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
'''
    for i in inp:
        if(i in punctuation):
            inp.replace(i, "")
    inp = inp.split()

    print("your writing score: " + str(((len(inp)-error)/len(inp))*100) + "%")

main()
