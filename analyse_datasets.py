"""
Analyse des Datasets Historiques - AlgoInvest&Trade
====================================================

Ce programme analyse les datasets historiques et compare les résultats
des algorithmes avec les décisions d'investissement de Sienna.

Fonctionnalités :
- Lecture et nettoyage des données
- Test des algorithmes (Glouton et Dynamique)
- Comparaison avec les choix de Sienna
- Génération d'un rapport complet
"""

import csv
import time


# ============================================================================
# PARTIE 1 : LECTURE ET NETTOYAGE DES DONNÉES
# ============================================================================


def lire_dataset(nom_fichier):
    """
    Lit un fichier CSV de dataset et retourne les actions valides.

    Format attendu : name,price,profit

    Filtre automatiquement :
    - Prix <= 0
    - Profit <= 0
    - Données manquantes

    Args:
        nom_fichier (str): Chemin vers le fichier CSV

    Returns:
        tuple: (liste des actions valides, compteur de rejets)
    """
    print(f"\n📂 Lecture du fichier '{nom_fichier}'...")

    actions_valides = []

    # Compteurs pour les statistiques
    total_lignes = 0
    lignes_valides = 0
    prix_invalides = 0
    profit_invalides = 0

    with open(nom_fichier, "r", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)

        for ligne in lecteur:
            total_lignes += 1

            # Essayer de créer une action
            action = creer_action_depuis_dataset(ligne)

            if action is None:
                # Compter pourquoi elle a été rejetée
                try:
                    prix = float(ligne.get("price", 0))
                    profit = float(ligne.get("profit", 0))

                    if prix <= 0:
                        prix_invalides += 1
                    if profit <= 0:
                        profit_invalides += 1
                except:
                    pass
            else:
                actions_valides.append(action)
                lignes_valides += 1

    # Afficher les statistiques
    lignes_rejetees = total_lignes - lignes_valides
    print(f"✓ {total_lignes} lignes lues")
    print(
        f"  → {lignes_valides} actions valides ({lignes_valides/total_lignes*100:.1f}%)"
    )
    print(
        f"  → {lignes_rejetees} actions rejetées ({lignes_rejetees/total_lignes*100:.1f}%)"
    )

    if lignes_rejetees > 0:
        print(f"     • Prix invalides : {prix_invalides}")
        print(f"     • Profit invalides : {profit_invalides}")

    return actions_valides, {
        "total": total_lignes,
        "valides": lignes_valides,
        "rejetees": lignes_rejetees,
    }


def creer_action_depuis_dataset(ligne):
    """
    Crée une action à partir d'une ligne de dataset.

    Format : name,price,profit

    Args:
        ligne (dict): Ligne du CSV

    Returns:
        dict ou None: Action si valide, None sinon
    """
    try:
        nom = ligne.get("name", "").strip()
        prix = float(ligne.get("price", 0))
        profit_pct = float(ligne.get("profit", 0))

        # Vérifier la validité
        if not nom or prix <= 0 or profit_pct <= 0:
            return None

        # Calculer le bénéfice en euros
        benefice_euros = prix * profit_pct / 100

        return {
            "nom": nom,
            "cout": prix,
            "benefice_pct": profit_pct,
            "benefice_euros": benefice_euros,
        }
    except:
        return None


# ============================================================================
# PARTIE 2 : ALGORITHMES
# ============================================================================


def algorithme_glouton(actions, budget_max=500):
    """
    Algorithme glouton : trie par ratio et prend les meilleures.

    Args:
        actions (list): Liste des actions
        budget_max (float): Budget maximum

    Returns:
        dict: Solution trouvée
    """
    # Calculer les ratios
    for action in actions:
        action["ratio"] = action["benefice_pct"] / action["cout"]

    # Trier par ratio décroissant
    actions_triees = sorted(actions, key=lambda a: a["ratio"], reverse=True)

    # Sélectionner les actions
    actions_selectionnees = []
    budget_restant = budget_max

    for action in actions_triees:
        if action["cout"] <= budget_restant:
            actions_selectionnees.append(action)
            budget_restant -= action["cout"]

    return calculer_solution(actions_selectionnees)


def algorithme_dynamique(actions, budget_max=500):
    """
    Algorithme de programmation dynamique (sac à dos).

    Args:
        actions (list): Liste des actions
        budget_max (float): Budget maximum

    Returns:
        dict: Solution optimale
    """
    # Convertir en centimes
    budget_centimes = int(budget_max * 100)

    actions_centimes = []
    for action in actions:
        actions_centimes.append(
            {
                **action,
                "cout_centimes": int(action["cout"] * 100),
                "benefice_centimes": int(action["benefice_euros"] * 100),
            }
        )

    n = len(actions_centimes)

    # Créer la table
    table = [[0] * (budget_centimes + 1) for _ in range(n + 1)]

    # Remplir la table
    for i in range(1, n + 1):
        action = actions_centimes[i - 1]
        cout = action["cout_centimes"]
        benefice = action["benefice_centimes"]

        for b in range(budget_centimes + 1):
            ne_pas_prendre = table[i - 1][b]

            if cout <= b:
                prendre = table[i - 1][b - cout] + benefice
            else:
                prendre = 0

            table[i][b] = max(ne_pas_prendre, prendre)

    # Backtracking
    actions_selectionnees = []
    i = n
    b = budget_centimes

    while i > 0 and b > 0:
        if table[i][b] != table[i - 1][b]:
            actions_selectionnees.append(actions[i - 1])
            b -= actions_centimes[i - 1]["cout_centimes"]
        i -= 1

    actions_selectionnees.reverse()

    return calculer_solution(actions_selectionnees)


def calculer_solution(actions_selectionnees):
    """
    Calcule les totaux d'une solution.

    Args:
        actions_selectionnees (list): Actions sélectionnées

    Returns:
        dict: Solution avec totaux
    """
    cout_total = sum(a["cout"] for a in actions_selectionnees)
    benefice_total = sum(a["benefice_euros"] for a in actions_selectionnees)

    return {
        "actions": actions_selectionnees,
        "cout_total": cout_total,
        "benefice_total": benefice_total,
    }


# ============================================================================
# PARTIE 3 : DONNÉES DE SIENNA
# ============================================================================


def obtenir_choix_sienna_dataset1():
    """
    Retourne les choix de Sienna pour le dataset 1.

    Returns:
        dict: Choix de Sienna
    """
    return {"actions": ["Share-GRUT"], "cout_total": 498.76, "benefice_total": 196.61}


def obtenir_choix_sienna_dataset2():
    """
    Retourne les choix de Sienna pour le dataset 2.

    Returns:
        dict: Choix de Sienna
    """
    return {
        "actions": [
            "Share-ECAQ",
            "Share-IXCI",
            "Share-FWBE",
            "Share-ZOFA",
            "Share-PLLK",
            "Share-YFVZ",
            "Share-ANFX",
            "Share-PATS",
            "Share-NDKR",
            "Share-ALIY",
            "Share-JWGF",
            "Share-JGTW",
            "Share-FAPS",
            "Share-VCAX",
            "Share-LFXB",
            "Share-DWSK",
            "Share-XQII",
            "Share-ROOM",
        ],
        "cout_total": 489.24,
        "benefice_total": 193.78,
    }


# ============================================================================
# PARTIE 4 : AFFICHAGE ET COMPARAISON
# ============================================================================


def afficher_solution(titre, solution, temps=None):
    """
    Affiche une solution de manière formatée.

    Args:
        titre (str): Titre de la solution
        solution (dict): Solution à afficher
        temps (float): Temps d'exécution (optionnel)
    """
    print(f"\n{titre}")
    print("-" * 70)

    if temps is not None:
        print(f"⏱️  Temps d'exécution  : {temps:.6f} secondes")

    nb_actions = len(solution["actions"])
    print(f"🛒 Nombre d'actions   : {nb_actions}")
    print(f"💰 Coût total         : {solution['cout_total']:.2f}€")
    print(f"📈 Bénéfice total     : {solution['benefice_total']:.2f}€")

    if solution["cout_total"] > 0:
        rentabilite = (solution["benefice_total"] / solution["cout_total"]) * 100
        print(f"📊 Rentabilité        : {rentabilite:.2f}%")


def comparer_solutions(algo, sienna, nom_dataset):
    """
    Compare la solution de l'algorithme avec celle de Sienna.

    Args:
        algo (dict): Solution de l'algorithme
        sienna (dict): Solution de Sienna
        nom_dataset (str): Nom du dataset
    """
    print(f"\n{'='*70}")
    print(f"⚖️  COMPARAISON - {nom_dataset}")
    print(f"{'='*70}")

    diff_benefice = algo["benefice_total"] - sienna["benefice_total"]
    diff_cout = algo["cout_total"] - sienna["cout_total"]

    # Tableau comparatif
    print(f"\n{'Métrique':<25} {'Algorithme':>15} {'Sienna':>15} {'Différence':>15}")
    print("-" * 70)

    nb_algo = len(algo["actions"])
    nb_sienna = len(sienna["actions"])
    print(
        f"{'Nombre d\'actions':<25} {nb_algo:>15} {nb_sienna:>15} {nb_algo-nb_sienna:>15}"
    )
    print(
        f"{'Coût total':<25} {algo['cout_total']:>14.2f}€ {sienna['cout_total']:>14.2f}€ {diff_cout:>14.2f}€"
    )
    print(
        f"{'Bénéfice total':<25} {algo['benefice_total']:>14.2f}€ {sienna['benefice_total']:>14.2f}€ {diff_benefice:>14.2f}€"
    )

    if algo["cout_total"] > 0 and sienna["cout_total"] > 0:
        rent_algo = (algo["benefice_total"] / algo["cout_total"]) * 100
        rent_sienna = (sienna["benefice_total"] / sienna["cout_total"]) * 100
        diff_rent = rent_algo - rent_sienna
        print(
            f"{'Rentabilité':<25} {rent_algo:>14.2f}% {rent_sienna:>14.2f}% {diff_rent:>14.2f}%"
        )

    # Verdict
    print(f"\n{'='*70}")
    print("🏆 VERDICT")
    print(f"{'='*70}")

    if diff_benefice > 0.01:
        pct = (diff_benefice / sienna["benefice_total"]) * 100
        print(f"\n✅ L'ALGORITHME EST MEILLEUR de {diff_benefice:.2f}€ (+{pct:.2f}%)")
    elif diff_benefice < -0.01:
        pct = (abs(diff_benefice) / sienna["benefice_total"]) * 100
        print(f"\n⚠️  SIENNA EST MEILLEURE de {abs(diff_benefice):.2f}€ (+{pct:.2f}%)")
    else:
        print(f"\n🎯 LES DEUX SOLUTIONS SONT ÉQUIVALENTES !")


# ============================================================================
# PARTIE 5 : ANALYSE COMPLÈTE D'UN DATASET
# ============================================================================


def analyser_dataset(fichier, nom, choix_sienna, algo="glouton"):
    """
    Analyse complète d'un dataset.

    Args:
        fichier (str): Chemin du fichier
        nom (str): Nom du dataset
        choix_sienna (dict): Choix de Sienna
        algo (str): Algorithme à utiliser ("glouton" ou "dynamique")
    """
    print(f"\n{'='*70}")
    print(f"🔍 ANALYSE : {nom}")
    print(f"{'='*70}")

    # Lecture et nettoyage
    actions, stats = lire_dataset(fichier)

    if len(actions) == 0:
        print("❌ Aucune action valide trouvée !")
        return

    # Application de l'algorithme
    print(f"\n🤖 Application de l'algorithme {algo}...")
    temps_debut = time.time()

    if algo == "glouton":
        solution = algorithme_glouton(actions, budget_max=500)
    else:
        solution = algorithme_dynamique(actions, budget_max=500)

    temps_exec = time.time() - temps_debut

    # Affichage
    afficher_solution(
        f"🤖 RÉSULTAT DE L'ALGORITHME {algo.upper()}", solution, temps_exec
    )
    afficher_solution("👤 CHOIX DE SIENNA", choix_sienna)

    # Comparaison
    comparer_solutions(solution, choix_sienna, nom)


# ============================================================================
# PARTIE 6 : FONCTION PRINCIPALE
# ============================================================================


def main():
    """
    Fonction principale du programme d'analyse.
    """
    print("=" * 70)
    print("📊 ANALYSE DES DATASETS HISTORIQUES - AlgoInvest&Trade")
    print("=" * 70)
    print("\nCe programme compare les algorithmes avec les choix de Sienna")
    print("=" * 70)

    # Demander quel algorithme utiliser
    print("\n🤖 Quel algorithme voulez-vous tester ?")
    print("  1. Glouton (rapide)")
    print("  2. Programmation Dynamique (optimal)")

    choix = input("\nVotre choix (1 ou 2) : ").strip()

    if choix == "2":
        algo = "dynamique"
    else:
        algo = "glouton"

    print(f"\n✓ Algorithme sélectionné : {algo.upper()}")

    # Analyse Dataset 1
    analyser_dataset(
        "data/dataset1_PythonP7.csv", "Dataset 1", obtenir_choix_sienna_dataset1(), algo
    )

    # Analyse Dataset 2
    analyser_dataset(
        "data/dataset2_PythonP7.csv", "Dataset 2", obtenir_choix_sienna_dataset2(), algo
    )

    # Conclusion
    print(f"\n{'='*70}")
    print("✅ ANALYSE COMPLÈTE TERMINÉE")
    print(f"{'='*70}")
    print("\n💡 Rapport d'exploration des données généré avec succès !")
    print("📊 Les résultats peuvent être utilisés pour la présentation.")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
