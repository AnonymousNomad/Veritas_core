from .rnn_core import TinyGatedRNN
import numpy as np

class VitalisBrain:
    def __init__(self):
        self.rnn = TinyGatedRNN()
        self.hidden = np.zeros(self.rnn.hidden_dim)

    def generate_response(self, text, system_prompt):
        # Local, private inference only
        tokens = [ord(c) % 4000 for c in text]
        for t in tokens:
            _, self.hidden = self.rnn.forward_step(t, self.hidden)
        return "Internal state updated. Logic processed locally."
