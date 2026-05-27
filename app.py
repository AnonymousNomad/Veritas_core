import gradio as gr
from src.core.memory_engine import MemoryEngine

# Initialize the Sovereign Brain
brain = MemoryEngine()
brain.ingest_knowledge('storage/knowledge')

def vitalis_chat(user_message, history):
    # Retrieve relevant protocol from local vector store
    response = brain.query(user_message)
    return f"[VITALIS_CORE_UI]: {response}"

demo = gr.ChatInterface(
    fn=vitalis_chat,
    title="Vitalis Synthetic Intelligence | Sovereign Core",
    theme="soft"
)

if __name__ == "__main__":
    demo.launch()
