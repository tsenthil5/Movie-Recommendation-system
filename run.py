from moviechanges import app

if __name__ == "__main__":
	app.run(debug=True)










#from flask import Flask,render_template,request,url_for,redirect,flash
#from forms import RegistrationForm
##from forms import LoginForm
#from flask_sqlalchemy import SQLAlchemy

#import pandas as pd
#import numpy as np
#from sklearn.feature_extraction.text import *
#from sklearn.metrics.pairwise import cosine_similarity

#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'abcdefgh'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#db = SQLAlchemy(app)
#from models import User

#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(20), unique=True, nullable=False)
#    email = db.Column(db.String(120), unique=True, nullable=False)
#    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#    password = db.Column(db.String(60), nullable=False)
#    def __repr__(self):
#        return f"User('{self.username}','{self.email}','{self.image_file}')"



#@app.route('/',methods=['GET','POST'])
#def register():
#	form=RegistrationForm()
#	if form.validate_on_submit():
#		flash(f'account created for {form.username.data}!','success')
#		return redirect(url_for('send'))
#	return render_template('register.html',form=form)

#@app.route("/login", methods=['GET', 'POST'])
#def login():
#    form = LoginForm()
#    if form.validate_on_submit():
#            flash('You have been logged in!', 'success')
#            return redirect(url_for('send'))
#        else:
##    return render_template('login.html', title='Login', form=form)


#@app.route('/send', methods = ['GET','POST'])
#def send():
#	if request.method == 'POST':
#		movie = request.form['movie_name']


#		def get_title_from_index(index):
#			return (df[df.index == index]["title"].values[0],df[df.index == index]["Img_links"].values[0],df[df.index == index]["Synopsys"].values[0])

#		def get_index_from_title(title):
#			return df[df.title == title]["index"].values[0]


#		df = pd.read_csv("export_dfinal.csv")

#		features = ['keywords','cast','director']
#		for feature in features:
#			df[feature] = df[feature].fillna('')

#		def combine_features(row):
#			try:
#				return row['keywords'] +" "+row['cast']+" "+row["director"]
#			except:
#				print ("Error:", row)

#		df["combined_features"] = df.apply(combine_features,axis=1)


#		cv = CountVectorizer()

#		count_matrix = cv.fit_transform(df["combined_features"])


#		cosine_sim = cosine_similarity(count_matrix)
#		movie_user_likes = movie

#		movie_index = get_index_from_title(movie_user_likes)

#		similar_movies =  list(enumerate(cosine_sim[movie_index]))

#		sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

#		i=0
#		recom_movie = []
#		img_link_f = []
#		synopsys_f = []
#		for element in sorted_similar_movies:
#				movie_title,img_link,synopsys = get_title_from_index(element[0])
#				recom_movie.append(movie_title)
#				img_link_f.append(img_link)
#				synopsys_f.append(synopsys)

#				i=i+1
#				if i > 5:
#					break;
#		return render_template('display.html',recom_movie = recom_movie,img_link_f = img_link_f,synopsys_f = synopsys_f)


#	return render_template('input.html')
