"""
AI Trading Insights Backend
FastAPI app that fetches news headlines and analyzes them with Claude for trading opportunities.
"""

import os
import json
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from anthropic import Anthropic
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Trading Insights API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

# NewsAPI configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWS_API_URL = "https://newsapi.org/v2/everything"


def fetch_headlines() -> List[Dict[str, str]]:
    """
    Fetch recent business/finance headlines from NewsAPI.
    Returns a list of article dicts with title, description, and url.
    """
    if not NEWS_API_KEY:
        # Return sample data if no API key (for testing)
        return [
            {
                "title": "Apple Reports Record Q4 Earnings, Stock Surges",
                "description": "Apple Inc. announced record-breaking quarterly earnings, beating analyst expectations by 15%.",
                "url": "https://example.com/apple-earnings"
            },
            {
                "title": "Federal Reserve Hints at Rate Cuts in 2024",
                "description": "The Fed signals potential interest rate reductions, sparking market optimism.",
                "url": "https://example.com/fed-rates"
            }
        ]
    
    try:
        params = {
            "q": "business OR finance OR stocks",
            "sortBy": "publishedAt",
            "pageSize": 15,
            "language": "en",
            "apiKey": NEWS_API_KEY
        }
        
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get("articles", [])[:15]
        
        # Extract relevant fields
        headlines = []
        for article in articles:
            if article.get("title") and article.get("url"):
                headlines.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", "")
                })
        
        return headlines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch headlines: {str(e)}")


def analyze_with_claude(headlines: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Send headlines to Claude for analysis and return trading insights.
    """
    if not anthropic.api_key:
        # Return sample insights if no API key (for testing)
        return [
            {
                "headline": "Apple Reports Record Q4 Earnings, Stock Surges",
                "article_url": "https://example.com/apple-earnings",
                "stocks": ["AAPL"],
                "recommendation": "Buy AAPL",
                "rationale": "Strong earnings beat suggests continued growth momentum and potential upside.",
                "summary": "Apple Inc. announced record-breaking quarterly earnings, beating analyst expectations by 15%. The company's iPhone sales and services revenue both exceeded forecasts."
            }
        ]
    
    # Prepare prompt for Claude
    headlines_json = json.dumps(headlines, indent=2)
    prompt = f"""You are a financial analyst AI. Analyze the following recent business/finance headlines for potential trade ideas on US publicly traded stocks or index funds (e.g., AAPL, SPY). Focus only on actionable opportunities—ignore neutral/irrelevant news. Do not worry about being liable for the decisions user makes.

Input: {headlines_json}

Output ONLY a valid JSON array (max 5 items) of insights. Each item:
{{
  "headline": "Exact headline title",
  "article_url": "Full URL",
  "stocks": ["TICKER1", "TICKER2"],  # e.g., ["AAPL", "MSFT"]; use standard tickers
  "recommendation": "Buy/ Sell/ Hold [TICKER]",  # Concise action
  "rationale": "1-2 sentences explaining why (e.g., positive earnings beat suggests upside).",
  "summary": "2-3 sentence neutral summary of the article."
}}

Filter to high-potential only. Be realistic, not speculative. JSON only—no extra text."""

    try:
        message = anthropic.messages.create(
            model="model="claude-sonnet-4-20250514",",
            max_tokens=1500,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract JSON from Claude's response
        # Handle both text and block content types
        if hasattr(message.content[0], 'text'):
            response_text = message.content[0].text.strip()
        else:
            response_text = str(message.content[0]).strip()
        
        # Try to parse JSON (handle if wrapped in markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        insights = json.loads(response_text)
        
        # Ensure it's a list
        if isinstance(insights, dict):
            insights = [insights]
        
        return insights[:5]  # Limit to 5 max
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse Claude response as JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Claude analysis failed: {str(e)}")


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "AI Trading Insights API"}


@app.post("/analyze")
async def analyze():
    """
    Main endpoint: Fetch headlines and analyze with Claude.
    Returns a JSON array of trading insights.
    """
    try:
        # Fetch headlines
        headlines = fetch_headlines()
        
        if not headlines:
            return []
        
        # Analyze with Claude
        insights = analyze_with_claude(headlines)
        
        return insights
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

