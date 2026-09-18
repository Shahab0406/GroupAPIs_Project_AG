(function() {
    console.log("=== AUTOFILL SCRIPT INITIALIZED ===");

    function triggerAutofill(input) {
        const rawValue = input.value.trim();
        if (!rawValue) return;

        const prefix = input.id.substring(0, input.id.lastIndexOf('flight_number'));

        const setFieldValue = (fieldName, value) => {
            if (value === undefined || value === null) return;
            const el = document.getElementById(prefix + fieldName);
            if (!el) return;

            // 1. Direct Assignment (Primary Key ID or standard text)
            el.value = value;

            // 2. Select Option Fallback by text matching if ID didn't match directly
            if (el.tagName === 'SELECT' && el.value !== String(value)) {
                const searchStr = String(value).trim().toLowerCase();
                for (let i = 0; i < el.options.length; i++) {
                    const opt = el.options[i];
                    if (opt.text.toLowerCase().includes(searchStr) || opt.value.toLowerCase() === searchStr) {
                        el.selectedIndex = i;
                        break;
                    }
                }
            }

            // 3. Dispatch native DOM and Django Admin Select2 events
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('input', { bubbles: true }));
            if (window.jQuery) {
                window.jQuery(el).trigger('change').trigger('change.select2');
            }
        };

        const parseDateTime = (dtStr) => {
            if (!dtStr) return { date: '', time: '' };
            const [date, fullTime] = String(dtStr).includes('T') ? dtStr.split('T') : dtStr.split(' ');
            return { date: date || '', time: fullTime ? fullTime.substring(0, 8) : '' };
        };

        fetch(`/api/flight-info/?flight_number=${encodeURIComponent(rawValue)}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' },
            credentials: 'same-origin'
        })
        .then(res => res.ok ? res.json() : null)
        .then(response => {
            if (!response) return;
            const data = response.data || response;

            // Foreign Key Airline ID
            setFieldValue('airline', data.airline);

            // Flight segment attributes
            setFieldValue('origin', data.origin);
            setFieldValue('destination', data.destination);

            const dep = parseDateTime(data.departure_datetime || data.departure_date);
            // setFieldValue('departure_datetime_0', dep.date);
            setFieldValue('departure_datetime_1', data.departure_time || dep.time);

            const arr = parseDateTime(data.arrival_datetime || data.arrival_date);
            // setFieldValue('arrival_datetime_0', arr.date);
            setFieldValue('arrival_datetime_1', data.arrival_time || arr.time);
        })
        .catch(err => console.error("Autofill fetch error:", err));
    }

    document.addEventListener('focusout', function(e) {
        if (e.target && e.target.id && e.target.id.includes('flight_number')) {
            triggerAutofill(e.target);
        }
    });
})();