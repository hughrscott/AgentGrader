# Agent Grader

An MCP-compliant answer grading system built with Gradio and Hugging Face Transformers.

## Description

This project provides an API for grading answers to questions using a large language model. It follows the Model Context Protocol (MCP) for LLM integration, making it compatible with agentic systems.

## Features

- Gradio web interface for easy testing
- MCP-compliant API endpoint
- Uses Hugging Face's GPT-2 model for answer evaluation
- Returns structured grading results (A-F) with justifications

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

3. Access the web interface at http://localhost:7860

## API Usage

Send a POST request to the endpoint with the following JSON structure:

```json
{
    "question": "Your question here",
    "context": "Relevant context",
    "answer": "Answer to grade",
    "reference_answer": "Correct reference answer"
}
```

The API will return a JSON response with:
- grade (A-F)
- justification
- hallucination_detected (true/false)

## Deployment

This project is configured for deployment on Hugging Face Spaces. The Gradio interface will be automatically available when deployed.
