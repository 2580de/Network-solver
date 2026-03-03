import os
import json
import requests # Make sure to: pip install requests

class MultiSolver:
    def __init__(self, mode='local'):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = 'network_map.json' if mode == 'local' else 'public_targets.json'
        self.data_path = os.path.join(self.base_dir, 'data', filename)
        self.inventory = set()
        self.path = []

    def run_web_check(self, url):
        """Simulates 'browsing' the internet target"""
        try:
            print(f"[*] Browsing to {url}...")
            # In a real tool, you would use requests.get(url) here
            return True
        except:
            return False

    def solve(self, targets, current_key):
        node = targets[current_key]
        
        # 1. Action: 'Browse' or 'Scan'
        if self.run_web_check(current_key):
            reward = node['provides']
            self.inventory.add(reward)
            self.path.append(current_key)
            print(f"    [+] Found: {reward}")

            # 2. Check Goal
            if reward == "data_exfiltration" or reward == "root_access":
                return True

            # 3. Branching
            for key, details in targets.items():
                if key not in self.path:
                    if details['requires'] == "none" or details['requires'] in self.inventory:
                        if self.solve(targets, key):
                            return True
        
        # Backtrack
        self.path.pop()
        return False

if __name__ == "__main__":
    # Choose mode: 'local' or 'public'
    mode = input("Enter mode (local/public): ").strip().lower()
    engine = MultiSolver(mode=mode)
    
    with open(engine.data_path, 'r') as f:
        data = json.load(f)
    
    # Identify the starting point (requires: none)
    targets = data['nodes'] if mode == 'local' else data['targets']
    start_point = next(k for k, v in targets.items() if v['requires'] == "none")

    print(f"\n--- Starting {mode.upper()} Pathfinder ---")
    if engine.solve(targets, start_point):
        print(f"\n UCCESSFUL PATH:\n" + " -> \n".join(engine.path))
    else:
        print("\n No valid path through these targets.")
