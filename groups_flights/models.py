from django.db import models, transaction

from groups_flights.utils import BookingStatus, TravelClass


class Group(models.Model):
    group_name = models.CharField(max_length=255)
    adult_seats = models.PositiveIntegerField(help_text="Total number of adult seats in the group")
    available_adult_seats = models.PositiveIntegerField(
        help_text="Adult seats currently available for booking",
    )
    child_seats = models.PositiveIntegerField(help_text="Total number of child seats in the group")
    available_child_seats = models.PositiveIntegerField(
        help_text="Child seats currently available for booking",
    )

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

    class Meta:
        db_table = "groups"

    def __str__(self):
        return self.group_name


class GroupBookingDetail(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="booking_details",
    )
    flight = models.ForeignKey(
        "Flight",
        on_delete=models.CASCADE,
        related_name="booking_details",
    )
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.ON_HOLD,
    )
    adult_seats_requested = models.PositiveIntegerField(default=0)
    child_seats_requested = models.PositiveIntegerField(default=0)
    adult_price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    child_price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    token_payment_deadline = models.DateTimeField()
    full_payment_deadline = models.DateTimeField()

    class Meta:
        db_table = "group_booking_details"

    def __str__(self):
        return f"{self.group.group_name} booking ({self.status})"

    def release_seats(self):
        with transaction.atomic():
            group = Group.objects.select_for_update().get(pk=self.group_id)
            group.available_adult_seats = min(
                group.adult_seats,
                group.available_adult_seats + self.adult_seats_requested,
            )
            group.available_child_seats = min(
                group.child_seats,
                group.available_child_seats + self.child_seats_requested,
            )
            group.save(
                update_fields=["available_adult_seats", "available_child_seats"]
            )

    def save(self, *args, **kwargs):
        previous_status = None
        if self.pk:
            previous_status = (
                GroupBookingDetail.objects.filter(pk=self.pk)
                .values_list("status", flat=True)
                .first()
            )

        super().save(*args, **kwargs)

        if (
            previous_status is not None
            and previous_status != BookingStatus.CANCELLED
            and self.status == BookingStatus.CANCELLED
        ):
            self.release_seats()


class Flight(models.Model):
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
