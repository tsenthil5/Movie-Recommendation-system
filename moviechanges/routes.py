from moviechanges.models import User
from PIL import Image
import secrets
import os
from flask import Flask,render_template,request,url_for,redirect,flash,jsonify
from moviechanges.forms import RegistrationForm,UpdateAccountForm
from moviechanges.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from moviechanges import app,db,bcrypt
from flask_login import login_user,logout_user,login_required,current_user
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import *
from sklearn.metrics.pairwise import cosine_similarity
recom_movie = []
img_link_f = []
synopsys_f = []
cast_f = []



@app.route('/',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'account created for {form.username.data}!','success')
        return redirect(url_for('send'))
    return render_template('register.html',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()        #checks for email in db
      if user and bcrypt.check_password_hash(user.password,form.password.data):
          login_user(user, remember = form.remember.data)
          return redirect(url_for('send'))
      else:
          flash('Login Unsuccessful. Please check email and password', 'danger')
  return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',image_file=image_file,form=form)


@app.route('/send', methods = ['GET','POST'])
@login_required
def send():
	if request.method == 'POST':
		movie = request.form['movie_name']


		def get_title_from_index(index):
			return (df[df.index == index]["title"].values[0],df[df.index == index]["Img_links"].values[0],df[df.index == index]["Synopsys"].values[0],df[df.index == index]["cast"].values[0])

		def get_index_from_title(title):
			return df[df.title == title]["index"].values[0]


		df = pd.read_csv("export_dfinal.csv")

		features = ['keywords','cast','director']
		for feature in features:
			df[feature] = df[feature].fillna('')

		def combine_features(row):
			try:
				return row['keywords'] +" "+row['cast']+" "+row["director"]
			except:
				print ("Error:", row)

		df["combined_features"] = df.apply(combine_features,axis=1)


		cv = CountVectorizer()

		count_matrix = cv.fit_transform(df["combined_features"])


		cosine_sim = cosine_similarity(count_matrix)
		movie_user_likes = movie

		movie_index = get_index_from_title(movie_user_likes)

		similar_movies =  list(enumerate(cosine_sim[movie_index]))

		sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

		i=0
		global recom_movie
		global img_link_f
		global synopsys_f
		global cast_f
		recom_movie = []
		img_link_f = []
		synopsys_f = []
		cast_f = []
		for element in sorted_similar_movies:
				movie_title,img_link,synopsys,cast = get_title_from_index(element[0])
				recom_movie.append(movie_title)
				img_link_f.append(img_link)
				synopsys_f.append(synopsys)
				cast_f.append(cast)
				i=i+1
				if i > 5:
					break;
		return render_template('carousal.html',recom_movie = recom_movie,img_link_f = img_link_f,synopsys_f = synopsys_f)








	return render_template('form.html')

@app.route('/process', methods = ['POST'])

def process():
	return jsonify({'recom_movie' : recom_movie,'img_link_f' : img_link_f,'synopsys_f' : synopsys_f,'cast_f':cast_f})
