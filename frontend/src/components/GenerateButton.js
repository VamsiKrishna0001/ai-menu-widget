import React from 'react';
import '../styles/GenerateButton.css';

const GenerateButton = ({ selectedModel, isLoading, onClick }) => {
  return (
    <button
      className={`generate-btn ${selectedModel === 'gpt-3.5-turbo' ? 'btn-light' : 'btn-dark'}`}
      onClick={onClick}
      disabled={isLoading}
    >
      {isLoading ? (
        <div className="loading-content">
          <div className="spinner"></div>
          <span>Generating...</span>
        </div>
      ) : (
        'Generate Description'
      )}
    </button>
  );
};

export default GenerateButton;
