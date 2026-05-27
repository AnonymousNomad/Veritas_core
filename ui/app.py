from flask import Flask, render_template, request, jsonify
import sys, os
sys.path.insert(0, os.path.expanduser("~/vitalis_core"))
from core.brain import VitalisBrain
from core.talker import VitalisTalker
from src.core.training_controller import TrainingController

app = Flask(__name__)
brain = VitalisBrain()
trainer = TrainingController()

TEMPLATES = {
    "cybersecurity": {"mode": "threat_detection", "focus": "security"},
    "assistant": {"mode": "conversational", "focus": "helpfulness"},
    "research": {"mode": "analytical", "focus": "knowledge"},
    "creative": {"mode": "generative", "focus": "creativity"},
    "education": {"mode": "instructional", "focus": "learning"},
    "developer": {"mode": "technical", "focus": "code"},
    "medical": {"mode": "clinical", "focus": "health"},
    "legal": {"mode": "analytical", "focus": "law"},
    "finance": {"mode": "quantitative", "focus": "markets"},
    "gaming": {"mode": "interactive", "focus": "entertainment"}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    tier = data.get('tier', 'basic')
    user_input = data.get('input', '')
    response = brain.process(user_input)
    return jsonify({
        'response': response if isinstance(response, str) else response.status,
        'cycle': brain.cycle,
        'state': brain.state
    })

@app.route('/template', methods=['POST'])
def load_template():
    data = request.json
    name = data.get('name', '')
    config = TEMPLATES.get(name, {})
    brain.state = config.get('mode', 'aware')
    return jsonify({
        'status': 'loaded',
        'template': name,
        'mode': config.get('mode', 'aware'),
        'focus': config.get('focus', 'general')
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'cycle': brain.cycle,
        'state': brain.state,
        'last_input': brain.last_input
    })
