from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import fitz  # PyMuPDF
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY no está configurada")

client = OpenAI(api_key=api_key)

def extract_text(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = extract_text(file_bytes)

    prompt = f"""
Texto extraído del PDF (resumen):

{text[:7000]}

Aplica las siguientes reglas legales:
🔎 Identifica procesos como demandado, insolvencia, familia, cooperativas/fondos de empleados.
❌ No alertar si la última actuación fue: archivo definitivo, terminación, exoneración, entrega de títulos, desistimiento tácito con 6+ meses, inadmisión o desistimiento.
📋 Devuelve: tabla detallada + cuadro resumen + estado judicial en Policía Nacional.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un analista legal experto en procesos judiciales colombianos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return {"resultado": response.choices[0].message.content}
