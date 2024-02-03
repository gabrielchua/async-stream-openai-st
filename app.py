"""
app.py
"""
import streamlit as st
import asyncio
from openai import AsyncOpenAI

try:
  client = AsyncOpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
  client = AsyncOpenAI()

st.set_page_config(
    page_title="OpenAI Async Stream Demo",
    layout="wide",
)

st.title("Demo: Async streaming of OpenAI output")
with st.sidebar:
    topic_1 = st.text_input("Essay Topic 1")
    topic_2 = st.text_input("Essay Topic 2")
    word_count = st.number_input("Word Count", value=200, step=100, max_value=300)
    generate = st.button("Generate")

col1, col2 = st.columns(2)

essay_1 = col1.empty()
essay_2 = col2.empty()

@st.partial
async def generate_essay(placeholder, topic, word_count):
    stream = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": f"Write a {word_count} word essay on {topic}. The first line is a 2-3 word title with an emoji and then include 2 line breaks. For example 'TITLE <emoji> \n \n ' "},],
        stream=True
    )
    streamed_text = "# "
    async for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            streamed_text = streamed_text + chunk_content
            placeholder.info(streamed_text)

async def main():
    await asyncio.gather(
        generate_essay(essay_1, topic=topic_1, word_count=word_count),
        generate_essay(essay_2, topic=topic_2, word_count=word_count)
    )

if generate:
    if topic_1 == "" or topic_2 == "":
        st.warning("Please enter both topics")
    else:
        asyncio.run(main())
