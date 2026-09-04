document.addEventListener('DOMContentLoaded', function() {
    // Event delegation to catch changes on both main form and dynamically added inline rows
    document.addEventListener('change', function(event) {
        const input = event.target;

        // Check if the changed element is a flight_number field
        if (input && input.id && input.id.endsWith('flight_number')) {
            const flightNumber = input.value.trim();
            if (!flightNumber) return;

            // Extract row prefix (e.g., 'id_' or 'id_flights-0-')
            const prefix = input.id.substring(0, input.id.lastIndexOf('flight_number'));

            // Helper function to safely set field value by field name
            const setFieldValue = (fieldName, value) => {
                const element = document.getElementById(prefix + fieldName);
                if (element && value) {
                    element.value = value;
                }
            };

            // Fetch flight details from your API
            fetch(`/api/flight-info/?flight_number=${encodeURIComponent(flightNumber)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response failed');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Sector fields
                        setFieldValue('origin', data.origin);
                        setFieldValue('destination', data.destination);

                        // Split DateTime fields (Date = _0, Time = _1)
                        setFieldValue('departure_datetime_0', data.departure_date);
                        setFieldValue('departure_datetime_1', data.departure_time);
                        setFieldValue('arrival_datetime_0', data.arrival_date);
                        setFieldValue('arrival_datetime_1', data.arrival_time);
                    }
                })
                .catch(err => console.error('Flight Autofill Error:', err));
        }
    });
});