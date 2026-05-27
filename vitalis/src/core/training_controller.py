import json
import os

BASE_PATH = os.path.expanduser("~/vitalis_core")

class TrainingController:
    def __init__(self):
        self.curriculum_path = os.path.join(BASE_PATH, "storage/curriculum/modules")
        self.log_path = os.path.join(BASE_PATH, "storage/benchmarks/training_log.txt")

    def load_module(self, module_id):
        path = os.path.join(self.curriculum_path, f"{module_id}.json")
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            return json.load(f)

    def run_module(self, module_id, brain):
        module = self.load_module(module_id)
        if not module:
            return {"status": "error", "message": f"Module {module_id} not found"}
        results = []
        for item in module.get("training_data", []):
            response = brain.process(item["input"])
            passed = item["expected"] in response
            results.append({"input": item["input"], "response": response, "passed": passed})
        self.log_results(module_id, results)
        score = sum(1 for r in results if r["passed"]) / len(results) if results else 0
        return {"status": "complete", "score": round(score, 2), "results": results}

    def log_results(self, module_id, results):
        with open(self.log_path, 'a') as f:
            f.write(f"\nModule: {module_id}\n")
            for r in results:
                f.write(f"  {r['input']} -> {r['response']} | {'PASS' if r['passed'] else 'FAIL'}\n")
