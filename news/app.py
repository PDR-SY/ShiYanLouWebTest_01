from flask import Flask,render_template,abort
import os
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('127.0.0.1',27017)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)
monDb = client.shiyanlou

@app.route('/')
def index():
	titles = File.query.all()
	tags = []
	for title in titles:
		file_tag = monDb.tag.find_one({'file_id':title.id})
		print(file_tag)
		tags.append(file_tag['name'])

	return render_template('index.html',titles = titles,tag = tags)


@app.route('/file/<file_id>')
def file(file_id):
	file_click =  File.query.filter_by(id=file_id).first()
	
	if file_click is not None:
			return render_template('file.html',file = file_click) 
	else:
		abort(404)


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'),404


class File(db.Model):

	"""docstring for File"""
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(80))
	created_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
	content = db.Column(db.Text)
	category = db.relationship('Category',backref='file')

	def __init__(self,title,category,content,created_time=None):
		self.title = title
		self.created_time = created_time
		self.content = content
		if created_time is None:
			self.created_time = datetime.utcnow()
		self.created_time = created_time
		self.category = category
	def __repr__(self):
		return '<File %r>' % self.title

	def add_tag(self,tag_name):
		file_id = self.id
		tag = monDb.tag.find_one({'file_id':file_id})
		if tag is not None:
			print('update',file_id,tag_name,tag)
			monDb.tag.update_one({'file_id':file_id},{'$set':{'name':tag['name'] if tag_name in tag['name'] else tag['name']+','+tag_name}})
		else:
			print('insert',self.id,tag_name)
			monDb.tag.insert_one({'file_id':file_id,'name':tag_name})

	def remove_tag(self,tag_name):
		file_id = self.id
		#file_id = File.query.filter_by(created_time=self.created_time).first().id
		tag = monDb.tag.find_one({'file_id':file_id})
		#if tag is not None:
		monDb.tag.update_one({'file_id':file_id},{'$set':{'name':tag['name'].replace(tag_name,'').replace(',,',',') if tag_name in tag['name'] else tag['name']}})
		
	@property
	def tags(self):
		file_id = File.query.filter_by(created_time=self.created_time).first().id
		return monDb.tag.find_many({'file_id':file_id})


		
class Category(db.Model):

	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(80))
	child = db.relationship('File')
	"""docstring for Category"""
	def __init__(self,name):
		self.name = name
	def __repr__(self):
		return '<Category %r>' % self.name
