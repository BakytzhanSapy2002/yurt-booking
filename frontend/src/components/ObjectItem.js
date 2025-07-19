// components/ObjectItem.js
import React from 'react';

const ObjectItem = ({ obj, onClick }) => {
  const color = obj.Status === 'free' ? '#4CAF50' : '#F44336';

  return (
    <div
      className="object-item"
      onClick={() => onClick(obj)}
      style={{
        backgroundColor: color,
        color: 'white',
        padding: '8px 12px',
        margin: '4px',
        borderRadius: '5px',
        minWidth: '50px',
        textAlign: 'center',
        cursor: 'pointer'
      }}
    >
      {obj.Number}
    </div>
  );
};

export default ObjectItem;
