
# Educational Q&A Bot for Mathematics

A web-based chatbot that answers math questions step-by-step using the Groq API and Llama-3.1 model. Built with Flask, it provides clear, structured solutions and mathematical explanations for students and learners.

---

## 🚀 Features
- Ask math questions and get step-by-step solutions
- Clear formatting for mathematical expressions
- Web interface with Flask
- Uses Groq API (Llama-3.1-8b-instant)
- Supports LaTeX-style math rendering

---

## 🛠️ Installation
1. Clone the repository:
	```bash
	git clone https://github.com/Muhammad-Muzammil-Shah/Educational-Q-A-Bot-for-Mathematics.git
	cd Educational-Q-A-Bot-for-Mathematics
	```
2. Create a virtual environment (optional but recommended):
	```bash
	python -m venv venv
	venv\Scripts\activate  # Windows
	# Or
	source venv/bin/activate  # macOS/Linux
	```
3. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
4. Add your Groq API key to a `.env` file:
	```env
	GROQ_API_KEY=your_api_key_here
	```

---

## 💡 Usage
1. Start the Flask app:
	```bash
	python app.py
	```
2. Open your browser and go to `http://localhost:5000`
3. Enter a math question and get a step-by-step solution.

---

## 📦 Technologies
- Python
- Flask
- Groq API
- Llama-3.1-8b-instant
- HTML/CSS/JS (templates/static)

---

## 📃 License
Open source. Feel free to use, modify, and distribute.
