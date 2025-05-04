from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    print(f"Mensagem recebida de {From}: {Body}")
    try:
        resposta_ia = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente prestativo e direto ao ponto."},
                {"role": "user", "content": Body}
            ]
        )
        texto = resposta_ia.choices[0].message.content
    except Exception as e:
        texto = f"Ocorreu um erro: {str(e)}"

    twiml = MessagingResponse()
    msg = twiml.message()
    msg.body(texto)

    return str(twiml)
