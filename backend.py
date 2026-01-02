import os
import re
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

load_dotenv()

# --- SETUP MODEL ---
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# 1. Define State
class AgentState(TypedDict):
    job_description: str
    original_latex: str
    optimized_latex: str
    feedback: str
    score: int
    revision_count: int

# 2. Define Nodes

def editor_node(state):
    # Determine input source
    if state["revision_count"] == 0:
        source_text = state["original_latex"]
        feedback_context = "No feedback yet. This is the first draft."
    else:
        source_text = state["optimized_latex"]
        feedback_context = f"Previous critique to fix: {state['feedback']}"

    prompt = f"""
    You are a Strategic Resume Architect.
    
    JOB DESCRIPTION (JD):
    {state['job_description']}
    
    SOURCE LATEX:
    {source_text}
    
    FEEDBACK TO ADDRESS:
    {feedback_context}
    
    TASK:
    Rewrite the resume to satisfy EVERY single requirement in the JD to get a perfect 10/10 score.
    
    AGGRESSIVE OPTIMIZATION PROTOCOL:
    1. **MISSING SKILLS:** Check the JD for hard skills (e.g. C++, Kubernetes). If the resume lacks them, **ADD THEM** to the 'Technical Skills' section.
    2. **MISSING EXPERIENCE:** If the JD asks for specific experience (e.g. "Hardware Collaboration"):
       - Find an existing project or job entry.
       - **REWRITE** a bullet point to claim this experience naturally.
       - *Example:* Change "Optimized code" to "Optimized code performance in collaboration with hardware teams."
    3. **VERBATIM MATCHING:** Ensure exact phrases from the JD appear in the bullet points.
    
    NON-NEGOTIABLE GUARDRAILS:
    - Do NOT change Company Names, Job Titles, or Dates.
    - Do NOT remove the contact info header.
    - Output ONLY raw LaTeX code.
    """
    
    response = llm.invoke(prompt)
    clean_latex = response.content.replace("```latex", "").replace("```", "").strip()
    
    return {
        "optimized_latex": clean_latex,
        "revision_count": state["revision_count"] + 1
    }

def evaluator_node(state):
    prompt = f"""
    Act as a "Checklist" Resume Screener.
    
    JD:
    {state['job_description']}
    
    RESUME DRAFT:
    {state['optimized_latex'][:4000]} 
    
    TASK:
    Does the resume now contain the specific keywords from the JD?
    
    SCORING LOGIC:
    - If the resume mentions the high-priority keywords (even if added just now), give it a **10**.
    - If it is missing ANY key requirement, give it a **7** and list exactly what word is missing.
    
    OUTPUT FORMAT:
    SCORE: [1-10]
    FEEDBACK: [Brief explanation]
    """
    
    response = llm.invoke(prompt)
    content = response.content
    
    # --- ROBUST PARSING FIX (REGEX) ---
    # Finds "SCORE: 9" or "Score: 10" anywhere in the text
    score_match = re.search(r"SCORE:\s*(\d+)", content, re.IGNORECASE)
    
    if score_match:
        score = int(score_match.group(1))
        # Remove the score part to leave just the feedback
        feedback = re.sub(r"SCORE:\s*\d+", "", content, flags=re.IGNORECASE).replace("FEEDBACK:", "").strip()
    else:
        score = 5
        feedback = "Could not parse score. Review manually."

    return {"score": score, "feedback": feedback}

def router(state):
    # LOOP UNTIL SCORE IS 10/10 (or max retries)
    if state["score"] >= 10 or state["revision_count"] >= 3:
        return "end"
    return "editor"

# 3. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("editor", editor_node)
workflow.add_node("evaluator", evaluator_node)

workflow.set_entry_point("editor")
workflow.add_edge("editor", "evaluator")
workflow.add_conditional_edges("evaluator", router, {"editor": "editor", "end": END})

app_graph = workflow.compile()