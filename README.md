# AI Trading Insights

A hackathon-ready demo app that analyzes recent business/finance headlines using AI to identify potential trading opportunities for US stocks and index funds.

## Overview

This app demonstrates a complete AI-powered workflow:
1. Fetches recent business/finance headlines from NewsAPI
2. Analyzes them with Claude (Anthropic AI) to extract trading insights
3. Displays actionable recommendations in a clean, responsive dashboard

Perfect for hackathon demos—click a button and see live analysis results in ~30 seconds!

## Features

- **Real-time News Analysis**: Fetches 10-15 recent headlines from NewsAPI
- **AI-Powered Insights**: Uses Claude 3.5 Sonnet to identify trading opportunities
- **Clean Dashboard**: Responsive grid layout with trading cards
- **Actionable Recommendations**: Buy/Sell/Hold suggestions with rationale
- **Robinhood Integration**: Direct links to view stocks on Robinhood

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript + Vite
- **AI**: Anthropic Claude 3.5 Sonnet
- **News API**: NewsAPI.org

## Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- API Keys:
  - [Anthropic API Key](https://console.anthropic.com/)
  - [NewsAPI Key](https://newsapi.org/register)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory:
```env
ANTHROPIC_API_KEY=your_anthropic_key_here
NEWS_API_KEY=your_newsapi_key_here
```

5. Start the backend server:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Usage

1. **Start both servers** (backend on port 8000, frontend on port 3000)
2. **Open the app** in your browser at `http://localhost:3000`
3. **Click "Run Analysis"** to fetch headlines and analyze with AI
4. **View insights** in the dashboard grid

## Demo Tips

- **For Hackathons**: The app works with sample data if API keys aren't configured, so you can demo even without keys
- **Live Demo**: Click the button and show judges the loading state → results flow
- **Explain the Flow**: "We fetch headlines, send them to Claude AI, and get actionable trading insights"
- **Show Features**: Point out the recommendation badges, rationale, and Robinhood links

## Project Structure

```
.
├── backend/
│   ├── app.py            # FastAPI backend
│   ├── requirements.txt  # Python dependencies
│   ├── .env.example      # Environment variables template
│   ├── .env              # Your API keys (not in git)
│   └── venv/             # Python virtual environment
├── frontend/
│   ├── package.json      # Node dependencies
│   ├── vite.config.ts    # Vite configuration
│   ├── tsconfig.json     # TypeScript config
│   ├── index.html        # HTML entry point
│   └── src/
│       ├── App.tsx       # Main React component
│       ├── main.tsx      # React entry point
│       └── index.css     # Styles
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## API Endpoints

- `GET /` - Health check
- `POST /analyze` - Fetch headlines and analyze with Claude

## Notes

- The app uses CORS middleware to allow frontend-backend communication
- Sample data is returned if API keys are missing (for testing)
- Claude is configured with `temperature=0.3` for consistent, concise output
- Maximum 5 insights are returned per analysis

## License

MIT - Hackathon project

