// components/ObjectView.js
import React from 'react';
import ObjectItem from './ObjectItem';

const ObjectView = ({ data, onSelectObject }) => {
  const categories = {
    "Үлкен тапчан": { type: "Tapchan", size: "Large", price: 15000 },
    "Кіші тапчан": { type: "Tapchan", size: "Small", price: 8000 },
    "Үлкен киіз үй": { type: "Yurt", size: "Large", price: 40000 },
    "Кіші киіз үй": { type: "Yurt", size: "Small", price: 25000 },
  };

  return (
    <div className="object-view">
      {Object.entries(categories).map(([label, filter]) => {
        const objects = data.filter(obj =>
          obj.Type === filter.type && obj.Size === filter.size
        );
        return (
          <div key={label}>
            <h3>{label} – {filter.price} тг</h3>
            <div className="object-list">
              {objects.map((obj) => (
                <ObjectItem key={obj.Number} obj={obj} onClick={onSelectObject} />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ObjectView;
