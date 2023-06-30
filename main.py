from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os,nltk
root = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(root)
os.chdir(download_dir)
nltk.data.path.append(download_dir)
from nltk.tokenize import sent_tokenize, word_tokenize


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def getQuestion(lyrics):
    # dividing to each sentence
    paragraphs = lyrics.split("\n")

    
    # dividing to each individual words in sentence
    store_2 = []
    for paragraph in paragraphs:
        divided_words = word_tokenize(paragraph)
        store_2.append(divided_words)
   

    # tagging each word with there repective POS
    store_3 = []
    for list_a in store_2:
        pos_words = nltk.pos_tag(list_a)
        store_3.append(pos_words)



    # extracting the line which has more nouns
   
    def count_nouns(sublist):
        noun_count = 0
        for word, pos in sublist:
            if pos.startswith('NN'):
                noun_count += 1
        return noun_count

    
    def extract_sublist_with_most_nouns(list_of_lists):
        max_noun_count = 0
        sublist_with_most_nouns = []
        for i, sublist in enumerate(list_of_lists):
            noun_count = count_nouns(sublist)
            if noun_count > max_noun_count:
                max_noun_count = noun_count
                sublist_with_most_nouns = sublist
                index = i
        return sublist_with_most_nouns, index





    paragraph_with_more_nouns, index = extract_sublist_with_most_nouns(store_3)

    sentence_from_lyrics_which_has_more_nouns = paragraphs[index]


    replaced_sentence = ""
    for word, pos in paragraph_with_more_nouns:
        if pos.startswith('NN'):
            replaced_sentence = sentence_from_lyrics_which_has_more_nouns.replace(word, "____")

    return replaced_sentence


@app.route('/question', methods=['POST'])
@cross_origin()
def question():
    lyrics = request.json.get('lyrics')
    return jsonify(data=getQuestion(lyrics))

if __name__ == '__main__':
    app.run(debug=True)
