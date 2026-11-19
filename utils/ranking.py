from constants import RANKING_FILE

# O ranking fica num arquivo de texto, uma partida por linha:  pontos;nome
# Ex:
#   20;Beto
#   12;Ana


def load_ranking():
    """Le os recordes salvos, do maior para o menor. Ex: [{"name": "Beto", "score": 20}, ...]"""
    ranking = []
    try:
        with open(RANKING_FILE, encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(";", 1)
                if len(parts) == 2 and parts[0].isdigit():
                    ranking.append({"name": parts[1], "score": int(parts[0])})
    except FileNotFoundError:
        return []
    return sorted(ranking, key=lambda entry: entry["score"], reverse=True)


def save_score(name, score):
    """Registra uma partida e devolve a posicao dela no ranking (1 = primeiro lugar)."""
    ranking = load_ranking()
    entry = {"name": name.replace(";", " "), "score": score}
    ranking.append(entry)
    # sorted e estavel: em caso de empate, quem fez primeiro fica na frente
    ranking = sorted(ranking, key=lambda e: e["score"], reverse=True)

    with open(RANKING_FILE, "w", encoding="utf-8") as file:
        for e in ranking:
            file.write(f"{e['score']};{e['name']}\n")

    return ranking.index(entry) + 1
