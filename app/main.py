import os
from openai import OpenAI
import researchAgent

# Agentic AI - make the research function autonomous and able to decide on its own without constant user input 

question = input("Enter your research question: ")
agent = researchAgent.ResearchAgent()
summary = agent.research(question)
print("\nResearch Summary:\n")
print(summary)