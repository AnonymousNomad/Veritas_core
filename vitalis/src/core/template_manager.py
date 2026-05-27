import json

class TemplateManager:
    """
    Handles loading and applying user-selected templates.
    """
    def __init__(self, profile_path="storage/templates/user_profiles.json"):
        self.profile_path = profile_path

    def load_template(self, template_name):
        # Logic to swap model configuration based on template
        print(f"Loading template: {template_name}")
        with open(self.profile_path, 'r+') as f:
            data = json.load(f)
            data['active_template'] = template_name
            f.seek(0)
            json.dump(data, f, indent=4)
        return True
