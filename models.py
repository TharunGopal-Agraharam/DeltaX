from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="New")
    salesperson = db.Column(db.String(50), nullable=True)

    def _repr_(self):
        return f"<Lead {self.name}>"
