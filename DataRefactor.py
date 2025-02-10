import os
import json

"""
    Skript zum Zusammenfügen und Exportieren der Versuchsergebnisse
"""
def combine_json_files(folder_path, output_file):
    """
        Erwartet eine JSON Datei mit einer Liste von Dicts
        und führt diese zu einer großen Liste zusammen
    """
    combined_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json') :
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Wenn data eine Liste ist, erweitern
                if isinstance(data, list):
                    combined_data.extend(data)
                # Wenn ein einzelnes Objekt, anhängen
                elif isinstance(data, dict):
                    combined_data.append(data)
                # Andernfalls überspringen oder passende Logik ergänzen

    # Zusammengeführte Daten in eine Ausgabedatei schreiben
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)

def write_scenarios_to_txt(input_file, output_file):
    """
    Erwartet eube JSON Datei mit einer Liste von Dicts welche: 'ID','Model','Prompt','Log' enthalten.
    Schreibt eine Textdeatei in folgendem Format:
      ## Scenario_{ID}_{Model}_{Prompt}

      {LOG}
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_file, 'w', encoding='utf-8') as f:
        for obj in data:
            scenario_header = f"## Scenario_{obj['ID']}_{obj['Model']}_{obj['Prompt']}\n\n"
            scenario_log = f"{obj['Log']}\n\n"
            f.write(scenario_header + scenario_log)


# # # # # # # # # # # # # # #
#combine_json_files("Data/Results", "Data/Results/AllResults.json")
write_scenarios_to_txt("Data/Results/AllResults.json", "scenarios_output.md")