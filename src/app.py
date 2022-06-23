from flask import Flask, request
from happytransformer import HappyTextToText, TTSettings
import json
import requests

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    #inp=""
    grammar=""
    spell=""
    autotext=""

    try:
        sentence=request.form['input']
    except:
        sentence=""
    if sentence != "":
        grammar = grammar_check(sentence)
        spell = spell_check(sentence)
        autotext = auto(sentence)


    with open("index.html", "r") as f:
        readfile = f.read()
    readfile = readfile.replace("[input]",sentence)
    readfile = readfile.replace("[grammar]",grammar)
    readfile = readfile.replace("[spell]",spell)
    readfile = readfile.replace("[auto]",autotext)
    return readfile



def grammar_check(usr):
    happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

    args = TTSettings(num_beams=5, min_length=1)

    # Add the prefix "grammar: " before each inp
    result = happy_tt.generate_text(usr, args=args)
    return result.text



def auto(usr):
    API_URL = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": "Bearer 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"}
    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))
    data = query(usr)
    retVal = data[0].get("generated_text")
    return retVal


def spell_check(s):
    out=""
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
            #three_words = similar_words(string)
            #out = out + ("You might have meant: " + "\n"+ three_words[0] + " [1] " + "\n" + three_words[1] + " [2] " + "\n" + three_words[2] + " [3] ")
            #out = "\n" + out + ("If you meant " + string + ", input [y]")
            #response = input("If you meant any of the words above, input the corresponding number")
            #if response == "y":
            #    file = open("words.txt", "a")
            #    file.write(string+"\n")
            #    file.close()
            #    error_counter -= 1
    out = "\n" + out + ("You have " + str(error_counter) + " errors")
    return out

def each_error(word):
    return

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
        words = []
        print("file not found")
        return words

def check_dict(word, list_words):
    index = 0
    while(index < len(list_words)):
        if (word.lower() == list_words[index].lower()):
            return True
        index+=1
    return False
