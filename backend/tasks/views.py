from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskInputSerializer
from .scoring import calculate_score
import json


@api_view(["POST"])
def analyze_tasks(request):
    tasks = request.data.get("tasks", [])
    strategy = request.data.get("strategy", "smart")

    if not isinstance(tasks, list):
        return Response({"error": "Tasks should be a list"}, status=400)

    results = []

    for idx, t in enumerate(tasks):
        if not isinstance(t, dict):
            return Response({"error": f"Invalid task format at index {idx}"}, status=400)

        t["id"] = idx  # temporary ID for dependencies

        # Validate input
        serializer = TaskInputSerializer(data=t)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=400)

        score, explanation = calculate_score(t, tasks, strategy)
        t["score"] = score
        t["explanation"] = explanation

        results.append(t)

    # Sort tasks by score descending
    sorted_tasks = sorted(results, key=lambda x: x["score"], reverse=True)
    return Response({"tasks": sorted_tasks})


@api_view(["GET"])
def suggest_tasks(request):
    tasks_json = request.query_params.get("tasks")
    if not tasks_json:
        return Response({"error": "No tasks provided"}, status=400)

    try:
        tasks = json.loads(tasks_json)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=400)

    results = []
    for idx, t in enumerate(tasks):
        if not isinstance(t, dict):
            continue
        t["id"] = idx
        score, explanation = calculate_score(t, tasks, "smart")
        t["score"] = score
        t["explanation"] = explanation
        results.append(t)

    sorted_tasks = sorted(results, key=lambda x: x["score"], reverse=True)
    return Response({"tasks": sorted_tasks[:3]})
