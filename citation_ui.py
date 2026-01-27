# frontend/citation_ui.py

import streamlit as st

def render_citations(sources, confidence):
    """
    Renders confidence score and expandable document citations
    in the Streamlit UI.
    """

    # Confidence score
    st.markdown(f"### 🔍 Confidence Score: **{confidence * 100:.0f}%**")

    if not sources:
        st.info("No source documents were used.")
        return

    st.markdown("### 📄 Sources Used")

    for idx, src in enumerate(sources):
        title = f"{idx + 1}. {src['document']} ({src['department']})"
        with st.expander(title):
            st.write(src["text"])
            st.caption(f"Relevance Score: {src['score']}")
