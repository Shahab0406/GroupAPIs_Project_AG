from django.db import models


class Segments(models.Model):
    flight_number = models.CharField(max_length=20)

    arrival_datetime = models.DateTimeField()
    departure_datetime = models.DateTimeField()

    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)

    operating_airline = models.CharField(max_length=3)
    marketing_airline = models.CharField(max_length=3)

    def __str__(self):
        return self.flight_number