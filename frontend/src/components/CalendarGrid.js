// components/CalendarGrid.js
import React from 'react';

const CalendarGrid = ({ dates, onSelectDate, selectedDate }) => {
  return (
    <div className="calendar-grid">
      {dates.map((date) => (
        <button
          key={date}
          className={selectedDate === date ? 'selected' : ''}
          onClick={() => onSelectDate(date)}
        >
          {new Date(date).toLocaleDateString('kk-KZ')}
        </button>
      ))}
    </div>
  );
};

export default CalendarGrid;
