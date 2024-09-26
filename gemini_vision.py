# Import necessary libraries
from dotenv import load_dotenv    # For loading environment variables from .env file
import streamlit as st            # For building web app interfaces
import os                         # For accessing environment variables
from PIL import Image             # For image processing
import google.generativeai as genai  # For interacting with Google Generative AI models

# Load environment variables from .env file
load_dotenv()

# Retrieve Google API key from the environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure the Generative AI library with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to get a response from the Gemini model based on input text and image
def get_gemini_response(input_message, input_image):
    # Instantiate the Generative AI model (Gemini-1.5-flash)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Generate a response using both text and image inputs if both are provided
    if input_message != "":
        response = model.generate_content([input_message, input_image])
    # If only an image is provided, generate content using just the image
    else:
        response = model.generate_content(input_image)
    
    # Return the generated text response
    return response.text

# Streamlit app configuration (sets the title of the web app)
st.set_page_config(page_title="Image-Driven Chatbot")

# App header
st.header("Image-Driven Chatbot")

# Text input for user prompt
input = st.text_input("Input prompt:", key='input')

# File uploader for the user to upload an image (supports JPEG, JPG, and PNG formats)
uploaded_file = st.file_uploader("Choose an image:", type=['jpeg', 'jpg', 'png'])

# Initialize a variable to store the uploaded image for display
display_image = ""

# If an image is uploaded, process and display it
if uploaded_file is not None:
    display_image = Image.open(uploaded_file)
    st.image(display_image, caption="Uploaded image", use_column_width=True)

# Submit button for user to send the input text and image to the model
submit = st.button('Submit')

# When the submit button is pressed, get the AI-generated response
if submit:
    # Call the function to get the response from the Gemini model
    output = get_gemini_response(input_message=input, input_image=display_image)
    
    # Display the AI-generated response in the app
    st.subheader("Your response is:")
    st.write(output)
