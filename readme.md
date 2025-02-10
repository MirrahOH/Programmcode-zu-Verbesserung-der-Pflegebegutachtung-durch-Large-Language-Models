# LLM Evaluation 

Das Projekt beinhaltet das Programm, welches die in der Bachelorarbeit "Verbesserung der Pflegebegutachtung durch Large Language Models: Ein explorativer Ansatz" verwedet wurde, um LLMs auf ihre Fähigkeit hin zu untersuchen, Pflegebegutachtungen durchzuführen.
Teile des Programms wurden mit zur Hilfenahme von LLMs erstellt.

## Übersicht

Das Programm testet verschiedene LLMs (Claude, GPT-4, Mistral, DeepSeek) mit verschiedenen Prompting Strategien:
- System Prompt 
- Few-Shot 
- RAG (simulated Retrieval Augmented Generation)
- RAG + Few-Shot 

## Projektstruktur

### Kernkomponenten

- **Interface Classes**
  - `ClaudeInterface.py` - Interface für die Anthropic's Claude API
  - `GTPInterface.py` - Interface für die OpenAI's GPT API
  - `MistralInterface.py` - Interface für die Mistral AI API
  - `DeepSeekInterface.py` - Interface für die DeepSeek API

- **Data Handling**
  - `ScenarioLoader.py` - Verwaltet das Laden und Speichern der Testfälle
  - `DataRefactor.py` - Kombiniert und exportiert die Testergebnisse

- **Visualization**
  - `Graphs.py` - Erstellt verschiedene Visualisierungsgraphen für die Ergebnisanalyse

- **Test Execution**
  - `TestAllMachines.py` - Hauptscript für die Ausführung der Evaluierungen über alle Modelle


## Setup

1. Installiere die benötigten Abhängigkeiten: 

pip install anthropic openai mistralai python-dotenv matplotlib

2. Erstelle eine `.env` Datei mit deinen API Keys:

ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here

3. Führe das Skript aus:

python TestAllMachines.py

