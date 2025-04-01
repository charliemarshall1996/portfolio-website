

document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const timeSlotSelect = document.getElementById('timeSlot');
    const selectedDateInput = document.getElementById('selectedDate');
    
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        weekends: false,
        contentHeight: 'auto',
        select: function(info) {
            const selectedDate = info.startStr;
            console.log('Selected date:', selectedDate);
            selectedDateInput.value = selectedDate;
            
            // Clear previous time slots
            timeSlotSelect.innerHTML = '<option value="">Select a time</option>';
            
            // Initialize request to get booked times
            var req = new XMLHttpRequest();
            req.open('GET', ApiUrl.replace('all', selectedDate));
            req.onload = function() {
                if (req.status === 200) {
                    const bookedTimes = JSON.parse(req.responseText).map(booking => booking.time);
                    generateTimeSlots(bookedTimes);
                }
            };
            req.send();
        },
        selectOverlap: false,
        selectAllow: function(selectInfo) {
            return selectInfo.start.getTime() === selectInfo.end.getTime() - 86400000;
        }
    });
    
    calendar.render();

    document.getElementById('bookingModal').addEventListener('shown.bs.modal', () => {
        calendar.updateSize();
    });
    
    // Generate time slots from 09:00 to 17:00 in 15-minute increments
    function generateTimeSlots(bookedTimes) {
        const startHour = 9;
        const endHour = 17;
        
        for (let hour = startHour; hour < endHour; hour++) {
            for (let minute = 0; minute < 60; minute += 15) {
                const timeString = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
                const timeValue = `${timeString}:00`;
                
                // Skip if this time is already booked
                if (bookedTimes.includes(timeValue)) continue;
                
                const option = document.createElement('option');
                option.value = timeValue;
                option.textContent = timeString;
                timeSlotSelect.appendChild(option);
            }
        }
    }
    
    // Handle form submission
    document.getElementById('bookingForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());
        
        // Include the selected date
        data.date = selectedDateInput.value;
        
        // Send POST request
        var req = new XMLHttpRequest();
        req.open('POST', ApiUrl.replace('all', data.date));
        req.setRequestHeader('Content-Type', 'application/json');
        req.onload = function() {
            if (req.status === 201) {
                alert('Booking successful!');
                // Optionally refresh the calendar or close the modal
            } else {
                alert('Error booking appointment');
            }
        };
        req.send(JSON.stringify(data));
    });
});

