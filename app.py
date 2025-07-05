import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyA93jup_qGXbRXBjMWZtx8lHqSpGBTb0-o"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

SYSTEM_INSTRUCTIONS = """
You are a sweet spiritual helper who gives responses based on the Bhagavad Gita. When a user shares a problem or situation, do the following:
1. Suggest a specific verse from the Gita (include chapter and verse).
2. Explain the meaning of the verse.
3. Relate it to the user's problem and make sure to focus on the teachings of the gita.
4. Give actionable advice inspired by the verse.
Use a warm, compassionate, and practical tone but focused on the teachings of the Bhagavad Gita. Dont start with the words "my dear one"
"""

def get_gita_response(user_input):
    prompt = f"{SYSTEM_INSTRUCTIONS}\n\nUser's problem: {user_input}"
    response = model.generate_content(prompt)

    # Convert plain text into formatted HTML
    formatted = response.text.replace('\n\n', '</p><p>').replace('\n', '<br>')
    styled_html = f"""
    <div class="response-box">
        <p>{formatted}</p>
    </div>
    """
    return styled_html


with gr.Blocks(css="""
@import url('https://fonts.googleapis.com/css2?family=Marcellus&family=Poppins:wght@400;500;700&display=swap');

.gradio-container {
    background: linear-gradient(135deg, #0e1c36, #1e3770, #2952a3);
    min-height: 100vh;
    padding-top: 80px;
    font-family: 'Poppins', sans-serif;
    color: #f0f0f0;
    zoom: 1.2; 
}

/* Title */
h1 {
    font-family: 'Marcellus', serif !important;
    font-size: 3rem !important;
    color: #ffffff !important;
    margin-bottom: 1rem !important;
    text-align: center;
    text-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

/* Subtitle */
.gr-description {
    font-family: 'Poppins', sans-serif !important;
    font-size: 1.3rem !important;
    color: #d0d0d0 !important;
    text-align: center;
    margin-bottom: 2.5rem !important;
}

/* Labels */
label {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    color: #e0e0e0 !important;
    font-family: 'Poppins', sans-serif !important;
}

/* Input & Output Box Styling */
.gr-textbox textarea,
.gr-textbox input,
.gr-textbox .wrap {
    font-size: 1.1rem !important;
    font-family: 'Poppins', sans-serif !important;
    border-radius: 12px !important;
    border: 2px solid #5aa3f6 !important;
    background-color: #1e293b !important;
    color: #ffffff !important;
    box-shadow: 0 0 12px rgba(90, 163, 246, 0.6); /* 💡 Glowing border */
}

/* Output */
.gr-textbox .scroll-hide {
    font-size: 1.1rem !important;
    line-height: 1.7;
    background-color: #1e293b !important;
    border-radius: 12px;
    padding: 1.2rem;
    font-family: 'Poppins', sans-serif !important;
    box-shadow: 0 0 12px rgba(90, 163, 246, 0.4); /* Soft glow */
}

/* Button */
.gr-button {
    background-color: #3b82f6 !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 14px 30px !important;
    border-radius: 12px !important;
    transition: 0.3s ease;
    box-shadow: 0 0 18px rgba(90, 163, 246, 0.6); /* Glowing blue */
}

.gr-button:hover {
    background-color: #2563eb !important;
    box-shadow: 0 0 25px rgba(90, 163, 246, 0.8);
}

/* Layout Panel */
.gr-panel {
    max-width: 800px !important;
    margin: auto !important;
    background-color: rgba(255, 255, 255, 0.03) !important;
    border-radius: 20px !important;
    padding: 35px !important;
    box-shadow: 0 0 40px rgba(0, 0, 0, 0.3);
}
               
    .response-box {
    font-size: 1.11rem;
    line-height: 1.8;
    font-style: italic;
    color: #f0f6ff;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid #5aa3f6;
    border-radius: 12px;
    box-shadow: 0 0 12px #5aa3f688;
    backdrop-filter: blur(6px);
    margin-top: 1rem;
    font-family: 'Poppins', sans-serif;
}

#gita-output {
    background-color: #47b2f5 !important; 
    color: #ffffff !important;             /* white text for readability */
    padding: 1.5rem !important;
    border-radius: 12px !important;
    font-size: 1.1rem !important;
    font-style: italic;
    box-shadow: 0 0 12px rgba(90, 163, 246, 0.4); /* Soft glow */
}


""") as demo:


    gr.Markdown("# 🕉️ Bhagavad Gita Wisdom Assistant")
    gr.Markdown("Get Gita-based guidance for your problems or dilemmas.")

    inp= gr.Textbox(lines=4, label="Describe your situation...")
    out = gr.HTML(label="What the Gita has to say <3", elem_id="gita-output")

    submit = gr.Button("Get Wisdom")
    submit.click(get_gita_response, inputs=inp, outputs=out)

demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)), debug=True)

