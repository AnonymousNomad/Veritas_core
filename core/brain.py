from core.thinker import emit_thought
from core.nexus import route_thought

class VitalisBrain:
    def __init__(self):
        self.state = "aware"

    def process(self, input_data):
        emit_thought(input_data)
        route_thought(input_data)
        return f"PROCESSED: {input_data}"
