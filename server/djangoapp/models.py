from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, primary_key=True)
    dealer_id = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Wagon', 'Wagon')])
    year = models.DateField()

    def __str__(self):
        return self.name

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, sentiment, id=0, purchase_date='NA', car_make='NA', car_model='NA', car_year='NA'):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.sentiment = sentiment
        self.id = id
        self.car_year = car_year

    def __str__(self):
        return "Review: " + self.review