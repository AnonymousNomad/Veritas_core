import os
import sys
import time
from flask import Flask, request, jsonify, render_template_string

# Structural Boot Guard: Enforce localized directory parity before compilation loops
os.makedirs(os.path.join(os.getcwd(), "storage", "knowledge"), exist_ok=True)
os.makedirs(os.path.join(os.getcwd(), "templates"), exist_ok=True)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.core.retrieval_engine import LocalRetrievalEngine
from src.core.memory_engine import MemoryEngine
from brain import get_ripple_payload

app = Flask(__name__)

# Cold-start compilation invocation
try:
    print("[*] Launching system boot-stage hot ingestion...")
    engine = MemoryEngine()
    engine.ingest_knowledge('storage/knowledge')
except Exception as e:
    print(f"[!] Warning: Initial bootstrapping execution anomaly intercepted: {str(e)}")

retriever = LocalRetrievalEngine()

@app.route('/', methods=['GET'])
def index():
    """Renders the offline water-ripple visualization canvas directly to local clients."""
    template_path = os.path.join(os.getcwd(), "templates", "ripple.html")
    if not os.path.exists(template_path):
        return "CRITICAL: Front-end template asset missing from disk.", 404
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)

@app.route('/ripple', methods=['POST'])
def ripple():
    data = request.get_json(force=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Null parameters: text query stream required."}), 400
        
    try:
        payload = get_ripple_payload(text, max_depth=12)
        return jsonify(payload)
    except Exception as e:
        return jsonify({"error": f"Internal cognitive pipeline exception: {str(e)}"}), 500

@app.route('/api/ingest', methods=['POST'])
def hot_ingest():
    data = request.get_json(force=True) or {}
    target_dir = data.get("directory", "storage/knowledge")
    try:
        ingestor = MemoryEngine()
        ingestor.ingest_knowledge(target_dir)
        return jsonify({"status": "SUCCESS", "timestamp": time.time()})
    except Exception as e:
        return jsonify({"error": f"Dynamic hot-ingestion compilation failure: {str(e)}"}), 500

@app.route('/api/query', methods=['POST'])
def semantic_query():
    data = request.get_json() or {}
    query_string = data.get('query', '').strip()
    top_k = int(data.get('top_k', 3))
    
    if not query_string:
        return jsonify({"error": "Missing parameter: query string required"}), 400
    try:
        matches = retriever.query(query_string, top_k=top_k)
        return jsonify({"query": query_string, "results_returned": len(matches), "matches": matches})
    except Exception as e:
        return jsonify({"error": f"Retrieval execution failure: {str(e)}"}), 500

if __name__ == '__main__':
    print("[*] Secure Sovereign UI Gateway staging on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
