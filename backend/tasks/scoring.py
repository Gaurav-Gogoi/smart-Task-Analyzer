from datetime import date, datetime


def calculate_urgency(due_date):
    # Convert string → date
    if isinstance(due_date, str):
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return 0  # invalid date

    today = date.today()
    diff = (due_date - today).days

    if diff < 0:
        return 10  # overdue = max urgency
    elif diff == 0:
        return 9
    elif diff <= 3:
        return 8
    elif diff <= 7:
        return 6
    else:
        return 3  # far deadline = low urgency


def calculate_dependency_score(task_id, tasks):
    count = 0
    for t in tasks:
        if task_id in t.get("dependencies", []):
            count += 1
    return count


def calculate_score(task, tasks, strategy="smart"):
    urgency = calculate_urgency(task.get("due_date"))
    importance = task.get("importance", 0)
    effort = task.get("estimated_hours", 0)
    dependency_score = calculate_dependency_score(task.get("id", 0), tasks)

    weight = {
        "urgency": 0.4,
        "importance": 0.3,
        "effort": 0.2,
        "dependency": 0.1,
    }

    # strategy overrides
    if strategy == "fastest":
        weight["effort"] = 0.6
    elif strategy == "impact":
        weight["importance"] = 0.6
    elif strategy == "deadline":
        weight["urgency"] = 0.7

    score = (
        urgency * weight["urgency"]
        + importance * weight["importance"]
        + (10 - effort) * weight["effort"]
        + dependency_score * weight["dependency"]
    )

    explanation = {
        "urgency": urgency,
        "importance": importance,
        "effort_effect": 10 - effort,
        "dependency_score": dependency_score,
        "strategy_used": strategy,
    }

    return round(score, 2), explanation
