from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=60, blank=True)
    founded = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    class CarType(models.TextChoices):
        SEDAN = 'SEDAN', 'Sedan'
        SUV = 'SUV', 'SUV'
        WAGON = 'WAGON', 'Wagon'
        TRUCK = 'TRUCK', 'Truck'
        COUPE = 'COUPE', 'Coupe'
        HATCHBACK = 'HATCHBACK', 'Hatchback'
        ELECTRIC = 'ELECTRIC', 'Electric'

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CarType.choices, default=CarType.SUV)
    year = models.IntegerField(
        default=2025, validators=[MinValueValidator(2015), MaxValueValidator(2026)]
    )
    # Id of a dealership stored in the Express/MongoDB service
    dealer_id = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['car_make__name', 'name']
        unique_together = ('car_make', 'name', 'year')

    def __str__(self):
        return f'{self.car_make.name} {self.name} ({self.year})'
