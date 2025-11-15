import gradio as gr
import researchAgent

agent = researchAgent.ResearchAgent()

def load_css():
    with open("style.css", "r") as f:
        css = f.read()
    return css

def run(question):
    summary = agent.research(question)
    return summary

with gr.Blocks() as demo:
    gr.Markdown("# Research Agent")
    gr.Markdown("Ask a question and get a researched summary.")
    
    #input and output components must be side by side
    with gr.Row():
        input_box = gr.Textbox(label="Enter your question here")
        output_box = gr.Textbox(label="Research Summary")
    run_button = gr.Button("Run Research")

    run_button.click(fn=run, inputs=input_box, outputs=output_box)
demo.launch()