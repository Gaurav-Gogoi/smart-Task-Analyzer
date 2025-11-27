# Smart Task Analyzer
Mini-application to intelligently score and prioritize tasks based on urgency, importance, effort, and dependencies.

## Setup Instructions

1. Clone the repository:

2. Create virtual environment:

3. Install dependencies:
django, rest_framework,cors-headers

4. Run the server:

5. Open `frontend/index.html` in browser for the UI.

6. Sample data has been provided copy and paste in frontend to check working 

## Priority Scoring Algorithm

Tasks are scored based on four factors:

1. **Urgency** – How close the due date is; overdue tasks get the highest score.
2. **Importance** – User-provided rating (1-10).
3. **Effort** – Lower estimated hours get higher priority in "fastest" strategy.
4. **Dependencies** – Tasks that block others get higher priority.

We combine these using weighted sums:

| Factor       | Weight (Smart Balance) |
|--------------|----------------------|
| Urgency      | 0.4                  |
| Importance   | 0.3                  |
| Effort       | 0.2                  |
| Dependency   | 0.1                  |

The algorithm supports multiple strategies:  
- **Smart Balance**: balances all factors  
- **Fastest Wins**: favors low-effort tasks  
- **High Impact**: favors importance  
- **Deadline Driven**: favors urgency

Each task also returns an explanation object showing individual factor contributions.

## Design Decisions

- Used **Django REST Framework** for API simplicity.
- Frontend is plain HTML/CSS/JS for quick integration.
- Used **JSONField** for dependencies to handle dynamic lists.
- Handled invalid/missing data gracefully in scoring.
- Strategy weights are configurable for different user preferences.

## Time Breakdown

- Backend models & serializer: 30 min  
- Scoring algorithm: 1 hr  
- API views: 45 min  
- Unit tests: 30 min  
- Frontend development: 1 hr  
- Bug fixing & integration: 1 hr

## Future Improvements

- Dependency graph visualization to detect circular dependencies.
- Date intelligence: skip weekends/holidays.
- Learning system: adjust algorithm based on user feedback.
- More extensive unit tests for edge cases.

