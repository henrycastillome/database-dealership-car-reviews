from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator



class CarMake(models.Model):
    name= models.CharField(null=False,max_length=100)
    country= models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name 

class CarModel(models.Model):
    car_make=models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    dealer_id=models.IntegerField(null=False)
    name=models.CharField(null=False, max_length=100)
    SEDAN='sedan'
    SUV='SUV'
    WAGON='wagon'
    TYPE_CHOICES= [
        (SEDAN,"Sedan"),
        (SUV, "SUV"),
        (WAGON, 'Wagon')
    ]
    type=models.CharField(null=False, choices=TYPE_CHOICES, default=SEDAN, max_length=50)
    year=models.IntegerField(null=False, validators=[MinValueValidator(1900), MaxValueValidator(2100)])

    def __str__(self):
        return "Car_make:" + str(self.car_make.name) + ","  + "dealer id" + str(self.dealer_id)  + ","  + "name" + self.name  + "," + "type" + self.type  + ","  + "year" + str(self.year )
    
        
        


