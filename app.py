import streamlit as st
from PIL import Image
import io

# Configure page
st.set_page_config(page_title="CodeT5: Live Translation", layout="wide")

# Logo and title
col1, col2 = st.columns([1, 4])
with col1:
    # Load your logo image (replace 'image.png' with your actual image file)
    try:
        logo = Image.open('image.png')
        st.image(logo, width=100)
    except:
        st.warning("Logo image not found")

with col2:
    st.title("CodeT5: Live Translation")

# Custom CSS for styling
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    margin: 10px;
    background-color: #f9f9f9;
}
.centered {
    display: flex;
    justify-content: center;
    align-items: center;
}
.download-btn {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for file handling
if 'translated_file' not in st.session_state:
    st.session_state.translated_file = None
if 'source_file' not in st.session_state:
    st.session_state.source_file = None

# Two cards layout
col1, col2, col3 = st.columns([5, 1, 5])

# Left card - Source
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Source Code")
    
    # Dropdown menu
    source_lang = st.selectbox("Select source language:", 
                              ["a", "b", "c"], 
                              key="source_lang")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload source file", 
                                   type=["txt", "py", "java", "cpp"],
                                   key="source_uploader")
    
    if uploaded_file is not None:
        st.session_state.source_file = uploaded_file.getvalue().decode("utf-8")
        st.code(st.session_state.source_file)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Middle column with translate button
with col2:
    st.write("")  # Spacer
    st.write("")  # Spacer
    if st.button("⟶ Translate ⟶", key="translate_btn"):
        if st.session_state.source_file:
            # Simulate translation (replace with actual translation logic)
            st.session_state.translated_file = f"Translated version of:\n{st.session_state.source_file}"
            st.success("Translation complete!")
        else:
            st.warning("Please upload a source file first")

# Right card - Target
with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Translated Code")
    
    # Dropdown menu
    target_lang = st.selectbox("Select target language:", 
                              ["a", "b", "c"], 
                              key="target_lang")
    
    # Display translated file and download button
    if st.session_state.translated_file:
        st.code(st.session_state.translated_file)
        
        # Create download button
        download_str = st.session_state.translated_file
        st.download_button(
            label="Download Translation",
            data=download_str,
            file_name=f"translated_code.{target_lang}",
            mime="text/plain"
        )
    else:
        st.info("Translation will appear here")
    
    st.markdown("</div>", unsafe_allow_html=True)
