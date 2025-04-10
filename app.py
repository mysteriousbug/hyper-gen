import streamlit as st
from PIL import Image

# Configure page
st.set_page_config(page_title="CodeT5: Live Translation", layout="wide")

# Custom CSS for bordered columns
st.markdown("""
<style>
.bordered-column {
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    height: 100%;
}
.translate-btn {
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Logo and title
col_logo, col_title = st.columns([1, 4])
with col_logo:
    try:
        logo = Image.open('image.png')
        st.image(logo, width=80)
    except:
        st.warning("Logo image not found")
with col_title:
    st.title("CodeT5: Live Translation")

# Initialize session state
if 'translated_file' not in st.session_state:
    st.session_state.translated_file = None
if 'source_file' not in st.session_state:
    st.session_state.source_file = None

# Main content - two bordered columns
col1, col2 = st.columns(2)

# Left column - Source
with col1:
    st.markdown('<div class="bordered-column">', unsafe_allow_html=True)
    st.subheader("Source Code")
    source_lang = st.selectbox("Select source language:", ["Python", "Java", "C++"])
    uploaded_file = st.file_uploader("Upload source file", type=["txt", "py", "java", "cpp"])
    
    if uploaded_file is not None:
        st.session_state.source_file = uploaded_file.getvalue().decode("utf-8")
        st.code(st.session_state.source_file, language=source_lang.lower())
    st.markdown("</div>", unsafe_allow_html=True)

# Right column - Target
with col2:
    st.markdown('<div class="bordered-column">', unsafe_allow_html=True)
    st.subheader("Translated Code")
    target_lang = st.selectbox("Select target language:", ["Python", "Java", "C++"])
    
    if st.button("Translate →", key="translate_btn", help="Click to translate the code"):
        if st.session_state.source_file:
            st.session_state.translated_file = f"# Translated to {target_lang}\n{st.session_state.source_file}"
            st.success("Translation complete!")
        else:
            st.warning("Please upload a source file first")
    
    if st.session_state.translated_file:
        st.code(st.session_state.translated_file, language=target_lang.lower())
        st.download_button(
            label="Download Translation",
            data=st.session_state.translated_file,
            file_name=f"translated_code.{target_lang.lower()}",
            mime="text/plain"
        )
    else:
        st.info("Translation will appear here")
    st.markdown("</div>", unsafe_allow_html=True)
