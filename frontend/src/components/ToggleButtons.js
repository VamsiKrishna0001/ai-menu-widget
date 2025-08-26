import React from 'react';
import '../styles/ToggleButtons.css';

const ToggleButtons = ({ selectedModel, onModelChange }) => {
  return (
    <div className="toggle-container">
      <button
        className={`toggle-btn ${selectedModel === 'gpt-3.5-turbo' ? 'toggle-a-active' : 'toggle-a-inactive'}`}
        onClick={() => onModelChange('gpt-3.5-turbo')}
      >
        GPT-3.5 Turbo
      </button>
      <button
        className={`toggle-btn ${selectedModel === 'gpt-4.1-mini' ? 'toggle-b-active' : 'toggle-b-inactive'}`}
        onClick={() => onModelChange('gpt-4.1-mini')}
      >
        GPT-4.1 Mini
      </button>
    </div>
  );
};

export default ToggleButtons;
