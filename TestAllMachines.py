import random
from ClaudeInterface import ClaudeInterface
from DeepSeekInterface import DSInterface
from GTPInterface import GPTInterface
from MistralInterface import MistralInterface
from ScenarioLoader import ScenarioHolder
import json
import shutil

"""
    Skript zum Ausführen aller Scenarios mit den LLMs
"""

def test_all_models():
    gpt4o = GPTInterface(model="gpt-4o")
    claude = ClaudeInterface()
    mistral = MistralInterface()
    deepSeek = DSInterface()

    models = [claude,gpt4o,mistral,deepSeek]
    for model in models:
        run_all_scenarios(model)

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

def run_all_scenarios(model):
    """
    Runs all test scenarios with different prompt iterations for the given model.
    """
    sh = ScenarioHolder()
    unique_sequence = uniqueid()

    for prompt_index in range(4):
        file_path = f"Data/{model.model}_prompt_{prompt_index}_scenarios.json"
        shutil.copy("Data/scenarios.json", file_path)
        for scenario_id in range(1,7):
            print(f"Starting Scenario {scenario_id}")
            sh.load_scenario(scenario_id)

            # Determine prompt ID based on scenario
            if scenario_id in [4, 5, 6]:
                prompt_id = prompt_index + 4
            else:
                prompt_id = prompt_index

            # Load prompt from JSON
            with open("Data/Prompts.json", "r", encoding="utf-8") as f:
                prompts_data = json.load(f)
            system_prompt = prompts_data[prompt_id]

            promptTitle = system_prompt['Title']
            promptContent = system_prompt["Content"]
            if 'RAG' in promptTitle:
                if 'US' in promptTitle:
                    promptContent = insert_text_remove_keyword(promptContent,prompts_data[9]['Content'],'{RAG}')
                if 'TR' in promptTitle:
                    promptContent = insert_text_remove_keyword(promptContent, prompts_data[8]['Content'], '{RAG}')
            print(f"Loaded prompt {promptTitle}")

            # Start chat with system prompt
            chat_ID = next(unique_sequence)
            model.start_chat(chat_id=chat_ID, system_message=promptContent)
            response = model.send_message(chat_id=chat_ID, user_message=sh.PatientenAntw)
            print(response)

            while True:
                user_input = input()
                if user_input.lower() == "q":
                    print("Finishing conversation...")
                    sh.Log = model.generate_chat_log(chat_id=chat_ID)
                    break
                else:
                    response = model.send_message(chat_id=chat_ID, user_message=user_input)
                    print(response)

            # Finalize scenario
            sh.Log = model.generate_chat_log(chat_id=chat_ID)
            sh.store_scenario(file_path)
            sh.unload_scenario()

def insert_text_remove_keyword(text: str, to_insert: str, key_word: str) -> str:
    """
    Searches for 'key_word' in 'text' and replaces it with 'to_insert'.
    If 'key_word' is not found, returns the original 'text' unchanged.
    """
    idx = text.find(key_word)
    if idx == -1:
        return text

    return text[:idx] + to_insert + text[idx + len(key_word):]

test_all_models()
