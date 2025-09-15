from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def format_math_response(response_text):
    """
    Clean and format the response to properly display mathematical expressions
    """
    formatted_text = response_text.strip()
    
    # Clean up any hash symbols or unwanted characters
    formatted_text = formatted_text.replace('#', '')
    
    # Ensure proper spacing around mathematical expressions
    formatted_text = re.sub(r'(\d+)\s*x', r'$\1x$', formatted_text)
    formatted_text = re.sub(r'x\s*=\s*(\d+)', r'$x = \1$', formatted_text)
    formatted_text = re.sub(r'(\d+x\s*[+\-]\s*\d+\s*=\s*\d+)', r'$\1$', formatted_text)
    
    # Fix step formatting
    formatted_text = re.sub(r'\*\*(Step\s*\d+)\*\*\s*:', r'**\1:**', formatted_text)
    formatted_text = re.sub(r'\*\*(Solution)\*\*\s*:', r'**\1:**', formatted_text)
    formatted_text = re.sub(r'\*\*(Final Answer)\*\*\s*:', r'**\1:**', formatted_text)
    
    # Ensure proper line breaks between sections
    formatted_text = re.sub(r'(\*\*(?:Step\s*\d+|Solution|Final Answer):\*\*)', r'\n\n\1', formatted_text)
    
    # Clean up multiple newlines
    formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text)
    
    return formatted_text.strip()

@app.route('/')
def home():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle math questions and return formatted responses"""
    try:
        data = request.get_json()
        user_question = data.get('question', '').strip()
        
        if not user_question:
            return jsonify({
                'success': False,
                'error': 'Please enter a question.'
            }), 400
        
        # Create a prompt that encourages clean, structured mathematical solutions
        prompt = f"""
You are a mathematical tutor. Solve this step by step: {user_question}

Format your response EXACTLY like this:

**Solution:**

**Step 1:** [Clear explanation of first step with mathematical operations]

**Step 2:** [Clear explanation of second step with mathematical operations]

[Continue with more steps as needed]

**Final Answer:** [Final result clearly stated]

Requirements:
- Use clear mathematical notation
- Show all work step by step
- Explain each step clearly
- Put mathematical expressions in a readable format
- End with a clear final answer

Question: {user_question}
"""
        
        # Send request to Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a math tutor. Give clear, numbered steps. Use simple notation like: sin(x), cos(x), x^2, f'(x), lim(h→0). No LaTeX commands. Be concise and organized."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=1024
        )
        
        # Get the response
        bot_response = chat_completion.choices[0].message.content
        
        # Format mathematical expressions for LaTeX rendering
        formatted_response = format_math_response(bot_response)
        
        return jsonify({
            'success': True,
            'response': formatted_response
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error while processing your question. Please try again.'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if API key is configured
    if not os.getenv("GROQ_API_KEY"):
        print("Warning: GROQ_API_KEY not found in environment variables.")
        print("Please make sure to set your API key in the .env file.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)