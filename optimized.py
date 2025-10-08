import csv
import time


def lire_fichier_actions(nom_fichier):
    """
    Lit le fichier CSV contenant les informations sur les actions.

    Args:
        nom_fichier (str): Le chemin vers le fichier CSV

    Returns:
        list: Une liste de dictionnaires contenant les informations de chaque action
    """
    actions = []

    with open(nom_fichier, "r", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)

        for ligne in lecteur:
            action = creer_action_depuis_ligne(ligne)
            if action:  # Ajouter seulement si l'action est valide
                actions.append(action)

    return actions


def creer_action_depuis_ligne(ligne):
    """
    Crée un dictionnaire d'action à partir d'une ligne CSV.

    Args:
        ligne (dict): Une ligne du fichier CSV

    Returns:
        dict ou None: Dictionnaire de l'action ou None si invalide
    """
    nom = ligne["Actions #"]
    cout = float(ligne["Coût par action (en euros)"])
    benefice_pct = float(ligne["Bénéfice (après 2 ans)"].replace("%", ""))

    # Ignorer les actions avec un coût ou bénéfice négatif ou nul
    if cout <= 0 or benefice_pct <= 0:
        return None

    # Calculer le ratio de rentabilité (bénéfice / coût)
    ratio_rentabilite = benefice_pct / cout

    return {
        "nom": nom,
        "cout": cout,
        "benefice_pct": benefice_pct,
        "ratio": ratio_rentabilite,
    }


def algorithme_glouton(actions, budget_max=500):
    """
    Trouve la meilleure combinaison d'actions avec un algorithme glouton.

    Args:
        actions (list): Liste de toutes les actions disponibles
        budget_max (float): Budget maximum disponible

    Returns:
        dict: Solution avec actions sélectionnées, coût et bénéfice total
    """
    # Trier par ratio de rentabilité décroissant
    actions_triees = sorted(actions, key=lambda a: a["ratio"], reverse=True)

    actions_selectionnees = []
    budget_restant = budget_max

    # Sélectionner les actions une par une
    for action in actions_triees:
        if action["cout"] <= budget_restant:
            actions_selectionnees.append(action)
            budget_restant -= action["cout"]

    return calculer_solution(actions_selectionnees)


def calculer_solution(actions_selectionnees):
    """
    Calcule le coût total et le bénéfice total d'une liste d'actions.

    Args:
        actions_selectionnees (list): Liste des actions sélectionnées

    Returns:
        dict: Dictionnaire avec actions, coût total et bénéfice total
    """
    cout_total = sum(action["cout"] for action in actions_selectionnees)

    benefice_total = sum(
        action["cout"] * action["benefice_pct"] / 100
        for action in actions_selectionnees
    )

    return {
        "actions": actions_selectionnees,
        "cout_total": cout_total,
        "benefice_total": benefice_total,
    }


def afficher_entete():
    """
    Affiche l'en-tête du résultat.
    """
    print("\n" + "=" * 60)
    print("🎯 MEILLEURE COMBINAISON (Algorithme Glouton)")
    print("=" * 60)


def afficher_metriques(solution, temps_execution):
    """
    Affiche les métriques de la solution (temps, coût, bénéfice).

    Args:
        solution (dict): La solution trouvée
        temps_execution (float): Le temps d'exécution en secondes
    """
    print(f"\n⏱️  Temps d'exécution : {temps_execution:.6f} secondes")
    print(f"💰 Coût total : {solution['cout_total']:.2f} €")
    print(f"📈 Bénéfice total après 2 ans : {solution['benefice_total']:.2f} €")

    if solution["cout_total"] > 0:
        rentabilite = (solution["benefice_total"] / solution["cout_total"]) * 100
        print(f"📊 Rentabilité : {rentabilite:.2f}%")


def afficher_tableau_actions(actions):
    """
    Affiche le tableau détaillé des actions sélectionnées.

    Args:
        actions (list): Liste des actions à afficher
    """
    print(f"\n📋 Actions à acheter ({len(actions)} actions) :")
    print("-" * 60)
    print(
        f"{"Action":<15} {"Coût":>10} {"Bénéfice %":>12} {"Bénéfice €":>12} {"Ratio":>10}"
    )
    print("-" * 60)

    for action in actions:
        benefice_euros = action["cout"] * action["benefice_pct"] / 100
        print(
            f"{action["nom"]:<15} {action["cout"]:>9.2f}€ "
            f"{action["benefice_pct"]:>12.1f}% "
            f"{benefice_euros:>11.2f}€ "
            f"{action["ratio"]:>10.4f}"
        )

    print("=" * 60)


def afficher_resultat(solution, temps_execution):
    """
    Affiche les résultats complets de la solution.

    Args:
        solution (dict): La solution trouvée
        temps_execution (float): Le temps d'exécution en secondes
    """
    afficher_entete()
    afficher_metriques(solution, temps_execution)
    afficher_tableau_actions(solution["actions"])


def afficher_statistiques(actions):
    """
    Affiche des statistiques sur le dataset d'actions.

    Args:
        actions (list): Liste de toutes les actions
    """
    print("\n📊 STATISTIQUES DU DATASET")
    print("-" * 60)
    print(f"Nombre total d'actions : {len(actions)}")

    if actions:
        cout_min = min(a["cout"] for a in actions)
        cout_max = max(a["cout"] for a in actions)
        cout_moyen = sum(a["cout"] for a in actions) / len(actions)

        benefice_min = min(a["benefice_pct"] for a in actions)
        benefice_max = max(a["benefice_pct"] for a in actions)
        benefice_moyen = sum(a["benefice_pct"] for a in actions) / len(actions)

        print(
            f"Coût : Min={cout_min:.2f}€ | Max={cout_max:.2f}€ | Moy={cout_moyen:.2f}€"
        )
        print(
            f"Bénéfice : Min={benefice_min:.1f}% | Max={benefice_max:.1f}% | Moy={benefice_moyen:.1f}%"
        )

    print("-" * 60)


def afficher_message_performance(temps_execution):
    """
    Affiche un message sur la performance du programme.

    Args:
        temps_execution (float): Le temps d'exécution en secondes
    """
    print("\n✅ Optimisation terminée avec succès !")

    if temps_execution < 1.0:
        print(
            f"⚡ Excellent ! Le programme a répondu en {temps_execution:.6f}s (< 1 seconde)"
        )
    else:
        print(
            f"⚠️  Attention : Le programme a pris {temps_execution:.2f}s (> 1 seconde)"
        )


def main():
    """
    Fonction principale qui orchestre l'exécution du programme optimisé.
    """
    print("🚀 Démarrage de l'algorithme d'optimisation (Version Glouton)")
    print("=" * 60)

    # Lire les données
    nom_fichier = "data/actions.csv"
    print(f"\n📂 Lecture du fichier '{nom_fichier}'...")
    actions = lire_fichier_actions(nom_fichier)
    print(f"✓ {len(actions)} actions valides chargées")

    # Statistiques
    afficher_statistiques(actions)

    # Optimisation
    print("\n🔍 Recherche de la meilleure combinaison...")
    temps_debut = time.time()
    solution = algorithme_glouton(actions, budget_max=500)
    temps_execution = time.time() - temps_debut

    # Affichage
    afficher_resultat(solution, temps_execution)
    afficher_message_performance(temps_execution)


# Point d'entrée du programme
if __name__ == "__main__":
    main()
