# AI-Powered Menu Intelligence Widget - Frontend

A React.js frontend application for the AI-Powered Menu Intelligence Widget that allows users to generate food item descriptions with toggle-based styling.

## Features

- **Toggle Buttons**: Two toggle options (GPT 3.5 and GPT 4) with visual color changes
- **Food Item Input**: Text input field for entering food item names
- **Generate Description Button**: Button that changes color based on selected toggle
- **Responsive Design**: Mobile-friendly interface with modern UI

## Visual Features
- **Modern UI**: Gradient backgrounds, shadows, and smooth transitions

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd "frontend"
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

```

## Future Enhancements

- Integration with backend API for actual AI-powered descriptions
- User authentication and history
- Advanced food item categorization
- Export functionality for generated descriptions

## Technologies Used

- React 18.2.0
- React-toastify
- CSS3 with modern features (gradients, transitions, backdrop-filter)
- Create React App for project scaffolding


# AI-Powered Menu Intelligence Widget - Backend

A FastAPI backend application for the AI-Powered Menu Intelligence Widget that provides API endpoints for generating food item descriptions with intelligent caching and data persistence.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Pydantic Models**: Advanced data validation and serialization using Pydantic
- **Intelligent Caching**: Automatic caching of generated descriptions with cache hit tracking
- **Data Persistence**: JSON-based storage for all generated descriptions
- **CORS Support**: Configured to work with the React frontend
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Comprehensive Error Handling**: Detailed error handling with HTTP status codes
- **Logging**: Structured logging for debugging and monitoring

## Project Structure

```
backend/
├── main.py                    # Main FastAPI application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── schemas/                  # Pydantic data models
│   ├── __init__.py
│   └── food_item.py         # Food item request/response models
├── models/                   # Business logic and data management
│   ├── __init__.py
│   └── food_item_manager.py # Data storage and caching manager
└── routes/                   # API route handlers
    ├── __init__.py
    └── generate.py          # Generate description routes
```

## API Endpoints

### POST `/api/v1/generate-description`
Generate a description and upsell message for a food item based on the model selection.

**Request Body:**
```json
{
  "name": "Margherita Pizza",
  "model": "A"
}
```

**Response:**
```json
{
  "name": "Margherita Pizza",
  "model": "A",
  "description": "A delightful Margherita Pizza that brings light and freshness...",
  "upsell": "Pair your Margherita Pizza with our signature house salad...",
  "success": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET `/`
Root endpoint with API information.

### GET `/health`
Health check endpoint.

### GET `/api-info`
Detailed API information and endpoint documentation.

## Pydantic Models

### FoodItemRequest
- `name` (str): Name of the food item (1-100 characters, validated and sanitized)
- `model` (str): Model selection (A or B)

### FoodItemResponse
- `name` (str): Name of the food item
- `model` (str): Selected model option
- `description` (str): Generated description
- `upsell` (str): Generated upsell message
- `success` (bool): Success status
- `timestamp` (datetime): Generation timestamp

### FoodItemHistory
- `id` (Optional[int]): Unique identifier
- `name` (str): Name of the food item
- `model` (str): Model used for generation
- `description` (str): Generated description
- `upsell` (str): Generated upsell message
- `created_at` (datetime): Creation timestamp
- `usage_count` (int): Number of times this item was requested

### FoodItemCache
- `name` (str): Name of the food item
- `model` (str): Model used for generation
- `description` (str): Generated description
- `upsell` (str): Generated upsell message
- `last_accessed` (datetime): Last access timestamp
- `access_count` (int): Number of times accessed

## Data Validation and Sanitization

The API includes comprehensive validation and sanitization:

- **Name Validation**: Checks for valid characters, length limits, and removes extra whitespace
- **Model Validation**: Ensures only valid model options (A or B) are accepted
- **Input Sanitization**: Automatically cleans and normalizes input data
- **Error Handling**: Provides detailed error messages for validation failures

## Caching Implementation

The backend implements intelligent caching:

- **Automatic Caching**: All generated descriptions are automatically cached
- **Cache Hit Tracking**: Monitors cache performance and access patterns
- **Persistent Storage**: Cache data persists between application restarts
- **Cache Management**: Provides endpoints to view cache stats and clear old entries
- **Performance Optimization**: Reduces response time for frequently requested items

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Navigate to the backend directory:
   ```bash
   cd "AI-Powered Menu Intelligence Widget/backend"
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Access the API:
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative API docs: http://localhost:8000/redoc

## Development

### Running with Auto-reload
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API
You can test the API using the interactive documentation at `/docs` or using tools like:
- curl
- Postman
- Insomnia
- HTTPie

### Example curl commands

```bash
# Generate description
curl -X POST "http://localhost:8000/api/v1/generate-description" \
     -H "Content-Type: application/json" \
     -d '{"name": "Margherita Pizza", "model": "A"}'

```

## Data Storage

The application uses JSON files for data persistence:
- `food_items_data.json`: Stores all generated descriptions and metadata
- `food_items_cache.json`: Stores cached descriptions for quick access

Both files are automatically created and managed by the application.

## Future Enhancements

- Integration with actual AI models for description generation
- Database integration (PostgreSQL, MongoDB)
- User authentication and rate limiting
- Advanced food item categorization
- Machine learning model training endpoints
- Redis integration for distributed caching
- API versioning and migration tools

## Technologies Used

- FastAPI 0.104.1
- Pydantic 2.5.0
- Uvicorn (ASGI server)
- Python 3.8+
- JSON for data persistence
