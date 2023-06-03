from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100)
    country = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=100)
    SEDAN = 'sedan'
    SUV = 'SUV'
    WAGON = 'wagon'
    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, 'Wagon')
    ]
    type = models.CharField(
        null=False, choices=TYPE_CHOICES, default=SEDAN, max_length=50)
    year = models.IntegerField(null=False, validators=[
                               MinValueValidator(1900), MaxValueValidator(2100)])

    def __str__(self):
        return "Car_make:" + str(self.car_make.name) + "," + "dealer id" + str(self.dealer_id) + "," + "name" + self.name + "," + "type" + self.type + "," + "year" + str(self.year)


class CarDealer:

    def __init__(self, id, full_name, address, city, st, state, zip):
        self.id = id
        self.full_name = full_name
        self.address = address
        self.city = city
        self.st = st
        self.state=state
        self.zip = zip

    def __str__(self):
        return self.full_name, self.address, self.city, self.st, self.state, self.zip
    




class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, review_id, sentiment):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.review_id = review_id
        self.sentiment=sentiment
        
        

    def __str__(self):
        return self.dealership, self.name, self.purchase, self.review, self.purchase_date, self.car_make, self.car_model, self.car_year, self.review_id, self.sentiment
