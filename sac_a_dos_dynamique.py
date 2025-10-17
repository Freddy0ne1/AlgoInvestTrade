"""
Algorithme du Sac à Dos - Programmation Dynamique
==================================================

Ce programme trouve la MEILLEURE combinaison d'actions avec un budget limité.
Il utilise la programmation dynamique pour garantir la solution OPTIMALE.

Différence avec le glouton :
- Glouton : Rapide mais approximatif
- Dynamique : Un peu plus lent mais OPTIMAL (meilleure solution garantie)
"""

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

    # Calculer le bénéfice en euros
    # Exemple : 100€ × 20% / 100 = 20€ de bénéfice
    benefice_euros = cout * benefice_pct / 100

    return {
        "nom": nom,
        "cout": cout,
        "benefice_pct": benefice_pct,
        "benefice_euros": benefice_euros,
    }


def algorithme_sac_a_dos(actions, budget_max=500):
    """
    Trouve la MEILLEURE combinaison d'actions avec programmation dynamique.

    Cette fonction garantit la solution OPTIMALE (pas d'approximation).

    Principe :
    - Construit une table qui stocke les meilleures solutions
    - Pour chaque action, décide : la prendre ou pas ?
    - Garde toujours le meilleur choix

    Args:
        actions (list): Liste de toutes les actions disponibles
        budget_max (float): Budget maximum disponible (défaut: 500€)

    Returns:
        dict: Solution optimale avec actions sélectionnées, coût et bénéfice total
    """
    print("\n🔧 Construction de la table de programmation dynamique...")

    # ASTUCE : Travailler en centimes pour éviter les problèmes avec les décimales
    # Exemple : 12.50€ devient 1250 centimes (nombre entier)
    budget_centimes = int(budget_max * 100)

    # Convertir les actions en centimes
    actions_centimes = convertir_actions_en_centimes(actions)

    # Créer la table de programmation dynamique
    table = creer_table_dynamique(actions_centimes, budget_centimes)

    # Retrouver quelles actions ont été sélectionnées
    actions_selectionnees = retrouver_actions(
        actions, actions_centimes, table, budget_centimes
    )

    # Calculer les totaux
    return calculer_solution(actions_selectionnees)


def convertir_actions_en_centimes(actions):
    """
    Convertit les coûts et bénéfices en centimes.

    Pourquoi ? Pour éviter les problèmes avec les nombres à virgule (float).
    Exemple : 12.50€ → 1250 centimes

    Args:
        actions (list): Liste des actions en euros

    Returns:
        list: Liste des actions en centimes
    """
    actions_centimes = []

    for action in actions:
        actions_centimes.append(
            {
                **action,  # Garder toutes les infos originales
                "cout_centimes": int(action["cout"] * 100),
                "benefice_centimes": int(action["benefice_euros"] * 100),
            }
        )

    return actions_centimes


def creer_table_dynamique(actions_centimes, budget_centimes):
    """
    Crée et remplit la table de programmation dynamique.

    La table stocke : Pour chaque action et chaque budget,
    quel est le meilleur bénéfice possible ?

    Args:
        actions_centimes (list): Actions en centimes
        budget_centimes (int): Budget en centimes

    Returns:
        list: Table 2D avec les meilleures solutions
    """
    n = len(actions_centimes)

    # Étape 1 : Créer une table vide (remplie de 0)
    # Lignes : 0 à n (nombre d'actions + 1)
    # Colonnes : 0 à budget_centimes
    table = [[0] * (budget_centimes + 1) for _ in range(n + 1)]

    # Étape 2 : Remplir la table ligne par ligne
    for i in range(1, n + 1):
        action = actions_centimes[i - 1]
        cout = action["cout_centimes"]
        benefice = action["benefice_centimes"]

        # Pour chaque budget possible
        for b in range(budget_centimes + 1):

            # QUESTION : Prendre ou ne pas prendre cette action ?

            # OPTION 1 : Ne pas prendre l'action
            ne_pas_prendre = table[i - 1][b]

            # OPTION 2 : Prendre l'action (si possible)
            if cout <= b:
                prendre = table[i - 1][b - cout] + benefice
            else:
                prendre = 0  # Impossible (pas assez de budget)

            # Garder la meilleure option
            table[i][b] = max(ne_pas_prendre, prendre)

    print("✓ Table construite avec succès")

    return table


def retrouver_actions(actions, actions_centimes, table, budget_centimes):
    """
    Retrouve quelles actions ont été sélectionnées (backtracking).

    En remontant dans la table, on peut voir quelles actions ont été prises.

    Args:
        actions (list): Actions originales (en euros)
        actions_centimes (list): Actions en centimes
        table (list): Table de programmation dynamique
        budget_centimes (int): Budget en centimes

    Returns:
        list: Liste des actions sélectionnées
    """
    print("🔍 Reconstruction de la solution...")

    n = len(actions_centimes)
    actions_selectionnees = []

    # Variables pour remonter dans la table
    i = n
    b = budget_centimes

    # Remonter dans la table
    while i > 0 and b > 0:

        # Si la valeur a changé par rapport à la ligne du dessus,
        # c'est qu'on a pris cette action
        if table[i][b] != table[i - 1][b]:
            # Ajouter l'action originale (en euros)
            actions_selectionnees.append(actions[i - 1])
            # Retirer son coût du budget
            b -= actions_centimes[i - 1]["cout_centimes"]

        i -= 1

    # Inverser car on a construit à l'envers
    actions_selectionnees.reverse()

    print(f"✓ {len(actions_selectionnees)} actions sélectionnées")

    return actions_selectionnees


def calculer_solution(actions_selectionnees):
    """
    Calcule le coût total et le bénéfice total d'une liste d'actions.

    Args:
        actions_selectionnees (list): Liste des actions sélectionnées

    Returns:
        dict: Dictionnaire avec actions, coût total et bénéfice total
    """
    cout_total = sum(action["cout"] for action in actions_selectionnees)
    benefice_total = sum(action["benefice_euros"] for action in actions_selectionnees)

    return {
        "actions": actions_selectionnees,
        "cout_total": cout_total,
        "benefice_total": benefice_total,
    }


def afficher_resultat(solution, temps_execution):
    """
    Affiche les résultats de manière claire et structurée.

    Args:
        solution (dict): La solution trouvée
        temps_execution (float): Le temps d'exécution en secondes
    """
    print("\n" + "=" * 70)
    print("🎯 MEILLEURE COMBINAISON (Programmation Dynamique - OPTIMAL)")
    print("=" * 70)

    print(f"\n⏱️  Temps d'exécution : {temps_execution:.6f} secondes")
    print(f"💰 Coût total : {solution['cout_total']:.2f} €")
    print(f"📈 Bénéfice total après 2 ans : {solution['benefice_total']:.2f} €")

    if solution["cout_total"] > 0:
        rentabilite = (solution["benefice_total"] / solution["cout_total"]) * 100
        print(f"📊 Rentabilité : {rentabilite:.2f}%")

    afficher_tableau_actions(solution["actions"])


def afficher_tableau_actions(actions):
    """
    Affiche le tableau détaillé des actions sélectionnées.

    Args:
        actions (list): Liste des actions à afficher
    """
    print(f"\n📋 Actions à acheter ({len(actions)} actions) :")
    print("-" * 70)
    print(f"{"Action":<15} {"Coût":>10} {"Bénéfice %":>12} {"Bénéfice €":>12}")
    print("-" * 70)

    for action in actions:
        print(
            f"{action['nom']:<15} {action['cout']:>9.2f}€ "
            f"{action['benefice_pct']:>12.1f}% "
            f"{action['benefice_euros']:>11.2f}€"
        )

    print("=" * 70)


def main():
    """
    Fonction principale qui orchestre l'exécution du programme.
    """
    print("🚀 Algorithme du Sac à Dos - Programmation Dynamique")
    print("=" * 70)
    print("Ce programme garantit la solution OPTIMALE !")
    print("=" * 70)

    # Lire les données
    nom_fichier = "data/actions.csv"
    print(f"\n📂 Lecture du fichier '{nom_fichier}'...")
    actions = lire_fichier_actions(nom_fichier)
    print(f"✓ {len(actions)} actions valides chargées")

    # Appliquer l'algorithme
    print(f"\n🔍 Recherche de la solution optimale...")
    temps_debut = time.time()
    solution = algorithme_sac_a_dos(actions, budget_max=500)
    temps_execution = time.time() - temps_debut

    # Afficher les résultats
    afficher_resultat(solution, temps_execution)

    # Message de performance
    print("\n✅ Optimisation terminée avec succès !")
    print("💡 Cette solution est GARANTIE comme étant la meilleure possible !")

    if temps_execution < 1.0:
        print(f"⚡ Excellent ! Temps : {temps_execution:.6f}s (< 1 seconde)")
    else:
        print(f"⚠️  Temps : {temps_execution:.2f}s (> 1 seconde)")


# Point d'entrée du programme
if __name__ == "__main__":
    main()
