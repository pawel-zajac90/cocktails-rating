from faker import Faker
from cocktails_rating import db
from rating.models import Pub, Cocktail, Rating
from random import randint


drop = input('Do You want to drop the tables if they exist?')
if drop.lower() != 'n':
    db.drop_all()

number_of_pubs = int(input('How many pubs?'))
number_of_cocktails = int(input('How many cocktails for each pub?'))
number_of_ratings = int(input('How many ratings for each cocktail?'))

fake = Faker()
db.create_all()
fake.name()
for n in range(number_of_pubs):
    name = fake.first_name() + "'s pub"
    n = Pub(name=name)
    db.session.add(n)

for pub in Pub.query.all():
    for c in range(number_of_cocktails):
        c_name = fake.first_name() + "'s cocktail"
        description = fake.text()
        c = Cocktail(name=c_name, pub_id=pub.id, description=description)
        db.session.add(c)

for cocktail in Cocktail.query.all():
    for r in range(number_of_ratings):
        rating = randint(0,5)
        r = Rating(cocktail_id=cocktail.id, rating=rating)
        db.session.add(r)

db.session.commit()
