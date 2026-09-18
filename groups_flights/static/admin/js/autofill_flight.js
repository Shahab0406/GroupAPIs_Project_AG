(function() {
    console.log("=== AUTOFILL SCRIPT INITIALIZED ===");

    function triggerAutofill(input) {
        const rawValue = input.value.trim();
        if (!rawValue) return;

        const prefix = input.id.substring(0, input.id.lastIndexOf('flight_number'));

        const setFieldValue = (fieldName, value, dataObj = {}) => {
            if (value === undefined || value === null) return;
            const targetId = prefix + fieldName;
            let el = document.getElementById(targetId);

            // 1. Handle Readonly Fields (Standalone Form & Group Inline Table)
            if (!el) {
                const inlineRow = input.closest('tr, .form-row');
                let fieldWrapper = inlineRow ? inlineRow.querySelector(`.field-${fieldName}`) : null;

                if (!fieldWrapper) {
                    fieldWrapper = document.querySelector(`.field-${fieldName}`);
                }

                if (fieldWrapper) {
                    // Specific targeting: Label ko bypass karke sirf text wrapper (.readonly, .readonly-main, ya div.readonly-main) target karein
                    const targetContainer = fieldWrapper.querySelector('.readonly, div.readonly-main, p') || fieldWrapper;
                    
                    // Agar label aur text sibling hain, toh label tabahi se bache
                    if (targetContainer.classList.contains(`field-${fieldName}`) && targetContainer.tagName === 'TD') {
                        targetContainer.textContent = dataObj.airline_display || value;
                    } else {
                        // Standard Django Admin form-row context
                        const textNode = targetContainer.querySelector('div') || targetContainer;
                        textNode.textContent = dataObj.airline_display || value;
                    }
                }
                return;
            }

            // 2. Direct Input / Select Value Assignment
            el.value = value;

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

            // Dispatch DOM & Select2 Events
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('input', { bubbles: true }));
            if (window.jQuery) {
                window.jQuery(el).trigger('change').trigger('change.select2');
            }

            // Visual Lock for dropdowns
            if (fieldName === 'airline') {
                el.style.pointerEvents = 'none';
                el.style.backgroundColor = '#f2f2f2';
                el.tabIndex = -1;
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

            // Foreign Key Airline ID & Display
            setFieldValue('airline', data.airline, data);

            // Flight attributes
            setFieldValue('origin', data.origin, data);
            setFieldValue('destination', data.destination, data);

            // Times populates automatically (_1)
            const dep = parseDateTime(data.departure_datetime || data.departure_date);
            setFieldValue('departure_datetime_1', data.departure_time || dep.time, data);

            const arr = parseDateTime(data.arrival_datetime || data.arrival_date);
            setFieldValue('arrival_datetime_1', data.arrival_time || arr.time, data);
        })
        .catch(err => console.error("Autofill fetch error:", err));
    }

    document.addEventListener('focusout', function(e) {
        if (e.target && e.target.id && e.target.id.includes('flight_number')) {
            triggerAutofill(e.target);
        }
    });
})();