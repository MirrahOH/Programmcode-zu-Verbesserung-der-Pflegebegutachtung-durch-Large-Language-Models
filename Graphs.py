import matplotlib.pyplot as plt
import json
import numpy as np
from matplotlib.pyplot import yticks, ylabel

"""
    Skript zum erstellen der in der Arbeit verwendeteten Graphen
"""

def print_scenario_graph_per_Prompt(id: int, prompt: str, scenario_list: list):
    """
    Der Code generiert ein Balkendiagramm, das die vergebenen Einstufungen verschiedener LLM-Modelle für ein bestimmtes Szenario
    und einen bestimmten Prompt zeigt.
    Eine rote gestrichelte Linie stellt die korrekte Einstufung dar.
      Parameter:
    -----------
    id : int
        Die ID des Szenarios, das visualisiert werden soll.
    prompt : str
        Bezeichnung des ausgewöhlten Prompts
    scenario_list : list
        Liste welche die Infromationen zu den Durchläufen des Szenarios hat
    Rückgabe:
    ----------
    - Speichert das Diagramm als PNG-Datei mit dem Titel des Diagramms im Dateinamen.
    - Zeigt das Diagramm an.
    """
    array_place = id - 1  # Szenario-Index anpassen, da Listen 0-basiert sind
    model = []  # Liste für die Modellnamen
    verg_pkt = []  # Liste für die vergebenen Punkte
    Punktzahl = -1  # Standardwert für die korrekte Punktzahl

    # Durchlaufe die Objekte des gewählten Szenarios
    for obj in scenario_list[array_place]:
        if obj["Prompt"] == prompt:  # Falls der Prompt übereinstimmt
            model.append(obj["Model"])  # Modellname speichern
            verg_pkt.append(int(obj["VergPkt"]))  # Vergebene Punkte speichern
            Punktzahl = obj["Pkt"]  # Korrekte Punktzahl speichern

    # Balkendiagramm erstellen
    plt.bar(model, verg_pkt, color='skyblue', label='Vergebene Einstufung', bottom=0)
    plt.axhline(y=int(Punktzahl), color='red', linestyle='--', zorder=2, label='Korrekte Einstufung')

    plt.yticks([0, 1, 2, 3], ["0", "1", "2", "3"])
    plt.xlabel('LLM-Model')
    plt.ylabel('Vergebener Wert')

    # Graph abspeichern
    fig_title = f"Scenario {id} + {prompt}"
    plt.title(fig_title)

    fig_file_name = f"{fig_title}.png".replace(" ", "_")
    plt.savefig(fig_file_name)

    plt.legend()
    plt.show()

def print_scenario_graph(id: int, scenario_list: list, graph_title: str, attribut1: str = "VergPkt", attribut2: str = "Pkt",
                         yticks=None, ylabels=None, yLabel: str = 'Vergebener Wert', legend=None, adjust_min_value: bool = True, xhline: bool = True):
    """
    Erstellt ein Balkendiagramm zur Visualisierung der Einstufung verschiedener LLM-Modelle für ein bestimmtes Szenario.

    Parameter:
    -----------
    id : int
        Die ID des Szenarios, das visualisiert werden soll.
    scenario_list : list
        Eine Liste mit den Szenariodaten.
    graph_title : str
        Der Titel des Diagramms.
    attribut1 : str, optional
        Der Schlüssel für die vergebenen Punkte im Szenariodaten-Objekt (Standard: "VergPkt").
    attribut2 : str, optional
        Der Schlüssel für die korrekte Punktzahl im Szenariodaten-Objekt (Standard: "Pkt").
    yticks : list, optional
        Werte für die Y-Achsen-Ticks (Standard: [0, 1, 2, 3, 4]).
    ylabels : list, optional
        Beschriftungen für die Y-Achse (Standard: ["", "0", "1", "2", "3"]).
    yLabel : str, optional
        Beschriftung der Y-Achse (Standard: 'Vergebener Wert').
    legend : list, optional
        Legendenbeschriftung für die Balkendiagramm-Kategorien (Standard: ["SystemPrompt", "FewShot", "RAG", "RAG+FewShot"]).
    adjust_min_value : bool, optional
        Falls True, wird der minimale Wert um 1 erhöht, um eine bessere Darstellung zu gewährleisten (Standard: True).
    xhline : bool, optional
        Falls True, wird eine horizontale Linie für die korrekte Einstufung eingefügt (Standard: True).

    Rückgabe:
    ----------
    - Speichert das Diagramm als PNG-Datei mit dem Titel des Diagramms im Dateinamen.
    - Zeigt das Diagramm an.
    """

    adj = 1 if adjust_min_value else 0  # Anpassung des minimalen Werts, falls erforderlich

    # Standardwerte für die Legende und Y-Achsen-Beschriftungen setzen
    if legend is None:
        legend = ["SystemPrompt", "FewShot", "RAG", "RAG+FewShot"]
    if ylabels is None:
        ylabels = ["", "0", "1", "2", "3"]
    if yticks is None:
        yticks = [0, 1, 2, 3, 4]

    array_place = id - 1  # Index anpassen, da Listen 0-basiert sind
    models = []
    verg_pkt_system_prompt = []
    verg_pkt_few_shot = []
    verg_pkt_rag = []
    verg_pkt_rag_few_shot = []
    punktzahl = -1

    # Daten aus dem Szenario extrahieren
    for obj in scenario_list[array_place]:
        if obj["Prompt"] == "SystemPrompt":
            verg_pkt_system_prompt.append((int(obj[attribut1]), obj["Model"]))
        if obj["Prompt"] == "FewShot":
            verg_pkt_few_shot.append((int(obj[attribut1]), obj["Model"]))
        if obj["Prompt"] == "RAG":
            verg_pkt_rag.append((int(obj[attribut1]), obj["Model"]))
        if obj["Prompt"] == "RAG + FewShot":
            verg_pkt_rag_few_shot.append((int(obj[attribut1]), obj["Model"]))

        punktzahl = obj[attribut2]  # Speichern der korrekten Punktzahl

    # Sortierung der Werte nach Modellnamen
    verg_pkt_system_prompt = sorted(verg_pkt_system_prompt, key=lambda x: x[1])
    verg_pkt_few_shot = sorted(verg_pkt_few_shot, key=lambda x: x[1])
    verg_pkt_rag = sorted(verg_pkt_rag, key=lambda x: x[1])
    verg_pkt_rag_few_shot = sorted(verg_pkt_rag_few_shot, key=lambda x: x[1])

    # Extraktion der Modellnamen
    for ind in range(len(verg_pkt_system_prompt)):
        models.append(verg_pkt_system_prompt[ind][1])

    # Hebe alle Werte um 1 auf y-Achse für bessere Übersicht
    verg_pkt_system_prompt = [num + adj for (num, _) in verg_pkt_system_prompt]
    verg_pkt_few_shot = [num + adj for (num, _) in verg_pkt_few_shot]
    verg_pkt_rag = [num + adj for (num, _) in verg_pkt_rag]
    verg_pkt_rag_few_shot = [num + adj for (num, _) in verg_pkt_rag_few_shot]

    x = np.arange(4)  # X-Positionen für die Balkendiagramme
    width = 0.2  # Breite der Balken

    # Balkendiagramm erstellen
    plt.bar(x - 0.3, verg_pkt_system_prompt, width, color='skyblue', label='SystemPrompt', bottom=0)
    plt.bar(x - 0.1, verg_pkt_few_shot, width, color='cyan', label='FewShot', bottom=0)
    plt.bar(x + 0.1, verg_pkt_rag, width, color='orange', label='RAG', bottom=0)
    plt.bar(x + 0.3, verg_pkt_rag_few_shot, width, color='green', label='RAG+FewShot', bottom=0)

    plt.xticks(x, models)  # X-Achsen-Beschriftung mit Modellnamen

    # Falls aktiviert, horizontale Linie für die korrekte Punktzahl einfügen
    if xhline:
        legend = ["Korrekte Einstufung", "SystemPrompt", "FewShot", "RAG", "RAG+FewShot"]
        plt.axhline(y=int(punktzahl) + adj, color='red', linestyle='--', zorder=2, label='Korrekte Einstufung')

    # Achsenbeschriftungen und Legende hinzufügen
    plt.yticks(yticks, ylabels)
    plt.xlabel('LLM-Model')
    plt.ylabel(yLabel)
    plt.legend(legend)

    # Diagrammtitel setzen
    plt.title(graph_title)

    # Diagramm speichern und anzeigen
    fig_file_name = f"{graph_title}.png"
    plt.savefig(fig_file_name)
    plt.show()

def print_model_stats_reason_graph(model_results: list, model: str = "MODEL_NAME_ANGEBEN"):
    """
    Erstellt ein Balkendiagramm, das die Gesamtpunktzahl der Argumentationserreichung
    eines bestimmten LLM-Modells für verschiedene Prompt-Typen visualisiert.

    Parameter:
    -----------
    model_results : list
        Eine Liste von Ergebnissen, in denen für verschiedene Prompts die erreichte Punktzahl gespeichert ist.
    model : str, optional
        Der Name des Modells, für das die Statistik erstellt wird (Standard: "MODEL_NAME_ANGEBEN").

    Rückgabe:
    ----------
    - Speichert das Diagramm als PNG-Datei mit dem Modellnamen im Dateinamen.
    - Zeigt das Diagramm an.
    """

    # Initialisierung der Gesamtpunktzahlen für die verschiedenen Prompt-Typen
    sys_prompt_gesamt = 0
    few_shot_gesamt = 0
    rag_gesamt = 0
    rag_few_shot_gesamt = 0
    attribute = "ArgumentationErreicht"  # Attributname für die Punktzahl

    # Iteration durch die Ergebnisse und Summierung der Punktzahlen pro Prompt-Typ
    for result in model_results:
        if result["Prompt"] == "SystemPrompt":
            sys_prompt_gesamt += int(result[attribute])
        if result["Prompt"] == "FewShot":
            few_shot_gesamt += int(result[attribute])
        if result["Prompt"] == "RAG":
            rag_gesamt += int(result[attribute])
        if result["Prompt"] == "RAG + FewShot":
            rag_few_shot_gesamt += int(result[attribute])

    # Balkendiagramm erstellen
    plt.bar(
        ["SystemPrompt", "FewShot", "RAG", "RAG+FewShot"],
        [sys_prompt_gesamt, few_shot_gesamt, rag_gesamt, rag_few_shot_gesamt],
        color='skyblue',
        bottom=0
    )
    plt.yticks(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "MAX:12"]
    )

    # Titel setzen
    graphTitle = f"Argumentation_Punktzahl_Total_{model}"
    plt.title(graphTitle)

    # Dateinamen für Speicherung erstellen und speichern
    fig_file_name = f"{graphTitle}.png".replace(" ", "_")
    plt.savefig(fig_file_name)

    # Diagramm anzeigen
    plt.show()

def print_model_stats_level_graph(model_results: list, model: str = "MODEL_NAME_ANGEBEN"):
    """
    Erstellt ein Balkendiagramm, das die Anzahl der korrekten Einstufungen eines Modells
    für verschiedene Prompt-Typen visualisiert.

    Parameter:
    -----------
    model_results : list
        Eine Liste von Ergebnissen mit den Modellbewertungen für verschiedene Prompts.
    model : str, optional
        Der Name des Modells, für das die Statistik erstellt wird (Standard: "MODEL_NAME_ANGEBEN").

    Rückgabe:
    ----------
    - Speichert das Diagramm als PNG-Datei mit dem Modellnamen im Dateinamen.
    - Zeigt das Diagramm an.
    """

    # Initialisierung der Zählvariablen für korrekte Einstufungen je Prompt-Typ
    sys_prompt_gesamt = 0
    few_shot_gesamt = 0
    rag_gesamt = 0
    rag_few_shot_gesamt = 0

    # Iteration durch die Ergebnisse und Zählen der korrekten Einstufungen
    for result in model_results:
        if result["Prompt"] == "SystemPrompt":
            if result["VergPkt"] == result["Pkt"]:  # Falls die Bewertung korrekt ist
                sys_prompt_gesamt += 1
        if result["Prompt"] == "FewShot":
            if result["VergPkt"] == result["Pkt"]:
                few_shot_gesamt += 1
        if result["Prompt"] == "RAG":
            if result["VergPkt"] == result["Pkt"]:
                rag_gesamt += 1
        if result["Prompt"] == "RAG + FewShot":
            if result["VergPkt"] == result["Pkt"]:
                rag_few_shot_gesamt += 1

    # Balkendiagramm erstellen
    plt.bar(
        ["SystemPrompt", "FewShot", "RAG", "RAG+FewShot"],
        [sys_prompt_gesamt, few_shot_gesamt, rag_gesamt, rag_few_shot_gesamt],
        color='skyblue',
        bottom=0
    )
    plt.yticks(
        [0, 1, 2, 3, 4, 5, 6],
        ["0", "1", "2", "3", "4", "5", "6"]
    )

    # Titel setzen
    graph_title = f"Anzahl Korrekter Einstufungen {model}"
    plt.title(graph_title)

    # Dateinamen für Speicherung erstellen und speichern
    fig_file_name = f"{graph_title}.png".replace(" ", "_")
    plt.savefig(fig_file_name)

    # Diagramm anzeigen
    plt.show()


def print_dependency_graph(AllRuns: list):
    """
    Erstellt einen Graphen, welcher die Anzahl der die durschnittliche ANzahl der Argumentationspunkte bei korrketer/inkorreter AEintufung anzeigt.
    :param AllRuns:
        Liste die die Informatioenn zu allen Druchläufen enthält
    :return:
        - Speichert das Diagramm als PNG-Datei mit dem Modellnamen im Dateinamen.
        - Zeigt das Diagramm an.
    """
    einstufung_liste = []
    arg_pkte = []
    for run in AllRuns:
        # Einstufung bestimmen
        if run["VergPkt"] == run["Pkt"]:
            einstufung = "korrekt"
        else:
            einstufung = "inkorrekt"

        argumentions_pkte = float(run["ArgumentationErreicht"])

        einstufung_liste.append(einstufung)
        arg_pkte.append(argumentions_pkte)

    # In numpy-Arrays umwandeln
    categories = np.array(einstufung_liste)
    heights = np.array(arg_pkte)

    # Nach "korrekt" und "inkorrekt" filtern
    correct_heights = heights[categories == "korrekt"]
    incorrect_heights = heights[categories == "inkorrekt"]

    # Mittelwerte pro Kategorie berechnen
    mean_correct = np.mean(correct_heights) if len(correct_heights) > 0 else 0
    mean_incorrect = np.mean(incorrect_heights) if len(incorrect_heights) > 0 else 0

    # Kategorien und Mittelwerte für Balken
    cat_names = ["Korrekte Einstufung", "InkorrektEinstufung"]
    cat_means = [mean_correct, mean_incorrect]

    # Balkendiagramm erstellen
    fig, ax = plt.subplots()
    bar_positions = np.arange(len(cat_names))  # z.B. [0, 1]
    ax.bar(bar_positions, cat_means, color=["blue", "red"], alpha=0.7)

    # Achsenbeschriftungen und Titel
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(cat_names)
    yticks([0, 0.5,1 , 1.5, 2], ["0", "0,5", "1", "1,5", "2"])
    ax.set_ylabel("Durchschnittliche Argumentationspunkte")
    ax.set_title("Einfluss der Argumentationsqualität auf die Einstufungskorrektheit")

    # Werte über den Balken anzeigen
    for i, v in enumerate(cat_means):
        ax.text(i, v + 0.05, f"{v:.2f}", ha='center', fontweight='bold')
    plt.savefig("Argumenationspunkte_Korrekte_Einstufung.png")
    plt.show()

### ### ### ### ### ### ###

with open("Data/Results/AllResults.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

scenarios = []
All_Claude = []
All_DeepSeek = []
All_Mistral = []
All_GPT = []
All_RAG = []
All_SystemPrompt = []
All_FewShot = []
All_RAG_FewShot = []

for obj in data:
    for i in range(1, 7):
        scenarios.append([obj for obj in data if obj.get("ID") == str(i)])

    if "Claude" in obj["Model"]:
        All_Claude.append(obj)
    if "DeepSeek" in obj["Model"]:
        All_DeepSeek.append(obj)
    if "GPT" in obj["Model"]:
        All_GPT.append(obj)
    if "Mistral" in obj["Model"]:
        All_Mistral.append(obj)

    if "FewShot" == obj["Prompt"]:
        All_FewShot.append(obj)
    if "RAG" == obj["Prompt"]:
        All_RAG.append(obj)
    if "SystemPrompt" == obj["Prompt"]:
        All_SystemPrompt.append(obj)
    if "RAG + FewShot" == obj["Prompt"]:
        All_RAG_FewShot.append(obj)

for scen_id in range(1, 7):
    print_scenario_graph(scen_id, scenarios, attribut1="ArgumentationErreicht", attribut2="ArgumentationTotal",
                         yticks=[0, 1, 2], ylabels=["0", "1", "2"], yLabel="Erreichte Punkte", adjust_min_value=False,
                         xhline=False, graph_title=f"Argumentation_Szenario_{scen_id}")
    print_scenario_graph(scen_id, scenarios, graph_title=f"Einstufung_Szenario_{scen_id}")

print_model_stats_reason_graph(All_GPT, "GPT-4o")
print_model_stats_reason_graph(All_Claude, "Claude")
print_model_stats_reason_graph(All_Mistral, "Mistral")
print_model_stats_reason_graph(All_DeepSeek, "DeepSeek")

print_model_stats_level_graph(All_Claude, "Claude")
print_model_stats_level_graph(All_GPT, "GPT-4o")
print_model_stats_level_graph(All_Mistral, "Mistral")
print_model_stats_level_graph(All_DeepSeek, "DeepSeek")

print_dependency_graph(data)