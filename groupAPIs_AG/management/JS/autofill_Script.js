document.addEventListener('DOMContentLoaded', function() {
    const flightInput = document.getElementById('id_flight_number');

    if (flightInput) {
        flightInput.addEventListener('change', function() {
            const flightNumber = this.value;
            if (!flightNumber) return;

            // Fetch flight details from your custom Django API view
            fetch(`/api/flight-info/?flight_number=${encodeURIComponent(flightNumber)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        if (data.origin) document.getElementById('id_origin').value = data.origin;
                        if (data.destination) document.getElementById('id_destination').value = data.destination;
                        if (data.operating_airline) document.getElementById('id_operating_airline').value = data.operating_airline;
                        // Populate datetime fields if returned (format: YYYY-MM-DD and HH:MM:SS)
                        if (data.departure_date) document.getElementById('id_departure_datetime_0').value = data.departure_date;
                        if (data.departure_time) document.getElementById('id_departure_datetime_1').value = data.departure_time;
                        if (data.arrival_date) document.getElementById('id_arrival_datetime_0').value = data.arrival_date;
                        if (data.arrival_time) document.getElementById('id_arrival_datetime_1').value = data.arrival_time;
                    }
                })
                .catch(err => console.error('Error fetching flight details:', err));
        });
    }
});

