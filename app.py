from flask import Flask, request, jsonify
import json
from marshmallow.fields import Bool
from sqlalchemy import Column, Integer, String
import csv


app = Flask(__name__)

db = SQLAlchemy(app)
ma = Marshmallow(app)
# create a flask backend for receiving a csv file via post request

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
#def db_seed():
#    mercury = Planet(planet_name='Mercury',
#                     planet_type='Class D',
#                     home_star='Sol',
#                     mass=2.258e23,
#                     radius=1516,
#                     distance=35.98e6)
#
#    venus = Planet(planet_name='Venus',
#                         planet_type='Class K',
#                         home_star='Sol',
#                         mass=4.867e24,
#                         radius=3760,
#                         distance=67.24e6)
#
#    earth = Planet(planet_name='Earth',
#                     planet_type='Class M',
#                     home_star='Sol',
#                     mass=5.972e24,
#                     radius=3959,
#                     distance=92.96e6)

#    db.session.add(mercury)
#    db.session.add(venus)
#    db.session.add(earth)




@app.route('/')
def hello_world():
    return 'Flask backend for receiving csv files!'

@app.route('/add_review', methods=['POST'])
def add_review():
    review_name = request.form['csv_sample']
    test = Review.query.filter_by(review_name=review_name).first()
    if test:
        return jsonify("There is already a csv file by that name"), 409
    else:
        review_id = request.form['review_id']
        review_username = request.form['review_username']
        review_header = request.form['review_header']
        review_body = request.form['review_body']
        review_like = bool(request.form['review_like'])

        new_review = Review(review_id=review_id,
                            review_username=review_username,
                            review_header=review_header,
                            review_body=review_body,
                            review_like=review_like)

        db.session.add(new_review)
        db.session.commit()
        return jsonify(message="You added a review"), 201

# database models
class Review(db.Model):
    __tablename__ = 'Reviews'
    review_id = Column(Integer, primary_key=True)
    review_username = Column(String)
    review_header = Column(String)
    review_body = Column(String)
    review_like = Column(Bool)


class ReviewSchema(ma.Schema):
    class Meta:
        fields = ('review_id', 'review_username', 'review_header', 'review_body', 'review_like')


if __name__ == '__main__':
    app.run()
