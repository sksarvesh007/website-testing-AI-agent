
import os
import gradio as gr
from groq import Groq
import base64
from PIL import Image
import io
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
import dotenv
dotenv.load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def encode_image(image, max_size=(1024, 1024)):
    """Encode the image to base64 format after resizing."""
    img = Image.fromarray(image)
    img.thumbnail(max_size, Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=2048,
    timeout=None,
    max_retries=2,
    groq_api_key=groq_api_key
)
extra_text = "List out the features of the website and provide a detailed description of each feature. , User additional query : "
def analyze_image(image, question):
    """Analyze the uploaded image and generate a feature list."""
    base64_image = encode_image(image)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": extra_text + question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llava-v1.5-7b-4096-preview",
    )

    query = chat_completion.choices[0].message.content

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
                "content": query 
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

demo = gr.Interface(
    fn=analyze_image,
    inputs=[
        gr.Image(type="numpy"),
        gr.Textbox(lines=2, placeholder="Upload an image and give some extra context about the image")
    ],
    outputs=gr.Markdown(label="Test Case and their description" , height=500),
    title="Test Cases Generator",
    description=""
)

demo.launch(share = True)