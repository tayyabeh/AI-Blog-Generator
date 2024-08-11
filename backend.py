from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import Html2TextTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import pandas as pd
from langchain_community.document_loaders import UnstructuredURLLoader
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import ast

# *******************************

options = Options()
options.add_argument("--headless")  # Ensure headless mode is enabled
options.add_argument("--disable-gpu")  # Optional: Disable GPU hardware acceleration
options.add_argument("--log-level=3")  # Optional: Suppress logging

# Specify the path to the Edge WebDriver executable
service = EdgeService('F:/projects/Ai Blog writer/msedgedriver.exe')

# Initialize the Edge WebDriver with headless options
# driver = webdriver.Edge(service=service, options=options)

# ************************************************


# api_key
genai.configure(api_key='AIzaSyDI-fQEhXTRQMb_FqjEZ-uId_EoDWJb8G4')

# Initialize the Edge WebDriver
driver = webdriver.Edge(service=service, options=options)

driver.get("https://www.google.com/")

text_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//textarea[@title="Search"]'))
    )

# text_area = driver.find_element(By.XPATH,'//textarea[@title="Search"]')

text_area.click()

# driver.implicitly_wait(5)

a = text_area.send_keys("Ai the future ")

# Press the Enter key to submit the search form
text_area.send_keys(Keys.RETURN)

driver.implicitly_wait(5)

# Get the page source
# page_sour = driver.page_source
# print(page_sour[0:100])

# Get the current URL of the search results page
current_url = driver.current_url

    # Find all the search result links
search_results = driver.find_elements(By.XPATH, '//a[@href]')

    # Extract the href attributes
urls = [current_url]
for result in search_results:
    url = result.get_attribute('href')
    if url and url.startswith('http'):
        urls.append(url)

    # Print the URLs
# for url in urls:
#     print(url)

# Print the current URL
# print(f'The current URL is: {current_url}')


loader=AsyncChromiumLoader([current_url])

# url_loaded = loader.load()
# print(url_loaded)
html_transforms = Html2TextTransformer()
docs=html_transforms.transform_documents(loader.load())
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=0)
splitted_docs = text_splitter.split_documents(docs)
# print((splitted_docs[0:2]))


# Create a Gemini model instance
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

prompt_for_reference = f''' You are a helpful intelligent assistant
    Role : your role is i give a text of google search page and you have to find top 5 pages of that searched topic in this template form 
     template :[
     Title : "Write the title name here"
     website: "name of the website here"
     Decription : "Some decription here"
     url : "enter a url here"        
     ]
note : Remember give 5 top pages of search item is based on blog website or article website bcz i have to make an article writing tool so iwant website as a reference so do it for me
so you have to pick those website that is based on article not on news and also youtube videio or other videos and give me json file
and now i am give u  urls so take that url of those top 5 searched item you choose {url}'''



l=[]
for xx in splitted_docs:
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction = prompt_for_reference
    )

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message(f"\n\n{xx}")

# print(type(response.text))

# .........................................................



# Assuming `response.text` is a string that looks like a JSON
response_text = response.text.strip()

# Debug print to see the actual response
print("Raw response text:", response_text)

# Clean the response text if necessary
cleaned_response_text = response_text.replace('```json', '').replace('```', '').strip()


# Parse the cleaned response text as JSON
parsed_response = json.loads(cleaned_response_text)

# Convert the parsed JSON to a pandas DataFrame
df = pd.DataFrame(parsed_response)

# Extract the 'url' column
final_urls = df['url'].tolist()

# Print the final URLs
# for url in final_urls:
#     print(url)

# print(final_urls)

# **************************************************************
# top 5 page  getting and  splitting method

final_urls = df['url'].tolist()
loader = UnstructuredURLLoader(urls=final_urls)
data = loader.load()
# print("printing the length of data :: ")
# print(len(data))
# print(data[0:10])

web_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=0)
web_splitted_docs = text_splitter.split_documents(docs)

# **************************************************************************************
#  Title names suggestion 
for w in web_splitted_docs:
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction = '''
                according to the topic given by user {a} give top 5 suggestion Topic name and please also think abou SEO and then generate the topics
                and give topic name in List form and in json format 
            for eg ::
                json 
                ['Future of Ai','2nd suggested topic'
                ,'3rd suggested topic'
                ,'4th suggested topic'
                ,'5th suggested topic' 
                ]
                give me response like that so i can do function like that and no extra content please  only and only this 
                    '''
    )

chat_session = model.start_chat(
  history=[
  ]
)

response_topics = chat_session.send_message(f"\n\n{w}")
print(response_topics.text)

# Assuming `response.text` is a string that looks like a JSON
response_topics_text = response_topics.text.strip()
# Clean the response text if necessary
cleaned_response_text = response_topics_text.replace('```json', '').replace('```', '').strip()

# Parse the cleaned response text as JSON
parsed_response = json.loads(cleaned_response_text)

# Convert the parsed JSON (which is a list) to a pandas DataFrame
df = pd.DataFrame(parsed_response, columns=["Topics"])

# Extract the 'Topics' column
listed_topics = df['Topics'].tolist()

user_input_topic = int(input("Enter your choice in number: "))
choiced_topic = listed_topics[user_input_topic]
# print(choiced_topic)

    


# **************************************************************************************
#  headings for Topic blog 
for w in web_splitted_docs:
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction = '''
                you work is to give heading accordingly user suggested topic from {choiced_topic} and also take {web_splitted_docs} as a  reference for  
                and generate headings from which you can can understand what type of headings they want  for blog writing of that topic
                note : you have to generate  like 2 introductions haeadings then  body headins for blog , then last thing conclusion based headings    
   give headings in dictionary form
            for eg ::
                {
                 "introduction_headings" : ["heading suggested 1" , "heading suggested 2" , " heading suggested 2", " heasdings suggested 3" ]
                  "body_headings" : ["body head 1","body head 2","body head 3"]
                  "conclusion heading":["conclusion head 1", "conclution head 2","conclusion head 3"]
                  }
                give me response like that so i can do function like that and no extra content please  only and only this not write json or any other stuff
   '''
       )

chat_session = model.start_chat(
  history=[
  ]
)

response_head = chat_session.send_message(f"\n\n{w}")
print(response_head.text)


start = response_head.text.find("{")
end = response_head.text.rfind("}") + 1
dict_string = response_head.text[start:end]

# Convert the string to a dictionary
headings_dict = ast.literal_eval(dict_string)

# Print the dictionary to verify
print(headings_dict)

# Print the dictionary to verify
l=[]
m=[]
for x, y in headings_dict.items():
  l.append(x)
  m.append(y)
  
user_intro = int(input("Enter a choice for intro headings :: "))
intro = m[0][user_intro]
print(intro)

l = []
m = []
for x, y in headings_dict.items():
    l.append(x)
    m.append(y)

print(m[0][0])  # Print the first introduction heading

chosen_body_headings = []
num_choices = int(input(f"Enter the number of body headings you want to choose (1 to {len(m[1])}): "))

for i in range(num_choices):
    user_body = int(input(f"Enter a choice for body heading {i+1} (0 to {len(m[1]) - 1}): "))
    body_heading = m[1][user_body]
    chosen_body_headings.append(body_heading)

# Print the chosen body headings to verify
print("Chosen body headings:")
for heading in chosen_body_headings:
    print(heading)

print(len(m[2]))
user_conc = int(input("Enter a choice for conclusion headings :: "))
conc = m[2][user_conc]
print(conc)

# **************************************************************************************


#                  Article 
# Read the prompt from the file
with open('prompted.txt', 'r') as file:
    prompt_template = file.read()
    file.close()

l=[]
for w in web_splitted_docs:
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction = prompt_template
    )

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message(f"\n\n{w}")
print(response.text)
