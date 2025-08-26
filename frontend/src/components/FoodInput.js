import React from 'react';
import './FoodInput.css';

const FoodInput = ({ foodName, onFoodNameChange }) => {
  return (
    <div className="input-container">
      <label htmlFor="foodItemName">Food Item Name:</label>
      <input
        type="text"
        id="foodItemName"
        value={foodName}
        onChange={(e) => onFoodNameChange(e.target.value)}
        placeholder="Enter food item name..."
        className="food-input"
      />
    </div>
  );
};

export default FoodInput;
