import streamlit as st
import pandas as pd
from PIL import Image

# App config
st.set_page_config(layout="wide", page_title="Code Translation Models")
st.title("Neural Network Models for Cross-Language Code Synthesis")

# Load your institution logo (replace with actual path)
# logo = Image.open("bmsce_logo.png")
# st.sidebar.image(logo, width=200)

# Model data - Hyperparameters (from your table)
hyperparameters = {
    "Hyperparameter": ["No. of Transformer Layers", "Max Length", "Embedding Size", 
                      "Vocabulary Size", "No. of Parameters"],
    "TransCoder": [12, 512, 1024, 64001, "100M"],
    "CodeT5": [24, 512, 768, 32100, "220M"],
    "CodeBERT": [12, 512, 768, 50265, "125M"]
}

# Model drawbacks (from your paper)
drawbacks = {
    "Model": ["TransCoder", "CodeT5", "CodeBERT"],
    "Key Challenges": [
        "Struggles with complex syntax (nested loops, recursion)\nRequires manual post-processing",
        "Faces issues with deeply nested logic\nHigher memory requirements",
        "Makes semantic errors in complex control flow\nStruggles with long-range dependencies"
    ],
    "Performance": [
        "CSS: 24.2 (Python→Java)\nOES: 68.7",
        "CSS: 65.0 (Python→Java)\nOES: 72.4",
        "CSS: 60.5 (Python→Java)\nOES: 68.6"
    ]
}

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Model Hyperparameters")
    st.markdown("""
    <style>
    .dataframe th, .dataframe td {
        white-space: nowrap;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    hp_df = pd.DataFrame(hyperparameters)
    st.table(hp_df.style.set_properties(**{
        'background-color': '#f0f2f6',
        'color': '#333',
        'border-color': '#c9d3df'
    }))

    st.subheader("Training Configuration")
    train_config = {
        "Parameter": ["Batch Size", "Learning Rate", "Epochs"],
        "TransCoder": [8, "5e-4", 25],
        "CodeT5": [16, "3e-5", 10],
        "CodeBERT": [12, "2e-5", 15]
    }
    st.table(pd.DataFrame(train_config))

with col2:
    st.header("Model Drawbacks & Performance")
    
    drawbacks_df = pd.DataFrame(drawbacks)
    st.table(drawbacks_df.style.set_properties(**{
        'white-space': 'pre-wrap',
        'text-align': 'left !important'
    }))
    
    st.subheader("Key Insights")
    st.markdown("""
    - **CodeT5** achieves highest CSS (65.0) but requires more memory
    - **TransCoder** needs extensive post-processing for Java output
    - **CodeBERT** shows semantic gaps in control flow translation
    """)
    
    # Visualization
    st.subheader("Performance Comparison")
    perf_data = {
        "Model": ["TransCoder", "CodeBERT", "CodeT5"],
        "CSS": [24.2, 60.5, 65.0],
        "OES": [68.7, 68.6, 72.4]
    }
    st.bar_chart(pd.DataFrame(perf_data).set_index("Model"))

# Add model architecture diagrams
st.header("Model Architectures")
arch_col1, arch_col2, arch_col3 = st.columns(3)

with arch_col1:
    st.image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformer_arch.png", 
             caption="TransCoder: Seq2Seq with Attention")

with arch_col2:
    st.image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/t5_architecture.png", 
             caption="CodeT5: Transformer Encoder-Decoder")

with arch_col3:
    st.image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bert_architecture.png", 
             caption="CodeBERT: BERT Architecture")

# Run with: streamlit run app.py
