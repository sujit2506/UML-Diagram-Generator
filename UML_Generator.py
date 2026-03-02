import spacy
from collections import defaultdict
import re

nlp = spacy.load("en_core_web_sm")

class UMLGenerator:

    def __init__(self):
        self.classes = set()
        self.relationships = []
        self.confidences = []

    def preprocess(self, text):
        return text.strip()

    def extract_entities(self, text):
        doc = nlp(text)

        for chunk in doc.noun_chunks:
            if chunk.root.pos_ in ["NOUN", "PROPN"]:
                class_name = chunk.root.text.capitalize()
                self.classes.add(class_name)

        return list(self.classes)

    def detect_relationships(self, text):
        doc = nlp(text)

        for sent in doc.sents:
            words = sent.text.lower()

            # Inheritance
            if "is a" in words:
                parts = words.split("is a")
                child = parts[0].split()[-1].capitalize()
                parent = parts[1].split()[0].capitalize()
                self.relationships.append((child, parent, "inheritance"))
                self.confidences.append(0.9)

            # Aggregation
            elif "has a" in words:
                parts = words.split("has a")
                owner = parts[0].split()[-1].capitalize()
                component = parts[1].split()[0].capitalize()
                self.relationships.append((owner, component, "aggregation"))
                self.confidences.append(0.85)

            # Association
            elif any(verb in words for verb in ["manages", "uses", "creates", "updates"]):
                tokens = sent.text.split()
                if len(tokens) >= 3:
                    subject = tokens[0].capitalize()
                    obj = tokens[-1].capitalize()
                    self.relationships.append((subject, obj, "association"))
                    self.confidences.append(0.75)

        return self.relationships

    def generate_plantuml(self):
        uml = "@startuml\n"

        for cls in self.classes:
            uml += f"class {cls}\n"

        for rel in self.relationships:
            source, target, rel_type = rel

            if rel_type == "inheritance":
                uml += f"{source} --|> {target}\n"
            elif rel_type == "aggregation":
                uml += f"{source} o-- {target}\n"
            elif rel_type == "association":
                uml += f"{source} --> {target}\n"

        uml += "@enduml"
        return uml

    def get_confidence_score(self):
        if not self.confidences:
            return 0.0
        return round(sum(self.confidences) / len(self.confidences), 2)
