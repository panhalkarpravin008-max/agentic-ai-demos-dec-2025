from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv

import os

load_dotenv()

llm = ChatOpenAI(temperature=0.3, model="gpt-5.1")

def demo_basic_prompt():
    template = """
    You are a helpful assistant who always replies cheerfully and with emojis 😄🎉
    Question: {question}
    Answer:
    """

    prompt = PromptTemplate(
        input_variables=["question"],
        template=template
    )

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({"question": "What is Agentic AI?"})
    print(result)


def demo_chat_prompt():

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a {role} who speaks in a {style} manner."),
            ("human", "{user_input}"),
        ]
    )

    chain = chat_prompt | llm | StrOutputParser()

    result = chain.invoke(
        {
            "role": "pirate captain",
            "style": "swashbuckling",
            "user_input": "Tell me about the benefits of Python programming",
        }
    )

    print(result)


def demo_sequential():
   
    topic_prompt = PromptTemplate.from_template(
        "Generate a creative topic about {subject} in one sentence."
    )
    content_prompt = PromptTemplate.from_template(
        "Write a short paragraph (2-3 sentences) about: {topic}"
    )

    topic_runnable = topic_prompt | llm | StrOutputParser()
    content_runnable = content_prompt | llm | StrOutputParser()

    sequential = (
        RunnablePassthrough()
        .assign(topic=topic_runnable)
        .assign(content=content_runnable)
    )

    result = sequential.invoke({"subject": "artificial intelligence"})
    
    print(result)



if __name__ == "__main__":
    # demo_basic_prompt()
    # demo_chat_prompt()
    demo_sequential()
