import os
import json
from datetime import datetime


class DashboardGenerator:

    def __init__(self):
        os.makedirs("outputs", exist_ok=True)
        os.makedirs("dashboard", exist_ok=True)

    def save_json(self, audio_path, summary, entities, events):

        output = {
            "source": audio_path,
            "processed_at": datetime.now().isoformat(),
            "summary": summary,
            "entities": entities,
            "events": events
        }

        json_file = os.path.join(
            "outputs",
            "sample_01_insights.json"
        )

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)

        print("✅ JSON Saved Successfully")

        return output

    def generate_dashboard(
        self,
        transcript,
        summary,
        entities,
        events
    ):

        total_entities = sum(len(v) for v in entities.values())
        total_events = len(events)
        word_count = len(transcript.split())

        html = f"""
<!DOCTYPE html>
<html>

<head>

<title>Audio Business Intelligence Pipeline</title>

<style>

body{{
font-family:Segoe UI;
background:#0f172a;
color:white;
padding:30px;
}}

.container{{
max-width:1200px;
margin:auto;
}}

.card{{
background:#1e293b;
padding:20px;
margin-bottom:20px;
border-radius:12px;
box-shadow:0 0 10px rgba(0,0,0,.3);
}}

.metric{{
display:inline-block;
width:180px;
padding:15px;
margin:8px;
background:#334155;
border-radius:10px;
text-align:center;
}}

.metric h2{{
color:#38bdf8;
margin:0;
}}

.metric p{{
margin:5px;
}}

.event{{
padding:12px;
background:#0f172a;
margin-top:10px;
border-left:5px solid #38bdf8;
}}

.entity{{
padding:8px;
margin:6px;
background:#334155;
border-radius:6px;
}}

pre{{
white-space:pre-wrap;
font-size:14px;
}}

</style>

</head>

<body>

<div class="container">

<h1>🎙 Audio Business Intelligence Pipeline</h1>

<div class="card">

<div class="metric">
<h2>{word_count}</h2>
<p>Total Words</p>
</div>

<div class="metric">
<h2>{total_entities}</h2>
<p>Total Entities</p>
</div>

<div class="metric">
<h2>{len(entities)}</h2>
<p>Entity Types</p>
</div>

<div class="metric">
<h2>{total_events}</h2>
<p>Business Events</p>
</div>

</div>

<div class="card">

<h2>📄 Summary</h2>

<p>{summary}</p>

</div>

<div class="card">

<h2>🏢 Extracted Entities</h2>
"""

        for label, values in entities.items():

            html += f"<h3>{label}</h3>"

            for item in values:

                html += f"<div class='entity'>{item}</div>"

        html += """
</div>

<div class="card">

<h2>📈 Business Events</h2>
"""

        for event in events:

            html += f"""
<div class="event">

<b>{event['event_type']}</b>

({int(event['confidence']*100)}%)

<br><br>

{event['sentence']}

</div>
"""

        html += f"""

</div>

<div class="card">

<h2>📝 Transcript</h2>

<pre>

{transcript[:6000]}

</pre>

</div>

</div>

</body>

</html>
"""

        dashboard_file = os.path.join(
            "dashboard",
            "dashboard.html"
        )

        with open(
            dashboard_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)

        print("✅ Dashboard Generated Successfully")
        print(f"Saved at : {dashboard_file}")