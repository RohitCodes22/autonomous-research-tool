import gradio as gr
import researchAgent

agent = researchAgent.ResearchAgent()

def run(question):
    summary = agent.research(question)
    return summary

with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo")) as demo:
    gr.HTML("<h1 style='text-align:center;'>Autonomous Research Assistant</h1>")
    gr.Markdown(
        "Ask me a research question and I'll analyze, summarize, and synthesize results autonomously."
    )

    with gr.Row():
        question = gr.Textbox(
            label="Research Question",
            placeholder="e.g. What is the moral significance of Pizza?",
            lines=2,
        )

    submitButton = gr.Button("Run Research", variant="primary")

    output = gr.Textbox(
        label="Summary",
        placeholder="The AI-generated research summary will appear here...",
        lines=15,
    )

    submitButton.click(run, inputs=[question], outputs=[output])

demo.launch()
