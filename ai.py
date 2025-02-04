from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

import re

def output_Cleaner(text):
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned_text.strip()
def llm_user_response(user_Data):

    template = """
    Make a short brief about this user based in the data provided to you.

    Username: {name},
    Followers: {followers},
    Person's Interests: {likes},
    """

    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="deepseek-r1:latest")

    chain = prompt | model

    return output_Cleaner(chain.invoke({"name": user_Data[1], "followers": user_Data[3], "likes": user_Data[4]}))