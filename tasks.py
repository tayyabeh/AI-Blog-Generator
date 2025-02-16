# tasks.py
from crewai import Task
from agents import (
    research_agent, title_agent, structure_agent,
    content_agent, image_agent, editor_agent
)

def get_research_task(topic):
    return Task(
        description=f"""Find the top 5 most relevant blog posts about {topic}.
                    Return list with title and URL for each.""",
        agent=research_agent
    )

def get_title_task(topic):
    return Task(
        description=f"""Create 5 SEO-optimized titles for a blog about {topic}.
                    Make them engaging and search-friendly.""",
        agent=title_agent
    )

def get_structure_task(topic, title):
    return Task(
        description=f"""Create blog structure for '{title}' about {topic}.
                    Include:
                    - 3 introduction section headings
                    - 4-5 body section headings
                    - 3 conclusion section headings""",
        agent=structure_agent
    )

def get_content_task(topic, title, headings, sources):
    return Task(
        description=f"""Write blog post about {topic} titled '{title}'.
                    Use these headings: {headings}
                    Reference these sources: {sources}""",
        agent=content_agent
    )

def get_image_task(topic, content):
    return Task(
        description=f"""Create 2-3 relevant images for blog about {topic}.
                    Content: {content}""",
        agent=image_agent
    )

def get_editor_task(content):
    return Task(
        description="""Polish and refine the blog post. Ensure it's engaging,
                    well-structured and free of errors.""",
        agent=editor_agent
    )