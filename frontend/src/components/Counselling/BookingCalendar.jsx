import React, { useState } from 'react';

export const BookingCalendar = ({ counsellorId, onBooking }) => {
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTime, setSelectedTime] = useState(null);

  const handleBooking = async () => {
    if (selectedDate && selectedTime) {
      try {
        const response = await fetch('/api/counselling/book', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            counsellorId,
            date: selectedDate,
            time: selectedTime,
          }),
        });
        const data = await response.json();
        onBooking(data);
      } catch (error) {
        console.error('Error booking appointment:', error);
      }
    }
  };

  return (
    <div className="booking-calendar">
      <input type="date" onChange={(e) => setSelectedDate(e.target.value)} />
      <select onChange={(e) => setSelectedTime(e.target.value)}>
        <option>Select Time</option>
        <option>09:00 AM</option>
        <option>10:00 AM</option>
        <option>02:00 PM</option>
        <option>03:00 PM</option>
      </select>
      <button onClick={handleBooking}>Confirm Booking</button>
    </div>
  );
};
