import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        word = request.form['word']
        if word.strip() != '':
            print("api", API_KEY)
            url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={API_KEY}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    try:
                        first_definition = data[0]['shortdef'][0]
                    
                        return render_template('index.html', definition=first_definition, word=word)
                    except TypeError:
                        first_definition = data[0]
                        return render_template('index.html', 
                                               error_message='No definitions found for the word "{}". Check the spelling. Do you mean the word <{}> ?'.format(word,first_definition))
                else:
                    return render_template('index.html', error_message='No definitions found for the word "{}".'.format(word))
            else:
                return render_template('index.html', error_message='Error retrieving definition. Please try again later.')
        else:
            return render_template('index.html', error_message='Please enter a word to look up.')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
