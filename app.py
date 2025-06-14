import gradio as gr
from grader_agent import AnswerGraderAgent
import requests
import json

def get_model():
    print("Initializing Ollama phi model...")
    try:
        def generate_text(prompt):
            try:
                # Call Ollama API
                response = requests.post('http://localhost:11434/api/generate',
                    json={
                        "model": "phi",
                        "prompt": prompt,
                        "stream": False
                    })
                response.raise_for_status()
                return response.json()['response']
            except Exception as e:
                print(f"Error generating text: {str(e)}")
                raise Exception(f"Text generation failed: {str(e)}")
        
        return generate_text
        
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        raise Exception(f"Failed to initialize model: {str(e)}")

print("Setting up model...")
model = get_model()
print("Model setup complete!")

print("Creating agent...")
agent = AnswerGraderAgent(model=model)
print("Agent created successfully!")

def mcp_endpoint(input_data):
    """
    MCP endpoint for answer grading.
    Expected input format:
    {
        "question": str,
        "context": str,
        "answer": str,
        "reference_answer": str
    }
    """
    try:
        # Validate input
        required_fields = ["question", "context", "answer", "reference_answer"]
        for field in required_fields:
            if field not in input_data:
                return {
                    "error": f"Missing required field: {field}",
                    "status": "error"
                }
        
        # Run the grading
        result = agent.run(input_data)
        
        # Format the response
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Create the Gradio interface
app = gr.Interface(
    fn=mcp_endpoint,
    inputs=gr.JSON(label="Input Data"),
    outputs=gr.JSON(label="Grading Result"),
    title="Answer Grader MCP Server",
    description="Grade answers using the MCP protocol. Input should be a JSON object with question, context, answer, and reference_answer fields.",
    examples=[
        {
            "question": "What did Tesla announce about batteries in 2022?",
            "context": "Tesla announced 4680 battery cells and a production ramp-up at Battery Day.",
            "answer": "They started making trucks in Germany.",
            "reference_answer": "Tesla announced the new 4680 battery cells and increased production capacity."
        }
    ]
)

# For local testing
if __name__ == "__main__":
    app.launch()
