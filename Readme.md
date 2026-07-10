# 🤖 AI DFA Generator (Prototype)

A prototype AI-powered Theory of Computation (TOC) assistant that generates **Deterministic Finite Automata (DFA)** from natural language questions.

## Features

* Generate DFA using AI
* Visualize DFA using Graphviz
* Display structured JSON output
* Validate JSON using Pydantic
* Simple Streamlit interface

## Tech Stack

* Python
* Streamlit
* Graphviz
* Pydantic
* Groq API

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Usage

1. Enter your Groq API Key.
2. Enter a TOC question.
3. Click **Generate DFA**.
4. View the generated DFA diagram and JSON.

### Example Prompt

```text
Construct a DFA over {a,b} that accepts all strings ending with abb.
```

## Current Status

🚧 This is an early prototype.

### Planned Features

* String Simulation
* JFLAP Export
* NFA Support
* PDA Support
* Turing Machine Support
* DFA Minimization
* Regex Conversion
* Interactive Visualization

---

Made for experimenting with AI-assisted automata generation.
