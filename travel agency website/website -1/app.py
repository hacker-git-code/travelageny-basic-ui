from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
db = SQLAlchemy(app)

class Continent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    destinations = db.relationship('Destination', backref='continent', lazy=True)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    highlights = db.Column(db.Text, nullable=False)
    continent_id = db.Column(db.Integer, db.ForeignKey('continent.id'), nullable=False)
    featured = db.Column(db.Boolean, default=False)

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_subscribed = db.Column(db.DateTime, default=datetime.utcnow)

def init_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()

        # Add sample continents
        continents = [
            {
                'name': 'North America',
                'description': 'Discover the wonders of North America, from bustling cities to breathtaking natural landscapes.',
                'image': 'north-america.jpg'
            },
            {
                'name': 'South America',
                'description': 'Experience the vibrant culture and stunning landscapes of South America.',
                'image': 'south-america.jpg'
            },
            {
                'name': 'Europe',
                'description': 'Explore the rich history and diverse cultures of Europe.',
                'image': 'europe.jpg'
            },
            {
                'name': 'Asia',
                'description': 'Immerse yourself in the ancient traditions and modern wonders of Asia.',
                'image': 'asia.jpg'
            },
            {
                'name': 'Africa',
                'description': 'Embark on unforgettable adventures across the diverse landscapes of Africa.',
                'image': 'africa.jpg'
            },
            {
                'name': 'Oceania',
                'description': 'Discover paradise in the stunning islands and landscapes of Oceania.',
                'image': 'oceania.jpg'
            }
        ]
        
        for cont in continents:
            continent = Continent(**cont)
            db.session.add(continent)
        db.session.commit()

        # Add sample destinations
        sample_destinations = [
            {
                'name': 'New York City',
                'description': 'Experience the energy of the city that never sleeps.',
                'image': 'nyc.jpg',
                'price': 1499.99,
                'highlights': 'Times Square, Central Park, Empire State Building',
                'continent_id': 1,
                'featured': True
            },
            {
                'name': 'Machu Picchu',
                'description': 'Explore the ancient Incan citadel in the Andes Mountains.',
                'image': 'machu-picchu.jpg',
                'price': 1899.99,
                'highlights': 'Ancient ruins, Mountain hiking, Cultural experiences',
                'continent_id': 2,
                'featured': True
            },
            {
                'name': 'Tokyo',
                'description': 'Discover the perfect blend of tradition and modernity.',
                'image': 'tokyo.jpg',
                'price': 1799.99,
                'highlights': 'Temples, Modern districts, Japanese cuisine',
                'continent_id': 4,
                'featured': True
            }
        ]
        
        for dest in sample_destinations:
            destination = Destination(**dest)
            db.session.add(destination)
        
        db.session.commit()

# Initialize the database
init_db()

@app.route('/')
def index():
    continents = Continent.query.all()
    featured_destinations = Destination.query.filter_by(featured=True).all()
    return render_template('index.html', continents=continents, featured_destinations=featured_destinations)

@app.route('/continent/<int:id>')
def continent(id):
    continent = Continent.query.get_or_404(id)
    return render_template('continent.html', continent=continent)

@app.route('/destination/<int:id>')
def destination(id):
    destination = Destination.query.get_or_404(id)
    return render_template('destination.html', destination=destination)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
    else:
        email = request.form.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    try:
        subscriber = Subscriber(email=email)
        db.session.add(subscriber)
        db.session.commit()
        return jsonify({'message': 'Successfully subscribed!'}), 200
    except:
        db.session.rollback()
        return jsonify({'error': 'Email already subscribed or invalid'}), 400

if __name__ == '__main__':
    app.run(debug=True)
