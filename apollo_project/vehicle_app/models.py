from django.db import models

# Create your models here.

class Vehicle(models.Model):
    vin = models.CharField(max_length=17, unique=True, db_index=True)
    manufacturer_name = models.CharField(max_length=100)
    description = models.TextField()
    horse_power = models.IntegerField()
    model_name = models.CharField(max_length=100)
    model_year = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        # Ensure VIN uniqueness is case-insensitive by normalizing VIN to uppercase before saving
        self.vin = self.vin.upper()
        super(Vehicle, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.manufacturer_name} {self.model_name} ({self.model_year}) - {self.vin}"