import json
"""
    Klasse welche das laden der Scenarios und deren Ergebnisse übernimmt
"""
class ScenarioHolder:
    def __init__(self):
        self.PatientenAntw = None
        self.Pkt = None
        self.ID = None
        self.VergPkt = None
        self.Log = None

    def load_scenario(self,scenario_id):
        """Loads a CSV file and assigns the attributes to the ScenarioHolder."""
        try:
            with open('Data/scenarios.json') as f:
                loadedScenarios = json.load(f)
            for scenario in loadedScenarios:
                if scenario['ID'] == str(scenario_id):
                    self.PatientenAntw = scenario['Content']
                    self.Pkt = scenario['Pkt']
                    self.ID = scenario['ID']
                    self.VergPkt = scenario['VergPkt']
                    self.Log = scenario['Log']
                    print("Scenario loaded successfully.")
                    return
            print("Scenario not found.")
            return None
        except FileNotFoundError:
            print("The file 'scenarios.json' does not exist.")
        except KeyError as e:
            print(f"Missing expected column in JSON: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def store_scenario(self, filename: str):
        """Updates the scenario with the current scenario's ID in the JSON file."""

        # 1. Read the existing JSON data
        with open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # 2. Update the scenario with matching ID
        for scenario in data:
            if scenario['ID'] == str(self.ID):
                print(f"updating {filename}", scenario['ID'])
                scenario['VergPkt'] = self.VergPkt
                scenario['Log'] = self.Log
                break

        # 3. Overwrite the existing JSON file with the modified data
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def print_scenario(self):
        """Prints out the variables stored in the ScenarioHolder."""
        print("Scenario Details:")
        print(f"ID: {self.ID}")
        print(f"PatientenAntw: {self.PatientenAntw}")
        print(f"Pkt: {self.Pkt}")
        print(f"VergPkt: {self.VergPkt}")
        print(f"Log: {self.Log}")

    def unload_scenario(self):
        self.PatientenAntw = None
        self.Pkt = None
        self.ID = None
        self.VergPkt = None
        self.Log = None