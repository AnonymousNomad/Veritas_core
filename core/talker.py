class VitalisTalker:
    def __init__(self, tier="basic"):
        self.tier = tier

    def speak(self, response):
        prefix = {
            "kids": "[VITALIS]: ",
            "basic": "[VITALIS]: ",
            "enthusiast": "[VITALIS/DEV]: ",
            "professional": "[VITALIS/ARCHITECT]: ",
            "school": "[VITALIS/EDU]: "
        }.get(self.tier, "[VITALIS]: ")
        output = f"{prefix}{response}"
        print(output)
        return output
