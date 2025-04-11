import streamlit as st

# Configure page
st.set_page_config(page_title="CodeT5: Live Translation", layout="wide")

# Title only (logo removed)
st.title("CodeT5: Live Translation")

# Initialize session state
if 'translated_file' not in st.session_state:
    st.session_state.translated_file = None
if 'source_file' not in st.session_state:
    st.session_state.source_file = None

# Main content - two clean columns
col1, col2 = st.columns(2)

# Left column - Source (with translate button)
with col1:
    st.subheader("Source Code")
    source_lang = st.selectbox("Select source language:", ["Python", "Java", "C++"])
    uploaded_file = st.file_uploader("Upload source file", type=["txt", "py", "java", "cpp"])
    
    if uploaded_file is not None:
        st.session_state.source_file = uploaded_file.getvalue().decode("utf-8")
        st.code(st.session_state.source_file, language=source_lang.lower())
        
        # Translate button now properly in source column
        if st.button("Translate →", key="translate_btn"):
            # Get target language from right column
            target_lang = st.session_state.get('target_lang', 'Python')
            st.session_state.translated_file = f"# Translated to {target_lang}\n{st.session_state.source_file}"
            st.success("Translation complete!")

# Right column - Target (display only)
with col2:
    st.subheader("Translated Code")
    target_lang = st.selectbox("Select target language:", ["Python", "Java", "C++"], key="target_lang_select")
    
    if st.session_state.translated_file:
        st.code(st.session_state.translated_file, language=target_lang.lower())
        st.download_button(
            label="Download Translation",
            data=st.session_state.translated_file,
            file_name=f"translated_code.{target_lang.lower()}",
            mime="text/plain"
        )
    else:
        st.info("Upload a file and click Translate to see results")
