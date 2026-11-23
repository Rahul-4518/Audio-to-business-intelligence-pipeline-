from transcriber import AudioTranscriber
from nlp_processor import NLPProcessor
from dashboard_generator import DashboardGenerator

audio_path = "audio_samples/sample.mp3"

# ----------------------------------
# Speech to Text
# ----------------------------------

transcriber = AudioTranscriber("base")

result = transcriber.transcribe_audio(audio_path)

transcript = result["text"]

# ----------------------------------
# NLP
# ----------------------------------

nlp = NLPProcessor()

summary = nlp.generate_summary(transcript)

entities = nlp.extract_entities(transcript)

events = nlp.detect_events(transcript)

# ----------------------------------
# Dashboard
# ----------------------------------

dashboard = DashboardGenerator()

dashboard.save_json(
    audio_path,
    summary,
    entities,
    events
)

dashboard.generate_dashboard(
    transcript,
    summary,
    entities,
    events
)

print("\nProject Completed Successfully!")