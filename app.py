
import json
from graphviz import Digraph
import streamlit as st
from openai import OpenAI
from groq import Groq
from pydantic import BaseModel

st.set_page_config(page_title="AI DFA Generator", layout="wide")

class DFA(BaseModel):
    alphabet: list[str]
    states: list[dict]
    transitions: list[dict]

st.title("🤖 AI DFA Generator Prototype")
st.sidebar.write("Please use GROQ API KEY u can find here https://console.groq.com/keys")
api_key = st.sidebar.text_input("GROQ API Key", type="password")
model = st.sidebar.text_input("Model", value="openai/gpt-oss-120b")

question = st.text_area(
    "Enter TOC Question",
    value="Construct a DFA over {a,b} that accepts strings ending with abb."
)

PROMPT = """You are a Theory of Computation expert.

Look into the user question and identify what and how to solve it. Follow this step to identify the context of question:
1. Identify the question context
2.what are the TOC topics it covers? to answer the question whetehr is it NFA/DFA/e-NFA/Regular Expression etc....
3.Answer the question in JSON
4. cross check the Answer You Have Generated in JSON 
 4.1. Check is it matching with the question context
 4.2. Analyze the Answer in deep.
 4.2. check the answer correctness?
5. if it fails to answer the question or u find any error or it deosnt matches the user question 
then revert back to step 1.

Priority: Return ONLY valid JSON.

Schema:
{
  "alphabet":["a","b"],
  "states":[
    {"id":"q0","initial":true,"accept":false},
    {"id":"q1","accept":false},
    {"id":"q2","accept":true}
  ],
  "transitions":[
    {"from":"q0","to":"q1","symbol":"a"}
  ]
}
"""

def render_graph(data):
    dot = Digraph("dfa")
    dot.attr(rankdir="LR")

    dot.node("start", shape="point")

    for s in data["states"]:
        shape = "doublecircle" if s.get("accept", False) else "circle"
        dot.node(s["id"], shape=shape)
        if s.get("initial", False):
            dot.edge("start", s["id"])

    for t in data["transitions"]:
        dot.edge(t["from"], t["to"], label=t["symbol"])

    return dot

if st.button("Generate DFA"):
    if not api_key:
        st.error("Enter your API key.")
        st.stop()

    client = Groq(api_key=api_key)

    with st.spinner("Generating DFA..."):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role":"system","content":PROMPT},
                {"role":"user","content":question}
            ],
            response_format={"type":"json_object"}
        )

    raw = response.choices[0].message.content
    data = json.loads(raw)
    DFA.model_validate(data)

    st.success("Generated successfully!")

    with st.expander("Show JSON data"):
        st.subheader("JSON")
        st.json(data)

    st.subheader("DFA Diagram")
    dot = render_graph(data)
    st.graphviz_chart(dot.source)

    st.download_button(
        "Download JSON",
        json.dumps(data, indent=2),
        file_name="dfa.json"
    )
    
    st.markdown(
        """
        <div style='text-align: center; margin-top: 50px;'>
            Made with ❤️ by Sahil <br>
            <a href="https://github.com/Sahilkumar8084" target="_blank">GitHub Profile</a>
        </div>
        """,
        unsafe_allow_html=True
    )


    