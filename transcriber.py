import os
import whisper


class AudioTranscriber:

    def __init__(self, model_name="base"):
        print("\nLoading Whisper model...")
        self.model = whisper.load_model(model_name)
        print("Whisper model loaded successfully!")

    def transcribe_audio(self, audio_path):

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print("\nTranscribing audio...")

        result = self.model.transcribe(audio_path)

        transcript = result["text"]

        language = result["language"]

        os.makedirs("transcripts", exist_ok=True)

        transcript_path = os.path.join(
            "transcripts",
            os.path.basename(audio_path).replace(".mp3", ".txt")
        )

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        print("\nTranscription completed successfully!")
        print(f"Detected Language : {language}")
        print(f"Transcript Saved : {transcript_path}")

        return result