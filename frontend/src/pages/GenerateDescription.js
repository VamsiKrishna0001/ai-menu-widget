import React, { useState } from 'react';
import { toast } from 'react-toastify';
import { foodDescriptionAPI } from '../services';
import {
  ToggleButtons,
  GenerateButton,
  FoodDescriptionCard
} from '../components';
import '../styles/App.css';

function GenerateDescription() {
  const [selectedModel, setSelectedModel] = useState('gpt-3.5-turbo');
  const [foodName, setFoodName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedFood, setGeneratedFood] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerateDescription = async () => {
    if (!foodName.trim()) {
      toast.error('Please enter a food item name');
      return;
    }

    setIsLoading(true);
    setError(null);
    setGeneratedFood(null);

    try {
      const data = await foodDescriptionAPI.generateDescription(
        foodName.trim(),
        selectedModel
      );
      setGeneratedFood(data);
      toast.success('Description generated successfully!');
    } catch (err) {
      setError(err.message || 'Failed to generate description');
      if (err.message.includes('Rate limit exceeded')) {
        toast.error('You have reached the limit. Try after 5 minutes.');
      } else if (err.message.includes('Server error')) {
        toast.error('Please try again after some time.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = async () => {
    if (!foodName.trim()) {
      toast.error('Please enter a food item name');
      return;
    }

    setIsLoading(true);
    setError(null);
    setGeneratedFood(null);

    try {
      const data = await foodDescriptionAPI.regenerateDescription(
        foodName.trim(),
        selectedModel
      );
      setGeneratedFood(data);
      toast.success('Description regenerated successfully!');
    } catch (err) {
      setError(err.message || 'Failed to regenerate description');
      if (err.message.includes('Rate limit exceeded')) {
        toast.error('You have reached the limit. Try after 5 minutes.');
      } else if (err.message.includes('Server error')) {
        toast.error('Please try again after some time.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="App-main">
      {/* Food Item Input with Toggle Buttons Above */}
      <div className="input-with-toggles">
        <div className="input-header">
          <label htmlFor="foodItemName">Food Item Name:</label>
          <ToggleButtons
            selectedModel={selectedModel}
            onModelChange={setSelectedModel}
          />
        </div>
        <input
          type="text"
          id="foodItemName"
          value={foodName}
          onChange={(e) => setFoodName(e.target.value)}
          placeholder="Enter food item name..."
          className="food-input"
        />
      </div>

      {/* Generate Description Button */}
      <GenerateButton
        selectedModel={selectedModel}
        isLoading={isLoading}
        onClick={handleGenerateDescription}
      />

      {/* Regenerate Button */}
      {generatedFood && (
        <button
          className={`generate-btn ${selectedModel === 'gpt-3.5-turbo' ? 'btn-light' : 'btn-dark'}`}
          onClick={handleRegenerate}
          disabled={isLoading}
          style={{ marginBottom: '1rem' }}
        >
          Regenerate Description
        </button>
      )}

      {/* Error Display */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {/* Generated Description Card */}
      <FoodDescriptionCard foodItem={generatedFood} />
    </main>
  );
}

export default GenerateDescription;
