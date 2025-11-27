async function analyze() {
    const jsonText = document.getElementById("jsonInput").value;
    const strategy = document.getElementById("strategy").value;
    const resultDiv = document.getElementById("result");

    let tasks;
    try {
        tasks = JSON.parse(jsonText);
        if (!Array.isArray(tasks)) throw new Error("JSON must be an array of tasks");
    } catch (err) {
        resultDiv.innerHTML = `<p style="color:red;">Invalid JSON! ${err.message}</p>`;
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tasks, strategy })
        });

        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch {
                errorData = { error: "Server returned non-JSON response" };
            }
            resultDiv.innerHTML = `<p style="color:red;">Error: ${JSON.stringify(errorData)}</p>`;
            return;
        }

        const data = await response.json();
        const tasksArr = data.tasks; // <-- important!

        resultDiv.innerHTML = "";

        tasksArr.forEach(t => {
            let cls = t.score > 8 ? "high" : t.score > 5 ? "medium" : "low";

            resultDiv.innerHTML += `
                <div class="task ${cls}">
                    <h3>${t.title} (Score: ${t.score})</h3>
                    <p>Due: ${t.due_date}</p>
                    <p>Hours: ${t.estimated_hours}</p>
                    <p>Importance: ${t.importance}</p>
                    <p><b>Reason:</b> ${JSON.stringify(t.explanation)}</p>
                </div>
            `;
        });

    } catch (err) {
        console.error(err);
        resultDiv.innerHTML = `<p style="color:red;">Error connecting to API</p>`;
    }
}
