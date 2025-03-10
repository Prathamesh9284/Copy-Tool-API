from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
import io
from typing import List
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://appt-hr.vercel.app","*"],  # Adjust this to match your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/')
async def root():
    return {'message':'Hello World!!!'}

@app.post('/extract-text')
async def extract_text(
    images: List[UploadFile] = File(...)
):
    extracted_text = ''
    for image in images:
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        prompt = 'Give the text from the image that has been provided. No preamble text and any other text. Keep only text from the image, no other text.'
        model=genai.GenerativeModel(model_name='gemini-2.0-flash')
        response=model.generate_content([prompt,pil_image])
        extracted_text+= response.text
    return extracted_text