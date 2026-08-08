from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from django_ratelimit.decorators import ratelimit

from agent import agent_query


@ensure_csrf_cookie
def index(request):
    return render(request, "chatbot/index.html")


# Two limits, both counted in the local-memory cache (see CACHES in settings):
#   - per IP: 10 POSTs/minute, so one visitor can't hammer the LLM
#   - global: 300 POSTs/day, a hard ceiling on total API spend for the instance
# block=False means the decorator flags request.limited instead of raising,
# so we can return a clean JSON 429 instead of Django's HTML error page.
@ratelimit(key="ip", rate="10/m", method="POST", block=False)
@ratelimit(key=lambda group, request: "global", rate="300/d", method="POST", block=False)
def ask(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    if getattr(request, "limited", False):
        return JsonResponse(
            {"error": "Rate limit reached. Please wait a moment and try again."},
            status=429,
        )

    try:
        data = json.loads(request.body)
        query = (data.get("question") or "").strip()
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not query:
        return JsonResponse({"error": "Empty question"}, status=400)

    try:
        res = agent_query(query)
        return JsonResponse({
            "answer": res['answer'],
            "sources": res['sources'],
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
