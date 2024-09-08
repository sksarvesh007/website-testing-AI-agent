import os
import gradio as gr
import google.generativeai as genai
from PIL import Image
import numpy as np
import base64
import io
import dotenv
from groq import Groq
from langchain_groq import ChatGroq

dotenv.load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def save_and_analyze_image(image, question):
    if not os.path.exists("images"):
        os.makedirs("images")

    image_path = "images/image.jpg"

    pil_image = Image.fromarray(image.astype(np.uint8))
    pil_image.save(image_path)

    sample_file = genai.upload_file(path=image_path, display_name="Website Screenshot")
    file = genai.get_file(name=sample_file.name)

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    gemini_response = model.generate_content([sample_file, 
        "List out the features of the website and provide a detailed description of each feature, "
        "the general overview of the website, and the services it provides."
    ])

    gemini_output = gemini_response.text

    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0,
        max_tokens=2048,
        timeout=None,
        max_retries=2,
        groq_api_key=groq_api_key
    )

    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional software developer with expertise in web development, "
                    "backend, blockchain, AIML, and mobile development. \nOutput should describe a "
                    "detailed, step-by-step guide on how to test each functionality. Each test case "
                    "should include:\n- Description: What the test case is about.\n- Pre-conditions: "
                    "What needs to be set up or ensured before testing.\n- Testing Steps: Clear, "
                    "step-by-step instructions on how to perform the test.\n- Expected Result: What "
                    "should happen if the feature works correctly.\nGive me the output in the format of:\n"
                    "Feature: <feature_name>\nDescription: <description>\nPre-conditions: <pre-conditions>\n"
                    "Testing Steps: <testing_steps>\nExpected Result: <expected_result>"
                )
            },
            {
                "role": "user",
                "content": gemini_output + " User additional query: " + question
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    feature_listing = ""
    for chunk in completion:
        feature_listing += chunk.choices[0].delta.content or ""

    return feature_listing
def encode_image(image, max_size=(1024, 1024)):
    img = Image.fromarray(image)
    img.thumbnail(max_size, Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

demo = gr.Interface(
    fn=save_and_analyze_image,
    inputs=[
        gr.Image(type="numpy"),
        gr.Textbox(lines=2, placeholder="Upload an image and give some extra context about the image")
    ],
    outputs=gr.Markdown(label="Test Cases and their Description", height=500),
    title="Test Cases Generator",
)

demo.launch(share=True)
