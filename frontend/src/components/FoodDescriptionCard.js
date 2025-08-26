import React, { useState } from 'react';
import '../styles/FoodDescriptionCard.css';

const FoodDescriptionCard = ({ foodItem }) => {
  const [copyStatus, setCopyStatus] = useState({ description: false, upsell: false });

  if (!foodItem) return null;

  const copyToClipboard = async (text, type) => {
    try {
      // Try modern clipboard API first
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        // Fallback for older browsers or non-secure contexts
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        document.execCommand('copy');
        textArea.remove();
      }
      
      setCopyStatus(prev => ({ ...prev, [type]: true }));
      setTimeout(() => {
        setCopyStatus(prev => ({ ...prev, [type]: false }));
      }, 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
      // Show error feedback
      setCopyStatus(prev => ({ ...prev, [type]: 'error' }));
      setTimeout(() => {
        setCopyStatus(prev => ({ ...prev, [type]: false }));
      }, 2000);
    }
  };

  return (
    <div className="description-card">
      <div className="card-header">
        <h3 className="food-name">{foodItem.name}</h3>
        <span className="model-badge">{foodItem.model}</span>
      </div>
      
      <div className="card-content">
        <div className="description-section">
          <div className="section-header">
            <h4 className="description-title">Description</h4>
            <button
              className={`copy-btn ${copyStatus.description ? (copyStatus.description === 'error' ? 'error' : 'copied') : ''}`}
              onClick={() => copyToClipboard(foodItem.description, 'description')}
              title="Copy description"
            >
              {copyStatus.description === 'error' ? '❌ Error' : copyStatus.description ? '✓ Copied!' : '📋 Copy'}
            </button>
          </div>
          <p className="copyable-text">{foodItem.description}</p>
        </div>
        
        <div className="upsell-section">
          <div className="section-header">
            <h4 className="upsell-title">Upsell Suggestion</h4>
            <button
              className={`copy-btn ${copyStatus.upsell ? (copyStatus.upsell === 'error' ? 'error' : 'copied') : ''}`}
              onClick={() => copyToClipboard(foodItem.upsell, 'upsell')}
              title="Copy upsell suggestion"
            >
              {copyStatus.upsell === 'error' ? '❌ Error' : copyStatus.upsell ? '✓ Copied!' : '📋 Copy'}
            </button>
          </div>
          <p className="copyable-text">{foodItem.upsell}</p>
        </div>
      </div>
      
      <div className="card-footer">
        <span className="timestamp">
          Generated: {new Date(foodItem.timestamp).toLocaleString()}
        </span>
      </div>
    </div>
  );
};

export default FoodDescriptionCard;
