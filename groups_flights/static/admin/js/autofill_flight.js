(function() {
    console.log("=== AUTOFILL SCRIPT INITIALIZED ===");

    function triggerAutofill(input) {
        const flightNumber = input.value.trim();
        if (!flightNumber) return;

        console.log("Processing flight number:", flightNumber);

        // Find prefix (e.g., 'id_' for standard form, 'id_flights-0-' for inlines)
        const inputId = input.id;
        const prefix = inputId.substring(0, inputId.lastIndexOf('flight_number'));

        const setFieldValue = (fieldName, value) => {
            if (value === undefined || value === null) return;
            const targetId = prefix + fieldName;
            const el = document.getElementById(targetId);
            if (el) {
                el.value = value;
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.dispatchEvent(new Event('input', { bubbles: true }));
                console.log(`Updated ${targetId} -> ${value}`);
            }
        };

        const parseDateTime = (dtStr) => {
            if (!dtStr) return { date: '', time: '' };
            const str = String(dtStr);
            const [date, fullTime] = str.includes('T') ? str.split('T') : str.split(' ');
            const time = fullTime ? fullTime.substring(0, 8) : '';
            return { date: date || '', time: time || '' };
        };

        const apiUrl = `/api/flight-info/?flight_number=${encodeURIComponent(flightNumber)}`;
        console.log("Fetching from API:", apiUrl);

        fetch(apiUrl, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            },
            credentials: 'same-origin'
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(response => {
            const segment = response.data || response;
            if (segment) {
                console.log("Segment data received:", segment);

                // Origin & Destination
                setFieldValue('origin', segment.origin);
                setFieldValue('destination', segment.destination);

                // Departure Datetime
                const dep = parseDateTime(segment.departure_datetime || segment.departure_date);
                setFieldValue('departure_datetime_1', segment.departure_time || dep.time);
                // Arrival Datetime
                const arr = parseDateTime(segment.arrival_datetime || segment.arrival_date);
                setFieldValue('arrival_datetime_1', segment.arrival_time || arr.time);
            }
        })
        .catch(err => console.error("Autofill fetch error:", err));
    }

    // Attach delegated event listeners
    document.addEventListener('change', function(e) {
        if (e.target && e.target.id && e.target.id.includes('flight_number')) {
            triggerAutofill(e.target);
        }
    });

    document.addEventListener('focusout', function(e) {
        if (e.target && e.target.id && e.target.id.includes('flight_number')) {
            triggerAutofill(e.target);
        }
    });
})();