import nltk
from flask import Flask, render_template, request
import pickle
import string

app: Flask = Flask(__name__, template_folder='template', static_folder='static')
nltk.download('stopwords')
nltk.download('punkt')
stopWords = nltk.corpus.stopwords.words('english')


def transform_text(text):
    #convart lower case
    text = text.lower()

    # tokenization :: convert string in to a list of words
    text = nltk.word_tokenize(text)

    # remove spatial char
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]  # this is cloning
    y.clear()

    # remove stop words and punctuation
    for i in text:
        if i not in stopWords and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    # stemming
    #  is process of reducing a word to its root word
    # for example dancing ---> dance
    ps = nltk.porter.PorterStemmer()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# ML object import
with open('tfid.pkl', 'rb') as f2:
    # Load the pickled object from the file
    tfid = pickle.load(f2)

with open('model.pkl', 'rb') as f1:
    # Load the pickled object from the file
    model = pickle.load(f1)


@app.route("/", methods=['GET'])
def lode_home_page():
    return render_template('home.html', head='Check Your SMS Spam or Not',root_home=True)


@app.route("/submit", methods=['POST'])
def result_page():
    mess = request.form.get("sms")
    process = transform_text(mess)
    vectorized = tfid.transform([process]).toarray()
    pdt = model.predict(vectorized)
    if pdt == 0:
        head_mess = 'This is not a Spam'
        root_home_=True
    else:
        head_mess = 'Spam!!'
        root_home_=False
    return render_template('home.html', head=head_mess,root_home=root_home_)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
