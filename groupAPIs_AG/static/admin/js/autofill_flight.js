document.addEventListener('DOMContentLoaded', function() {
    const flightInput = document.getElementById('id_flight_number');

    if (flightInput) {
        // Listen for when the user leaves the input box or changes value
        flightInput.addEventListener('change', function() {
            const flightNumber = this.value.trim();
            if (!flightNumber) return;

            // Make request to the API
            fetch(`/api/flight-info/?flight_number=${encodeURIComponent(flightNumber)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Text fields
                        if (data.origin) document.getElementById('id_origin').value = data.origin;
                        if (data.destination) document.getElementById('id_destination').value = data.destination;
                        if (data.operating_airline) document.getElementById('id_operating_airline').value = data.operating_airline;
                        if (data.marketing_airline && document.getElementById('id_marketing_airline')) {
                            document.getElementById('id_marketing_airline').value = data.marketing_airline;
                        }

                        // Split DateTime fields (Date = _0, Time = _1)
                        if (data.departure_date) document.getElementById('id_departure_datetime_0').value = data.departure_date;
                        if (data.departure_time) document.getElementById('id_departure_datetime_1').value = data.departure_time;
                        if (data.arrival_date) document.getElementById('id_arrival_datetime_0').value = data.arrival_date;
                        if (data.arrival_time) document.getElementById('id_arrival_datetime_1').value = data.arrival_time;
                    }
                })
                .catch(err => console.error('Autofill Error:', err));
        });
    }
});