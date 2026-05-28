import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class SovereignTransformer:
    """
    Loads a pre-trained causal LM and exposes a single encode() method 
    that returns a single vector (the hidden state of the last token, L2-normalized).
    """
    def __init__(self, model_name: str = "facebook/opt-125m", device: str = None):
        # Default to CPU to ensure stable execution on ARM64 architectures
        self.device = device or "cpu"
        
        # Use float32 to prevent PyTorch 'Half' unimplemented errors on native CPU
        self.dtype = torch.float32

        print(f"[*] Initializing Sovereign Generative Backbone: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=self.dtype,
            low_cpu_mem_usage=True,
        ).to(self.device)

        self.model.eval()

    def encode(self, text: str) -> torch.Tensor:
        """Returns a single L2-normalized vector (shape = (dim,))."""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(self.device)

        with torch.no_grad():
            hidden = self.model.base_model(
                **inputs,
                output_hidden_states=False,
                return_dict=True,
            ).last_hidden_state

        # Extract the final token state
        vec = hidden[:, -1, :]
        vec = torch.nn.functional.normalize(vec, p=2, dim=-1)
        return vec.squeeze(0)

    @property
    def dim(self) -> int:
        return self.model.config.hidden_size
