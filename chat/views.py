from django.shortcuts import render

# Create your views here.	
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_groq import ChatGroq
import json

llm = ChatGroq(model="openai/gpt-oss-20b")

def home(request):
	return render(request, "chat/index.html")

@csrf_exempt
def ask(request):
    question = json.loads(request.body)["question"]
    answer = llm.invoke(question).content
    return JsonResponse({"answer": answer})
