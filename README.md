# Test Case Generator with Groq and LangChain

This project is a web-based tool that analyzes uploaded images and generates detailed test cases using Groq's AI capabilities. The application is built with [Gradio](https://gradio.app/) for user interaction, [LangChain](https://langchain.com/) for AI-powered document and text processing, and the Groq API for model interactions.

![1725784578139](image/README/1725784578139.png)

## Features

- **Image Upload and Encoding**: Upload any image, and the application will resize it and encode it into a base64 format to be used in the model.
- **AI-Powered Analysis**: Uses Groq's `llama-3.1-70b-versatile` model to analyze the uploaded image and generate test cases for its features.
- **Dynamic Test Case Generation**: Provides a step-by-step test case for each functionality detected in the image.
- **User Queries**: Allows additional queries from the user to provide context for more specific test cases.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/sksarvesh007/website-testing-AI-agent.git
   cd website-testing-AI-agent
   ```
2. **Install dependencies**:
   Make sure you have Python 3.x installed, and then install the required libraries using `pip`:

   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   Create a `.env` file in the root of the project and add your Groq API key:

   ```bash
   GROQ_API_KEY=your_groq_api_key
   ```
4. **Download Gradio and LangChain dependencies**:
   Ensure Gradio, PIL, and Groq API dependencies are installed.

   ```bash
   pip install gradio pillow langchain
   ```

## Usage

1. **Run the application**:
   Start the application using the following command:

   ```bash
   python app.py
   ```
2. **Interact with the Interface**:

   - Open the Gradio interface in your browser.
   - Upload an image and add a query to provide extra context about the image.
   - The application will analyze the image and return detailed test cases with pre-conditions, steps, and expected results.

## Code Structure

- **`app.py`**: The main application script.
- **`encode_image()`**: This function takes an image, resizes it, and encodes it to base64 format.
- **`analyze_image()`**: This function handles the interaction with Groq's API to generate test cases for the uploaded image.
- **`gr.Interface()`**: This sets up the Gradio interface to accept images and user queries.

## Example

- **Input**: An image of a website and a query like "Describe the login functionality."
- **Output**: A step-by-step guide on testing the login feature, including pre-conditions, test steps, and expected results.

## How It Works

1. **Image Encoding**: The uploaded image is resized and converted into a base64 string.
2. **Groq API Call**: The encoded image and user query are sent to Groq's model (`llava-v1.5-7b-4096-preview`) to generate a list of features in the image.
3. **Feature Test Case Generation**: Based on the feature list, the model generates a detailed guide on how to test each feature, which is then displayed in the Gradio interface.
