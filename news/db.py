from app import db
from datetime import datetime


class File(db.Model):

	__tablename__ = 'file'
	"""docstring for File"""
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(80))
	created_time = db.Column(db.DateTime)
	catogory_id = db.Column(db.Integer,db.ForeignKey('catogory.id'))
	content = db.Column(db.Text)
	catogory = db.relationship('Category',backref='file')


	def __init__(self,title,created_time=None,catogory,content):
		self.title = title
		self.created_time = created_time
		self.catogory_id = catogory_id
		if created_time is None:
			self.created_time = datetime.utcnow()
		self.created_time = created_time
		self.catogory = catogory
	def __repr__(self):
		return '<File %r>' % self.title
			

		
class Category(db.Model):
	__tablename__ = 'catogory'
	id = db.Column(db.Integer,primary_key = True)

	name = db.Column(db.String(80))

	"""docstring for Category"""
	def __init__(self,name):
		self.name = name
	def __repr__(self):
		return '<Category %r>' % self.name
						
