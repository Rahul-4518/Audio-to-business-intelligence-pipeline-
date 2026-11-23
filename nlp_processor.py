import spacy
import re
from collections import defaultdict, Counter


class NLPProcessor:

    def __init__(self):

        print("\nLoading SpaCy Model...")

        self.nlp = spacy.load("en_core_web_sm")

        print("SpaCy Model Loaded Successfully!")

    # -------------------------
    # Entity Extraction
    # -------------------------
    def extract_entities(self, text):

        doc = self.nlp(text)

        entities = defaultdict(list)

        labels = [
            "ORG",
            "PERSON",
            "PRODUCT",
            "GPE",
            "DATE",
            "MONEY"
        ]

        for ent in doc.ents:

            if ent.label_ in labels:

                if ent.text not in entities[ent.label_]:

                    entities[ent.label_].append(ent.text)

        return dict(entities)

    # -------------------------
    # Summary Generation
    # -------------------------
    def generate_summary(self, text, num_sentences=5):

        sentences = [
            s.strip()
            for s in re.split(r'(?<=[.!?])\s+', text)
            if len(s.strip()) > 30
        ]

        stopwords = {
            "the","a","an","is","in","of","to","and",
            "for","with","that","this","was","are",
            "has","have","been","its","it","at","by",
            "we","our","as"
        }

        words = re.findall(r"\b\w+\b", text.lower())

        frequency = Counter(
            word for word in words
            if word not in stopwords
        )

        ranked = sorted(
            sentences,
            key=lambda sentence:
            sum(
                frequency.get(word, 0)
                for word in re.findall(r"\b\w+\b", sentence.lower())
            ),
            reverse=True
        )

        top = set(ranked[:num_sentences])

        summary = " ".join(
            sentence
            for sentence in sentences
            if sentence in top
        )

        return summary

    # -------------------------
    # Business Event Detection
    # -------------------------
    def detect_events(self, text):

        event_keywords = {

            "Product Launch":[
                "launch",
                "release",
                "announce",
                "introducing"
            ],

            "Investment":[
                "invest",
                "funding",
                "raised",
                "million",
                "billion"
            ],

            "Partnership":[
                "partner",
                "collaboration",
                "alliance"
            ],

            "Acquisition":[
                "acquire",
                "acquisition",
                "merger",
                "purchase"
            ],

            "Leadership Change":[
                "CEO",
                "appointed",
                "resigned",
                "stepping down"
            ],

            "Market Expansion":[
                "expand",
                "growth",
                "international",
                "global"
            ]

        }

        sentences = re.split(r'(?<=[.!?])\s+', text)

        events = []

        for sentence in sentences:

            lower = sentence.lower()

            for event_type, keywords in event_keywords.items():

                if any(keyword.lower() in lower for keyword in keywords):

                    events.append({

                        "event_type": event_type,
                        "sentence": sentence[:150],
                        "confidence": 0.75

                    })

                    break

        return events