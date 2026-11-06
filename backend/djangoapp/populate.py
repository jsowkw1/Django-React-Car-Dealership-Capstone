"""Demonstration car makes and models."""
from .models import CarMake, CarModel

CAR_DATA = [
    ('Toyota', 'Japan', 1937, 'Reliable, efficient cars and the best-selling hybrid line-up.', [
        ('Camry', 'SEDAN', 2025, 1), ('RAV4', 'SUV', 2025, 1), ('Prius', 'HATCHBACK', 2024, 13),
        ('4Runner', 'SUV', 2025, 11), ('Tacoma', 'TRUCK', 2026, 5)]),
    ('Honda', 'Japan', 1948, 'Practical, fuel-efficient cars with excellent resale value.', [
        ('Civic', 'SEDAN', 2023, 1), ('Accord', 'SEDAN', 2025, 10), ('CR-V', 'SUV', 2025, 10),
        ('Pilot', 'SUV', 2024, 12)]),
    ('Ford', 'United States', 1903, 'Trucks, SUVs and performance cars built in America.', [
        ('F-150', 'TRUCK', 2025, 2), ('Escape', 'SUV', 2024, 1), ('Mustang', 'COUPE', 2025, 15),
        ('Explorer', 'SUV', 2025, 5)]),
    ('Chevrolet', 'United States', 1911, 'Full-size trucks, family SUVs and the Corvette.', [
        ('Silverado', 'TRUCK', 2024, 2), ('Tahoe', 'SUV', 2025, 5), ('Malibu', 'SEDAN', 2023, 4),
        ('Bolt EUV', 'ELECTRIC', 2023, 6)]),
    ('BMW', 'Germany', 1916, 'Premium sport sedans and SUVs.', [
        ('3 Series', 'SEDAN', 2025, 8), ('X5', 'SUV', 2026, 3), ('i4', 'ELECTRIC', 2025, 7)]),
    ('Mercedes-Benz', 'Germany', 1926, 'Luxury vehicles with advanced safety technology.', [
        ('C-Class', 'SEDAN', 2025, 3), ('GLE', 'SUV', 2025, 8), ('EQB', 'ELECTRIC', 2024, 7)]),
    ('Nissan', 'Japan', 1933, 'Affordable everyday cars and pioneering EVs.', [
        ('Altima', 'SEDAN', 2021, 4), ('Rogue', 'SUV', 2025, 9), ('Leaf', 'ELECTRIC', 2024, 6),
        ('Frontier', 'TRUCK', 2025, 14)]),
    ('Subaru', 'Japan', 1953, 'Symmetrical all-wheel drive on almost every model.', [
        ('Outback', 'WAGON', 2025, 11), ('Forester', 'SUV', 2025, 13)]),
]


def initiate():
    """Creates the demonstration makes/models (idempotent)."""
    for name, country, founded, description, models in CAR_DATA:
        make, _ = CarMake.objects.get_or_create(
            name=name, defaults={'country': country, 'founded': founded, 'description': description}
        )
        for model_name, car_type, year, dealer_id in models:
            CarModel.objects.get_or_create(
                car_make=make, name=model_name, year=year,
                defaults={'type': car_type, 'dealer_id': dealer_id},
            )
