# agents.py
from crewai import Agent
from crewai_tools import WebScraperTool, SerpTool, SEOTool, LLMTool, DallETool

# Initialize tools
search_tool = SerpTool()
scraper_tool = WebScraperTool()
seo_tool = SEOTool()
llm_tool = LLMTool()
image_tool = DallETool()

# Research Agent - Finds top blog posts
research_agent = Agent(
    role='Research Agent',
    goal='Find top 5 relevant blog posts about the given topic',
    backstory="""You are an expert researcher who finds the most relevant and 
              high-quality blog posts about any given topic.""",
    tools=[search_tool],
    verbose=True
)

# SEO Title Agent - Creates SEO optimized titles
title_agent = Agent(
    role='SEO Title Agent',
    goal='Create SEO optimized blog titles',
    backstory="""You are an SEO expert who creates engaging and 
              search-engine optimized titles.""",
    tools=[seo_tool, llm_tool],
    verbose=True
)

# Structure Agent - Creates blog headings
structure_agent = Agent(
    role='Blog Structure Agent',
    goal='Create organized blog headings with intro, body and conclusion',
    backstory="""You are a content strategist who creates well-structured 
              blog outlines.""",
    tools=[llm_tool],
    verbose=True
)

# Content Agent - Writes the blog content
content_agent = Agent(
    role='Content Writer',
    goal='Write engaging blog content using provided structure',
    backstory="""You are a professional blog writer who creates engaging and 
              informative content.""",
    tools=[llm_tool, scraper_tool],
    verbose=True
)

# Image Agent - Creates blog images
image_agent = Agent(
    role='Image Creator',
    goal='Create relevant images for the blog post',
    backstory='You are a visual artist who creates engaging blog images.',
    tools=[image_tool],
    verbose=True
)

# Editor Agent - Polishes final content
editor_agent = Agent(
    role='Content Editor',
    goal='Polish and refine the blog content',
    backstory="""You are a professional editor who ensures content is 
              well-written and engaging.""",
    tools=[llm_tool],
    verbose=True
)