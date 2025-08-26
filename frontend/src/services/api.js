const API_BASE_URL = 'http://localhost:8000/api/v1';

export const foodDescriptionAPI = {

  generateDescription: async (name, model) => {
    const response = await fetch(`${API_BASE_URL}/generate-description`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, model })
    });

    if (!response.ok) {
      if (response.status === 429) {
        throw new Error('Rate limit exceeded. Please wait before trying again.');
      } else if (response.status === 500) {
        throw new Error('Server error. Please try again later.');
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  regenerateDescription: async (name, model) => {
    const response = await fetch(`${API_BASE_URL}/regenerate-description`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, model })
    });

    if (!response.ok) {
      if (response.status === 429) {
        throw new Error('Rate limit exceeded. Please wait before trying again.');
      } else if (response.status === 500) {
        throw new Error('Server error. Please try again later.');
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
};
