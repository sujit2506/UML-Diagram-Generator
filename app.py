import streamlit as st
from uml_engine import UMLGenerator
from plantuml import PlantUML

st.set_page_config(page_title="AI UML Generator", layout="wide")

st.title("🤖 AI-Based UML Diagram Generator")

text_input = st.text_area(
    "Enter SRS Statement",
    height=200,
    placeholder="Example: Admin manages users. User has a profile. Profile is a document."
)

if st.button("Generate UML"):

    engine = UMLGenerator()

    cleaned_text = engine.preprocess(text_input)

    classes = engine.extract_entities(cleaned_text)
    relationships = engine.detect_relationships(cleaned_text)

    plantuml_code = engine.generate_plantuml()
    confidence = engine.get_confidence_score()

    st.subheader("📦 Extracted Classes")
    st.write(classes)

    st.subheader("🔗 Relationships")
    st.write(relationships)

    st.subheader("📊 Confidence Score")
    st.write(confidence)

    st.subheader("🧾 PlantUML Code")
    st.code(plantuml_code, language="text")

    # Render UML Diagram
    st.subheader("🖼 UML Diagram")

    try:
        plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        diagram_url = plantuml.get_url(plantuml_code)
        st.image(diagram_url)
    except:
        st.warning("Could not render UML image. Please check internet connection.")
