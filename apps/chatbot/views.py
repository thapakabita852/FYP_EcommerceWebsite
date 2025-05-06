import traceback
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .chatbot import process_message
import json


def chatbot_view(request):
    """
    Renders the chatbot interface.
    """
    return render(request, "chatbot/chatbot.html")


def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            bot_reply = process_message(user_message)
            return JsonResponse({"reply": bot_reply})
        except Exception as e:
            # Log the full traceback
            print("Error in chatbot_api:", traceback.format_exc())
            return JsonResponse({"error": "An internal server error occurred. Please try again later."}, status=500)
    else:
        return HttpResponse("Method Not Allowed", status=405)
