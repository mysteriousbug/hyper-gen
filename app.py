import streamlit as st
from PIL import Image
import io

# Configure page
st.set_page_config(page_title="CodeT5: Live Translation", layout="wide")

# Custom CSS with improved card styling
st.markdown("""
<style>
.card-container {
    border-radius: 10px;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    padding: 1.5rem;
    margin: 1rem 0;
    background-color: white;
    border: 1px solid #e0e0e0;
}
.header {
    margin-bottom: 1.5rem;
}
.translate-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}
.download-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 500;
    margin-top: 1rem;
}
.download-btn:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

# Logo and title in header
header = st.container()
with header:
    cols = st.columns([1, 4])
    with cols[0]:
        try:
            logo = Image.open('logo.jpeg')
            st.image(logo, width=80)
        except:
            st.warning("Logo image not found")
    with cols[1]:
        st.markdown("<div class='header'><h1>CodeT5: Live Translation</h1></div>", unsafe_allow_html=True)

# Initialize session state
if 'translated_file' not in st.session_state:
    st.session_state.translated_file = None
if 'source_file' not in st.session_state:
    st.session_state.source_file = None

# Main content columns
col1, col2, col3 = st.columns([5, 1, 5])

# Left card - Source
with col1:
    # Start card container with all content inside
    st.markdown("""
    <div class='card-container'>
        <h2>Source Code</h2>
    """, unsafe_allow_html=True)
    
    # Card content - all Streamlit elements will flow into the div
    source_lang = st.selectbox("Select source language:", ["Python", "Java", "C++"], key="source_lang")
    uploaded_file = st.file_uploader("Upload source file", type=["txt", "py", "java", "cpp"], key="source_uploader")
    
    if uploaded_file is not None:
        st.session_state.source_file = uploaded_file.getvalue().decode("utf-8")
        st.code(st.session_state.source_file, language=source_lang.lower())
    
    # Close the card container
    st.markdown("</div>", unsafe_allow_html=True)
# Middle column with translate button
with col2:
    st.markdown("<div class='translate-btn'>", unsafe_allow_html=True)
    if st.button("⟶ Translate ⟶", key="translate_btn"):
        if st.session_state.source_file:
            # Simulate translation
            st.session_state.translated_file = f"# Translated code\n{st.session_state.source_file}"
            st.success("Translation complete!")
        else:
            st.warning("Please upload a source file first")
    st.markdown("</div>", unsafe_allow_html=True)

# Right card - Target
with col3:
    with st.container():
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        
        # Card content
        st.subheader("Translated Code")
        target_lang = st.selectbox("Select target language:", ["Python", "Java", "C++"], key="target_lang")
        
        if st.session_state.translated_file:
            st.code(st.session_state.translated_file, language=target_lang.lower())
            
            # Download button
            st.download_button(
                label="Download Translation",
                data=st.session_state.translated_file,
                file_name=f"translated_code.{target_lang.lower()}",
                mime="text/plain",
                key="download_btn"
            )
        else:
            st.info("Translation will appear here after processing")
        
        st.markdown("</div>", unsafe_allow_html=True)
