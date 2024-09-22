# ReviewLensAI
AI-powered product review analyzer that reduces the time spent reading online reviews by 80%.

It help you make faster, more informed purchase decisions by automatically extracting, analyzing, and summarizing online reviews. Powered by IBM’s watsonx.ai granite-13b-chat-v2 foundation model.

## Features
- **Structured Review Insights**: Collects and summarizes product reviews into concise, actionable insight.
- **Sentiment Analysis**: Analyzes the reviews to determine how the product is generally viewed by customers.
- **Chat**: uses LangChain for context-aware coherent conversation, enabling you to ask follow-up questions.
- **Product Comparison**: Side-by-side review based comparison.

## Getting Started

### Prerequisites

- Python 3.9+
- IBM watsonx API Key

### Installation

1. Clone the repo
```bash
git clone https://github.com/asutoshranjan/ReviewLensAI
cd ReviewLensAI
```

2. Create a virtual environment and install the dependencies from `requirements.txt`
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add the following environment variables
```bash
SBR_WEBDRIVER="YOUR_WEBDRIVER_URL"
WATSONX_APIKEY="YOUR_API_KEY"
PROJECT_ID="YOUR_PROJECT_ID"
```

4. Run the app
```bash
streamlit run main.py
```
