from flask import Flask,render_template,url_for,request

import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
import preprocessor as p
from preprocessor import api
lemmatizer = WordNetLemmatizer()
import pickle

# load the model from disk
filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
cv=pickle.load(open('tranform.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')
@app.route('/predict',methods=['POST'])
def predict():

	if request.method == 'POST':
		message = request.form['message']
		
		data = [message]
		show=api.clean(message)		
		show=re.sub(r'[0-9]+','',show)
		show=re.sub(r'[^\w\s]','',show)
		show = show.lower()
		show = show.split()
		show = [lemmatizer.lemmatize(word) for word in show if not word in stopwords.words('english')]
		show = ' '.join(show)
		
		vect = cv.transform([show]).toarray()
		my_prediction = clf.predict(vect)
	return render_template('result.html',prediction = my_prediction)



if __name__ == '__main__':
	app.run(debug=True)
