import streamlit as st
import base64
import os
from model.model import MyModel
from ppt_layouts.ppt_layouts import ppt
from ppt_layouts.get_download_link import get_link


st.set_page_config(
    page_title="PPT Generator",
    page_icon="��",
    layout="wide"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
    .download-link {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #1f77b4;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():

    st.markdown('<h1 class="main-header">�� PPT Generator</h1>', unsafe_allow_html=True)
    

    with st.sidebar:
        st.header("🎨 Presentation Settings")
        
        topic = st.text_input("📝 Topic", placeholder="Enter your presentation topic...")
        
        # Number of slides
        slides = st.number_input("�� Number of Slides", min_value=1, max_value=20, value=5)
        
        layout_options = ["normal", "creative", "modern", "retro"]
        layout = st.selectbox("🎨 Layout Style", layout_options, index=0)
        
        tone_options = ["professional", "casual", "academic", "creative", "formal"]
        tone = st.selectbox("🎭 Tone", tone_options, index=0)
        
        depth_options = ["basic", "intermediate", "advanced", "expert"]
        depth = st.selectbox("📚 Depth Level", depth_options, index=1)
        
        # Color scheme
        st.subheader("🎨 Color Scheme")
        col1, col2 = st.columns(2)
        with col1:
            background_color = st.selectbox(
                "Background Color",
                ["white", "black", "lightblue", "lightgreen", "lightgray", "beige", "lavender"],
                index=0
            )
        with col2:
            text_color = st.selectbox(
                "Text Color", 
                ["black", "white", "darkblue", "darkgreen", "darkred", "purple", "brown"],
                index=0
            )
        
        color_scheme = [background_color, text_color]
        
        st.subheader("🔤 Font Style")
        font_options = ["Arial", "Calibri", "Times New Roman", "Helvetica", "Georgia"]
        title_font = st.selectbox("Title Font", font_options, index=0)
        content_font = st.selectbox("Content Font", font_options, index=1)
        font_style = [title_font, content_font]
        
        generate_button = st.button("🚀 Generate Presentation", type="primary")
    
    # Main content area
    if generate_button:
        if not topic:
            st.error("❌ Please enter a topic!")
            return
        
        with st.spinner("🤖 Generating your presentation..."):
            try:
                # Initialize models
                llm = MyModel()
                ppt_obj = ppt()
                
                # Generate content
                st.info("📝 Generating slide titles...")
                list_of_topics = llm.generate_title_of_slides(topic, slides)
                
                st.info("📄 Generating slide content...")
                list_of_content = llm.generate_content_of_topics(
                    subtopics=list_of_topics, 
                    tone=tone, 
                    depth=depth
                )
                
                st.info("🎨 Creating presentation...")
                
                # Generate PPT based on layout
                if layout == "normal":
                    response = ppt_obj.generate_normal_ppt(
                        topic, list_of_content, list_of_topics, 
                        slides, color_scheme, font_style
                    )
                elif layout == "creative":
                    response = ppt_obj.generate_creative_ppt(
                        topic, list_of_content, list_of_topics, slides
                    )
                elif layout == "modern":
                    response = ppt_obj.generate_modern_ppt(
                        topic, list_of_content, list_of_topics, slides
                    )
                elif layout == "retro":
                    response = ppt_obj.generate_retro_ppt(
                        topic, list_of_content, list_of_topics, slides
                    )
                
                # Get file path
                if isinstance(response, dict):
                    file_path = response['file_path']
                    status_message = response['message']
                else:
                    file_path = response.split("Saved as ")[-1] if "Saved as " in response else ""
                    status_message = response
                
                st.success("✅ Presentation generated successfully!")
                
                # Display results
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.subheader("📋 Slide Titles")
                    for i, title in enumerate(list_of_topics, 1):
                        st.write(f"**Slide {i}:** {title}")
                
                with col2:
                    st.subheader("📄 Slide Content Preview")
                    for i, content in enumerate(list_of_content, 1):
                        with st.expander(f"Slide {i} Content"):
                            st.write(content[:200] + "..." if len(content) > 200 else content)
                
                st.markdown("---")
                st.subheader("📥 Download Your Presentation")
                
                if file_path and os.path.exists(file_path):
                    download_link = get_link(file_path)
                    
                    st.markdown(f"""
                    <div class="download-link">
                        <h4>🎉 Your presentation is ready!</h4>
                        <p>Click the link below to download your {layout.title()} presentation:</p>
                        <a href="{download_link}" download="presentation.pptx" style="
                            display: inline-block;
                            background-color: #1f77b4;
                            color: white;
                            padding: 0.75rem 1.5rem;
                            text-decoration: none;
                            border-radius: 0.5rem;
                            font-weight: bold;
                            margin-top: 1rem;
                        ">📥 Download Presentation</a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="📥 Download (Alternative)",
                            data=file.read(),
                            file_name=f"presentation_{topic.replace(' ', '_')}.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )
                else:
                    st.error("❌ Error: Could not generate download link")
                
            except Exception as e:
                st.error(f"❌ Error generating presentation: {str(e)}")
                st.exception(e)
    
    else:
        # Welcome message
        st.markdown("""
        ### 🎯 Welcome to PPT Generator!
        
        **How to use:**
        1. 📝 Enter your presentation topic in the sidebar
        2. 📊 Choose the number of slides you want
        3. 🎨 Select your preferred layout style
        4. 🎭 Pick the tone and depth level
        5. 🎨 Customize colors and fonts
        6. 🚀 Click "Generate Presentation"
        7. 📥 Download your presentation when ready!
        
        **Available Layouts:**
        - **Normal**: Clean and professional
        - **Creative**: Fun and colorful
        - **Modern**: Sleek and contemporary
        - **Retro**: Classic and nostalgic
        
        Start by filling out the form in the sidebar! 🚀
        """)

if __name__ == "__main__":
    main() 