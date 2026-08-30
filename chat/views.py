from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from langchain_groq import ChatGroq
from elevenlabs.client import ElevenLabs
import json

eleven_client = ElevenLabs()

llm = ChatGroq(model="openai/gpt-oss-20b")

conversation_log = []

def home(request):
    return render(request, "chat/index.html")

def gp_view(request):
    return render(request, "chat/gp.html", {"log": conversation_log})

@csrf_exempt
def ask(request):
    question = json.loads(request.body)["question"]

    system_prompt = (
        "You are a warm, calm, empathetic pre-consultation assistant talking to a patient "
        "before they see their GP. Speak naturally, like a caring nurse — not clinical or robotic. "
        "Acknowledge what they say before asking anything. Ask ONE gentle follow-up question at a time. "
        "Keep responses short (2-3 sentences), since this is spoken aloud, not read."
    )

    messages = [("system", system_prompt)]
    for entry in conversation_log:
        messages.append(("human", entry["question"]))
        messages.append(("ai", entry["answer"]))
    messages.append(("human", question))

    answer = llm.invoke(messages).content

    conversation_log.append({"question": question, "answer": answer})

    return JsonResponse({"answer": answer})

@csrf_exempt
def speak(request):
    text = json.loads(request.body)["text"]
    audio = eleven_client.text_to_speech.convert(
        voice_id="rYDhrwHnXppgdRdM6xrv",  # old voice idk
        model_id="eleven_turbo_v2",
        text=text,
    )
    audio_bytes = b"".join(audio)
    return HttpResponse(audio_bytes, content_type="audio/mpeg")