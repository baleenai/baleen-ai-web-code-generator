import re
from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import google.generativeai as genai

# Replace this with your actual API key
api_key = "AIzaSyBjEj0j6P8UZ3Fn18XO2t1Cy16n8piM1Vg"

# Configure the model with your API key
genai.configure(api_key=api_key)

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 50000,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    input_data = request.json
    input_text = input_data.get('inputText', '')

    chat_session = model.start_chat(
        history=[]
    )
    response = chat_session.send_message(input_text + " Generate an HTML page with embedded CSS and JavaScript")

    # Extract HTML, CSS, and JavaScript using regular expressions
    html_pattern = re.compile(r'(<html.*?>.*?</html>)', re.DOTALL)
    css_pattern = re.compile(r'(<style.*?>.*?</style>)', re.DOTALL)
    js_pattern = re.compile(r'(<script.*?>.*?</script>)', re.DOTALL)

    html_match = html_pattern.search(response.text)
    css_match = css_pattern.search(response.text)
    js_match = js_pattern.search(response.text)

    html_code = html_match.group(0) if html_match else ""
    css_code = css_match.group(0) if css_match else ""
    js_code = js_match.group(0) if js_match else ""

    return jsonify({
        'html': html_code,
        'css': css_code,
        'js': js_code
    })

if __name__ == '__main__':
    app.run(debug=True)
