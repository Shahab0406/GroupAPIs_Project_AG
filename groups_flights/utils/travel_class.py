from django.db import models


class TravelClass(models.TextChoices):
    ECONOMY = "economy", "Economy"
    PREMIUM_ECONOMY = "premium_economy", "Premium Economy"
    BUSINESS = "business", "Business"
    FIRST = "first", "First"
