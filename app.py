from flask import Flask, render_template, request
from groq import Groq
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Initialize Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Interview Questions
QUESTIONS = [
    "Tell me about yourself",
    "What are your strengths?",
    "What are your weaknesses?",
    "Why should we hire you?",
    "Where do you see yourself in 5 years?",
    "Describe a challenging project"
]


# AI Feedback Function
def get_ai_feedback(question, answer):

    prompt = f"""
You are a professional interview coach.

Analyze the answer below.

Question:
{question}

Answer:
{answer}

Give feedback in this format:

Confidence: X/10
Clarity: X/10
Grammar: X/10

Strengths:
- ...

Weaknesses:
- ...

Suggestions:
- ...

Sample Improved Answer:
...
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert interview coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )

    return completion.choices[0].message.content


# Main Route
@app.route("/", methods=["GET", "POST"])
def home():

    feedback = ""
    answer = ""
    selected = QUESTIONS[0]

    if request.method == "POST":

        # Clear Button
        if "clear" in request.form:
            return render_template(
                "index.html",
                questions=QUESTIONS,
                feedback="",
                answer="",
                selected=QUESTIONS[0]
            )

        selected = request.form.get("question")
        answer = request.form.get("answer")

        if answer.strip():

            try:
                feedback = get_ai_feedback(selected, answer)

            except Exception as e:
                feedback = f"❌ AI Error: {str(e)}"

        else:
            feedback = "⚠️ Please enter your answer."

    return render_template(
        "index.html",
        questions=QUESTIONS,
        feedback=feedback,
        answer=answer,
        selected=selected
    )


# Run App
if __name__ == "__main__":
    app.run(debug=True)
