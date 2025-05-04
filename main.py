from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse, JSONResponse
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os

# Inicializa cliente da OpenAI (nova sintaxe >=1.0.0)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "online",
        "info": "Use o endpoint POST /webhook para enviar mensagens via Twilio WhatsApp.",
        "documentacao": "https://fastapi.tiangolo.com/"
    }

@app.post("/webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    print(f"Mensagem recebida de {From}: {Body}")

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente prestativo e direto ao ponto."},
                {"role": "user", "content": Body}
            ]
        )
        texto = chat_completion.choices[0].message.content
    except Exception as e:
        texto = f"Ocorreu um erro: {str(e)}"

    twiml = MessagingResponse()
    msg = twiml.message()
    msg.body(texto)

    return str(twiml)
