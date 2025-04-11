import streamlit as st

# Configure page
st.set_page_config(page_title="CodeT5: Live Translation", layout="wide")

# Title
st.title("CodeT5: Live Translation")

# Initialize session state
if 'translated_file' not in st.session_state:
    st.session_state.translated_file = None
if 'source_file' not in st.session_state:
    st.session_state.source_file = None

# Main content - two columns
col1, col2 = st.columns(2)

# Left column - Source input
with col1:
    st.subheader("Source Code")
    source_lang = st.selectbox("Select source language:", ["Python", "Java", "C++"])
    
    # Text input box for direct code entry
    source_code = st.text_area("Or type your code here:", height=200, 
                             placeholder="Enter your source code here...")
    
    # File uploader
    uploaded_file = st.file_uploader("Or upload a file:", type=["txt", "py", "java", "cpp"])
    
    # Determine source (text input or file)
    if source_code or uploaded_file:
        if uploaded_file:
            st.session_state.source_file = uploaded_file.getvalue().decode("utf-8")
        else:
            st.session_state.source_file = source_code
            
        st.code(st.session_state.source_file, language=source_lang.lower())
        
        # Translate button
        if st.button("Translate →", key="translate_btn"):
            target_lang = st.session_state.get('target_lang', 'Python')
            st.session_state.translated_file = f"# Translated to {target_lang}\n{st.session_state.source_file}"
            st.success("Translation complete!")

# Right column - Translation output
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
        st.info("Enter code or upload a file, then click Translate")
