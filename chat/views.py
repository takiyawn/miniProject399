from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_groq import ChatGroq
import json

#view = controller class

llm = ChatGroq(model="openai/gpt-oss-20b")

def home(request):
	return render(request, "chat/index.html")

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