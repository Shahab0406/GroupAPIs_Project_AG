import json
from datetime import datetime

from django.core.management.base import BaseCommand

from groups_flights.models import Segment as Flight


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        with open("data/flights_segments_data.json", "r") as file:
            flights = json.load(file)
        count = 0

        flight_list = []

        for flight in flights:
            
            flight = Flight(
                flight_number=flight["flight_number"],
                arrival_datetime=datetime.fromisoformat(
                    flight["arrival_datetime"]
                ),
                departure_datetime=datetime.fromisoformat(
                    flight["departure_datetime"]
                ),
                origin=flight["origin"],
                destination=flight["destination"],
                operating_airline=flight["operating_airline"],
                marketing_airline=flight["marketing_airline"],
            )
            count += 1
            print(f"Inserted flight : {count}")
            flight_list.append(flight)

        Flight.objects.bulk_create(flight_list)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {len(flights)} flights."
            )
        )