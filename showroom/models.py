from django.db import models

# color options for car colors
COLORS = (
    ('blue', 'Blue'),
    ('red', 'Red'),
    ('green', 'Green')
)


class Car(models.Model):
    """
    All cars stored in this model
    """
    car_make = models.CharField(max_length=20)
    color = models.CharField(max_length=20, choices=COLORS)
    reg_number = models.CharField(max_length=20, unique=True)
    yom = models.IntegerField()
    car_type = models.CharField(max_length=20)
    available = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    viewable = models.BooleanField()
