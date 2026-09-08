from django.db import models


class Group(models.Model):
    group_name = models.CharField(max_length=255)
    seats = models.PositiveIntegerField(help_text="Number of seats available")
    child_seats = models.PositiveIntegerField(help_text="Number of child seats available")

    token_payment_deadline = models.DateTimeField()
    full_payment_deadline = models.DateTimeField()
    token_amount = models.DecimalField(max_digits=10, decimal_places=2)

    buying_currency = models.CharField(max_length=3)
    buying_price_per_seat_adult = models.DecimalField(max_digits=10, decimal_places=2)
    buying_price_per_seat_child = models.DecimalField(max_digits=10, decimal_places=2)
    buying_price_per_seat_infant = models.DecimalField(max_digits=10, decimal_places=2)

    selling_currency = models.CharField(max_length=3)
    selling_price_per_seat_adult = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price_per_seat_child = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price_per_seat_infant = models.DecimalField(max_digits=10, decimal_places=2)

    pnr = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    class meta:
        db_table = "groups"
        
    def __str__(self):
        return self.group_name


class Flight(models.Model):
    class TravelClass(models.TextChoices):
        ECONOMY = "economy", "Economy"
        PREMIUM_ECONOMY = "premium_economy", "Premium Economy"
        BUSINESS = "business", "Business"
        FIRST = "first", "First"

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="flights",
    )

    flight_number = models.CharField(max_length=20)
    departure_datetime = models.DateTimeField()
    origin = models.CharField(max_length=3)
    arrival_datetime = models.DateTimeField()
    destination = models.CharField(max_length=3)

    travel_class = models.CharField(
        max_length=20,
        choices=TravelClass.choices,
        default=TravelClass.ECONOMY,
    )
    baggage_allowance = models.CharField(max_length=100)
    meal_available = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "flight_number", "departure_datetime"],
                name="unique_flight_per_group_departure",
            ),
        ]
        db_table = "flights"

    def __str__(self):
        return f"{self.flight_number} ({self.origin} → {self.destination})"


class Segment(models.Model):
    flight_number = models.CharField(max_length=20)

    arrival_datetime = models.DateTimeField()
    departure_datetime = models.DateTimeField()

    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)

    operating_airline = models.CharField(max_length=3)
    marketing_airline = models.CharField(max_length=3)

    class Meta:
        db_table = "segments"
    def __str__(self):
        return self.flight_number
    
