from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


saves = db.Table(
  'saves',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
  db.Column('crystal_id', db.Integer, db.ForeignKey('crystal.id'), primary_key=True)
)

class Crystal(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), unique=True, nullable=False)
  props = db.Column(db.String(200), nullable=False)
  desc = db.Column(db.String(500), nullable=False)
  img = db.Column(db.String(120), nullable=False)

  def __repr__(self):
    return f"Crystal('{self.name}')"


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  user_saves = db.relationship(
    'Crystal',
    secondary=saves,
    backref='saved_by'
  )

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"