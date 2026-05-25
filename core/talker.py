class VitalisTalker:
    def __init__(self, tier="basic"):
        self.tier = tier

    def speak(self, response):
        print(f"[VITALIS/{self.tier.upper()}]: {response}")
        return response
