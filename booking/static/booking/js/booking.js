



$(function() {
    let endpoint = "booking/"
    const calendarEl = $('#calendar')[0];
    const timeSlotSelect = $('#timeSlot');
    const selectedDateInput = $('#selectedDate');
    const bookingModal = $('#bookingModal');
    const bookingForm = $('#bookingForm');
    
    /* GET CSRF COOKIE
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    } */
    
    // GENERATE TIME SLOTS
    function generateTimeSlots(bookedTimes) {
        const startHour = 9;
        const endHour = 17;
        for (let hour = startHour; hour < endHour; hour++) {
            for (let minute = 0; minute < 60; minute += 15) {
                const timeString = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
                const timeValue = `${timeString}:00`;
                if (bookedTimes.includes(timeValue)) continue;
                $('<option>', {
                    value: timeValue,
                    text: timeString
                }).appendTo(timeSlotSelect);
            }
        }
    };
    
    // HANDLE DATA CLICKING
    
    
    // HANDLE FORM SUBMISSION
    function bookingFormSubmission(e) {
        console.log("Starting booking form submission...")
        e.preventDefault();
        const formData = $(this).serializeArray();
        console.log(`Serialized form data: ${formData}`)
        let data = {};
        $.each(formData, function(_, field) {
            data[field.name] = field.value;
        });
        console.log(`DATA: ${data}`)
        let url = endpoint + selectedDateInput.val() + "/";
        data.date = selectedDateInput.val();
        
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        })
        .then(response => response.data)
        .then(data => {
            console.log('Success:', data);
            bookingModal.modal('hide');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };
    

    // FORMAT NON-SELECTABLE BOOKINGS
    
    

    

    // Calander Init
    let calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        weekends: false,
        contentHeight: 'auto',
        selectOverlap: false,
        validRange: {
            start: new Date()
        },
        dayCellClassNames: function(arg) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            return arg.date < today ? 'fc-past-disabled' : '';
        },
        selectAllow: function(selectInfo) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const isOneDaySelection = selectInfo.start.getTime() === selectInfo.end.getTime() - 86400000;
            const isNotPastDate = selectInfo.start >= today;
            return isOneDaySelection && isNotPastDate;
        }

    });
    
    calendar.render()

    // Handle form submission
    bookingForm.on('submit', 
        {e: this}, 
        bookingFormSubmission
    );

    bookingModal.on('shown.bs.modal', function() {
        calendar.updateSize();
    });
    
});


/*dateClick: function(info) {
            
    const selectedDate = info.date
    console.log()
    console.log('Selected date:', selectedDate);
    selectedDateInput.val(selectedDate);
    let url = endpoint + selectedDate + "/";
    timeSlotSelect.html('<option value="" disabled>Loading times...</option>');
    
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Available times data:', data);
        timeSlotSelect.html('<option value="">Select a time</option>');
        generateTimeSlots(data.booked_times || []);
    })
    console.log("Completed time fetch")
},

selectAllow: function(selectInfo) {
    bookingSelectAllow(selectInfo)
}*/