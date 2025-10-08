import csv
from itertools import combinations


def lire_fichier_actions(nom_fichier):
    """
    Lit le fichier CSV contenant les informations sur les actions.

    Args:
        nom_fichier (str): Le chemin vers le fichier CSV

    Returns:
        list: Une liste de dictionnaires contenant les informations de chaque action
              Format: [{'nom': 'Action-1', 'cout': 20, 'benefice_pct': 5}, ...]
    """
    actions = []

    # Ouvrir et lire le fichier CSV
    with open(nom_fichier, "r", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)

        # Parcourir chaque ligne du fichier
        for ligne in lecteur:
            # Extraire le nom de l'action
            nom = ligne["Actions #"]

            # Convertir le coût en nombre (float)
            cout = float(ligne["Coût par action (en euros)"])

            # Convertir le bénéfice en nombre (enlever le % et diviser par 100)
            benefice_pct = float(ligne["Bénéfice (après 2 ans)"].replace("%", ""))

            # Ajouter l'action à notre liste
            actions.append({"nom": nom, "cout": cout, "benefice_pct": benefice_pct})

    return actions


def calculer_benefice_total(actions_selectionnees):
    """
    Calcule le coût total et le bénéfice total d'une combinaison d'actions.

    Args:
        actions_selectionnees (list): Liste des actions sélectionnées

    Returns:
        tuple: (cout_total, benefice_total_euros)
    """
    cout_total = 0
    benefice_total_euros = 0

    # Pour chaque action sélectionnée
    for action in actions_selectionnees:
        cout_total += action["cout"]

        # Calculer le bénéfice en euros : coût × pourcentage / 100
        benefice_en_euros = action["cout"] * action["benefice_pct"] / 100
        benefice_total_euros += benefice_en_euros

    return cout_total, benefice_total_euros


def trouver_meilleure_combinaison(actions, budget_max=500):
    """
    Trouve la meilleure combinaison d'actions en testant toutes les possibilités.

    Args:
        actions (list): Liste de toutes les actions disponibles
        budget_max (int): Budget maximum disponible (par défaut 500€)

    Returns:
        dict: Dictionnaire contenant la meilleure solution trouvée
              Format: {'actions': [...], 'cout_total': X, 'benefice_total': Y}
    """
    # On initialise une variable qui va stocker la meilleure solution trouvée.
    meilleure_solution = {"actions": [], "cout_total": 0, "benefice_total": 0}

    # Initialisation du compteur combinaison
    nombre_total_combinaisons = 0

    # Tester toutes les tailles de combinaisons possibles (de 1 à toutes les actions)
    for taille in range(1, len(actions) + 1):

        # Générer toutes les combinaisons de cette taille
        for combinaison in combinations(actions, taille):
            nombre_total_combinaisons += 1

            # Calculer le coût et le bénéfice de cette combinaison
            cout_total, benefice_total = calculer_benefice_total(combinaison)

            # Vérifier si cette combinaison respecte le budget
            if cout_total <= budget_max:

                # Si cette combinaison est meilleure que la précédente, on la garde
                if benefice_total > meilleure_solution["benefice_total"]:
                    meilleure_solution = {
                        "actions": list(combinaison),
                        "cout_total": cout_total,
                        "benefice_total": benefice_total,
                    }

    print(f"\n✓ Nombre total de combinaisons testées : {nombre_total_combinaisons:,}")

    return meilleure_solution


def afficher_resultat(solution):
    """
    Affiche de manière claire les résultats de la meilleure solution trouvée.

    Args:
        solution (dict): Le dictionnaire contenant la meilleure solution
    """
    print("\n" + "=" * 60)
    print("🎯 MEILLEURE COMBINAISON D'INVESTISSEMENT")
    print("=" * 60)

    print(f"\n💰 Coût total : {solution['cout_total']:.2f} €")
    print(f"📈 Bénéfice total après 2 ans : {solution['benefice_total']:.2f} €")
    print(
        f"📊 Rentabilité : {(solution['benefice_total'] / solution['cout_total'] * 100):.2f}%"
    )

    print(f"\n📋 Actions à acheter ({len(solution['actions'])} actions) :")
    print("-" * 60)

    # Afficher chaque action de la solution
    for action in solution["actions"]:
        benefice_euros = action["cout"] * action["benefice_pct"] / 100
        print(
            f"  • {action['nom']:12} | Coût: {action['cout']:6.2f}€ | "
            f"Bénéfice: {action['benefice_pct']:5.1f}% ({benefice_euros:6.2f}€)"
        )

    print("=" * 60)


def main():
    """
    Fonction principale qui orchestre l'exécution du programme.
    """
    print("🚀 Démarrage de l'algorithme d'optimisation d'investissement...")

    # Nom du fichier CSV (à adapter selon votre fichier)
    nom_fichier = "data/actions.csv"

    # Étape 1 : Lire les données du fichier
    print(f"\n📂 Lecture du fichier '{nom_fichier}'...")
    actions = lire_fichier_actions(nom_fichier)
    print(f"✓ {len(actions)} actions chargées avec succès")

    # Étape 2 : Trouver la meilleure combinaison
    # print("\n🔍 Recherche de la meilleure combinaison...")
    print("⏳ Cela peut prendre quelques secondes...")

    meilleure_solution = trouver_meilleure_combinaison(actions, budget_max=500)

    # Étape 3 : Afficher les résultats
    afficher_resultat(meilleure_solution)


# Point d'entrée du programme
if __name__ == "__main__":
    main()
