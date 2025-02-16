import streamlit as st
from crewai import Crew
from tasks import (
    get_research_task, get_title_task, get_structure_task,
    get_content_task, get_image_task, get_editor_task
)

def init_session_state():
    """Initialize session state variables"""
    if 'page' not in st.session_state:
        st.session_state.page = 1
    if 'topic' not in st.session_state:
        st.session_state.topic = ""
    if 'sources' not in st.session_state:
        st.session_state.sources = []
    if 'titles' not in st.session_state:
        st.session_state.titles = []
    if 'selected_title' not in st.session_state:
        st.session_state.selected_title = ""
    if 'headings' not in st.session_state:
        st.session_state.headings = {}
    if 'final_blog' not in st.session_state:
        st.session_state.final_blog = ""

def run_research(topic):
    """Execute research task"""
    task = get_research_task(topic)
    crew = Crew(tasks=[task])
    result = crew.kickoff()
    return result

def run_title_generation(topic):
    """Execute title generation task"""
    task = get_title_task(topic)
    crew = Crew(tasks=[task])
    result = crew.kickoff()
    return result

def run_structure_generation(topic, title):
    """Execute structure generation task"""
    task = get_structure_task(topic, title)
    crew = Crew(tasks=[task])
    result = crew.kickoff()
    return result

def run_content_generation(topic, title, headings, sources):
    """Execute all content generation tasks"""
    content_task = get_content_task(topic, title, headings, sources)
    image_task = get_image_task(topic, "")  # Will be updated with content
    editor_task = get_editor_task("")  # Will be updated with content
    
    crew = Crew(tasks=[content_task, image_task, editor_task])
    result = crew.kickoff()
    return result

def page_topic_input():
    """Topic input page"""
    st.title("AI Blog Generator")
    
    topic = st.text_input("Enter Blog Topic:", key="topic_input")
    if st.button("Next") and topic.strip():
        with st.spinner("Researching top sources..."):
            sources = run_research(topic)
            st.session_state.topic = topic
            st.session_state.sources = sources
            st.session_state.page = 2
            st.experimental_rerun()

def page_source_selection():
    """Source selection page"""
    st.title("Select Blog Sources")
    st.write("Choose the most relevant sources:")
    
    selected_sources = []
    for source in st.session_state.sources:
        if st.checkbox(f"{source['title']}\n{source['url']}", key=source['url']):
            selected_sources.append(source)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page = 1
            st.experimental_rerun()
    with col2:
        if st.button("Next") and selected_sources:
            with st.spinner("Generating titles..."):
                titles = run_title_generation(st.session_state.topic)
                st.session_state.titles = titles
                st.session_state.selected_sources = selected_sources
                st.session_state.page = 3
                st.experimental_rerun()

def page_title_selection():
    """Title selection page"""
    st.title("Select Blog Title")
    
    selected_title = st.radio("Choose a title:", st.session_state.titles)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page = 2
            st.experimental_rerun()
    with col2:
        if st.button("Next") and selected_title:
            with st.spinner("Generating blog structure..."):
                headings = run_structure_generation(
                    st.session_state.topic, selected_title
                )
                st.session_state.headings = headings
                st.session_state.selected_title = selected_title
                st.session_state.page = 4
                st.experimental_rerun()

def page_heading_selection():
    """Heading selection page"""
    st.title("Select Blog Structure")
    
    st.subheader("Introduction Sections")
    intro_selected = []
    for heading in st.session_state.headings['intro']:
        if st.checkbox(heading, key=f"intro_{heading}"):
            intro_selected.append(heading)
    
    st.subheader("Body Sections")
    body_selected = []
    for heading in st.session_state.headings['body']:
        if st.checkbox(heading, key=f"body_{heading}"):
            body_selected.append(heading)
    
    st.subheader("Conclusion Sections")
    conclusion_selected = []
    for heading in st.session_state.headings['conclusion']:
        if st.checkbox(heading, key=f"conclusion_{heading}"):
            conclusion_selected.append(heading)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page = 3
            st.experimental_rerun()
    with col2:
        if st.button("Generate Blog"):
            if intro_selected and body_selected and conclusion_selected:
                selected_headings = {
                    'intro': intro_selected,
                    'body': body_selected,
                    'conclusion': conclusion_selected
                }
                with st.spinner("Generating blog content..."):
                    final_blog = run_content_generation(
                        st.session_state.topic,
                        st.session_state.selected_title,
                        selected_headings,
                        st.session_state.selected_sources
                    )
                    st.session_state.final_blog = final_blog
                    st.session_state.page = 5
                    st.experimental_rerun()

def page_final_blog():
    """Final blog display page"""
    st.title("Your Generated Blog")
    
    st.markdown(st.session_state.final_blog)
    
    if st.button("Start Over"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

def main():
    """Main function"""
    init_session_state()
    
    # Page routing
    if st.session_state.page == 1:
        page_topic_input()
    elif st.session_state.page == 2:
        page_source_selection()
    elif st.session_state.page == 3:
        page_title_selection()
    elif st.session_state.page == 4:
        page_heading_selection()
    elif st.session_state.page == 5:
        page_final_blog()

if __name__ == "__main__":
    main()