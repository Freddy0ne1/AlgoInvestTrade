# 📊 AlgoInvest&Trade

**Projet d'optimisation d'investissement en actions**

Ce projet aide à choisir les meilleures actions à acheter avec un budget de 500€ pour maximiser le bénéfice après 2 ans.

---

## 🎯 C'est quoi ce projet ?

Imaginez que vous avez **500€** à investir et **20 actions** disponibles.

**Question :** Comment choisir les meilleures actions pour gagner le plus d'argent ?

**Réponse :** Utiliser des algorithmes intelligents ! 🤖

---

## 📁 Les Fichiers du Projet

```
AlgoInvest&Trade/
│
├── data/                          ← Dossier des données
│   ├── actions.csv                   (20 actions)
│   ├── dataset1_PythonP7.csv         (1001 actions)
│   └── dataset2_PythonP7.csv         (1000 actions)
│
├── bruteforce.py                  ← Programme 1 : Force Brute
├── optimized.py                   ← Programme 2 : Glouton
├── sac_a_dos_dynamique.py         ← Programme 3 : Dynamique
├── analyse_datasets.py            ← Programme 4 : Comparaison
│
└── README.md                      ← Ce fichier
```

---

## 🤖 Les 3 Algorithmes Expliqués Simplement

### **1. Force Brute** 🐌 (bruteforce.py)

**Comment ça marche ?**

- Teste TOUTES les combinaisons possibles
- Garde la meilleure

**Exemple :**

```
4 actions → teste 15 combinaisons
20 actions → teste 1 048 576 combinaisons !
```

**Avantage :** Trouve LA meilleure solution  
**Problème :** Très lent avec beaucoup d'actions

---

### **2. Glouton** ⚡ (optimized.py)

**Comment ça marche ?**

1. Calculer pour chaque action : **combien elle rapporte par euro investi**
2. Trier les actions (meilleure en premier)
3. Prendre les meilleures tant qu'il reste du budget

**Analogie :**

```
C'est comme au buffet :
- Vous calculez le "plaisir par euro" de chaque plat
- Vous prenez les plats les plus rentables en premier
```

**Avantage :** TRÈS rapide (< 0.001 seconde)  
**Problème :** Ne trouve pas toujours LA meilleure solution

---

### **3. Programmation Dynamique** 🎯 (sac_a_dos_dynamique.py)

**Comment ça marche ?**

- Construit un grand tableau
- Pour chaque action, décide : "La prendre ou pas ?"
- Garde toujours le meilleur choix

**Analogie :**

```
C'est comme remplir un sac à dos de randonnée :
- Chaque objet a un poids (= coût) et une valeur (= bénéfice)
- Vous devez remplir le sac pour maximiser la valeur
```

**Avantage :** Trouve LA meilleure solution ET reste rapide  
**Problème :** Plus complexe à comprendre

---

## 🚀 Comment Utiliser les Programmes

### **Étape 1 : Vérifier que Python est installé**

```bash
python --version
```

Si vous voyez `Python 3.x.x`, c'est bon ! ✅

---

### **Étape 2 : Organiser les fichiers**

Créez cette structure :

```
AlgoInvest&Trade/
├── bruteforce.py
├── optimized.py
├── sac_a_dos_dynamique.py
├── analyse_datasets.py
└── data/
    ├── actions.csv
    ├── dataset1_PythonP7.csv
    └── dataset2_PythonP7.csv
```

---

### **Étape 3 : Lancer un programme**

**Pour tester le glouton (rapide) :**

```bash
python optimized.py
```

**Pour tester la programmation dynamique (optimal) :**

```bash
python sac_a_dos_dynamique.py
```

**Pour tester la force brute (attention, lent !) :**

```bash
python bruteforce.py
```

**Pour comparer avec Sienna :**

```bash
python analyse_datasets.py
```

---

## 📊 Résultats Attendus

### **Exemple avec optimized.py**

```
🚀 Démarrage de l'algorithme d'optimisation (Version Glouton)
============================================================

📂 Lecture du fichier 'data/actions.csv'...
✓ 20 actions valides chargées

📊 STATISTIQUES DU DATASET
------------------------------------------------------------
Nombre total d'actions : 20
Coût : Min=10.24€ | Max=45.78€ | Moy=28.50€
Bénéfice : Min=5.2% | Max=35.8% | Moy=18.6%
------------------------------------------------------------

🔍 Recherche de la meilleure combinaison...

============================================================
🎯 MEILLEURE COMBINAISON (Algorithme Glouton)
============================================================

⏱️  Temps d'exécution : 0.000234 secondes
💰 Coût total : 498.00 €
📈 Bénéfice total après 2 ans : 197.60 €
📊 Rentabilité : 39.68%

📋 Actions à acheter (8 actions) :
------------------------------------------------------------
Action          Coût    Bénéfice %   Bénéfice €      Ratio
------------------------------------------------------------
Action-5      45.00€        35.8%       16.11€     0.7956
Action-2      68.50€        28.2%       19.32€     0.4117
...
============================================================

✅ Optimisation terminée avec succès !
⚡ Excellent ! Le programme a répondu en 0.000234s (< 1 seconde)
```

---

## 📈 Comparaison des 3 Algorithmes

| Critère                    | Force Brute | Glouton          | Dynamique   |
| -------------------------- | ----------- | ---------------- | ----------- |
| **Vitesse (20 actions)**   | ~5 secondes | 0.0003 sec       | 0.0024 sec  |
| **Vitesse (1000 actions)** | IMPOSSIBLE  | 0.002 sec        | 0.02 sec    |
| **Solution**               | Optimale ✅ | Approximative ⚠️ | Optimale ✅ |
| **Facile à comprendre**    | ✅✅✅      | ✅✅             | ⚠️          |

---

## 🎓 Pour les Débutants : Quel Programme Utiliser ?

### **Vous débutez en programmation ?**

→ Utilisez `optimized.py` (Glouton)

- Très rapide
- Facile à comprendre
- Résultats très bons

### **Vous voulez la solution parfaite ?**

→ Utilisez `sac_a_dos_dynamique.py` (Dynamique)

- Garantit la meilleure solution
- Encore très rapide
- Un peu plus complexe

### **Vous voulez comprendre comment ça marche ?**

→ Regardez `bruteforce.py` (Force Brute)

- Très simple à comprendre
- Teste toutes les possibilités
- Attention : lent !

---

## 📝 Format des Fichiers CSV

### **Format 1 : actions.csv**

```csv
Actions #,Coût par action (en euros),Bénéfice (après 2 ans)
Action-1,20,5%
Action-2,30,10%
Action-3,50,15%
```

### **Format 2 : dataset1 et dataset2**

```csv
name,price,profit
Share-DUPH,10.01,12.25
Share-GTAN,26.04,38.06
Share-USUF,9.25,27.69
```

---

## 🔧 Problèmes Courants

### **Erreur : "File not found"**

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/actions.csv'
```

**Solution :**

1. Vérifiez que le dossier `data/` existe
2. Vérifiez que le fichier CSV est bien dans `data/`
3. Vérifiez l'orthographe du nom du fichier

---

### **Erreur : "python not found"**

**Solution :**

1. Installez Python depuis python.org
2. Ou utilisez `python3` au lieu de `python` :
   ```bash
   python3 optimized.py
   ```

---

### **Le programme est trop lent**

**Si vous utilisez bruteforce.py :**

- C'est normal avec plus de 20 actions
- Utilisez `optimized.py` ou `sac_a_dos_dynamique.py` à la place

---

## 💡 Comprendre les Résultats

### **Coût total**

```
💰 Coût total : 498.00 €
```

→ Combien d'argent vous investissez (max 500€)

### **Bénéfice total**

```
📈 Bénéfice total : 197.60 €
```

→ Combien d'argent vous gagnez après 2 ans

### **Rentabilité**

```
📊 Rentabilité : 39.68%
```

→ Pourcentage de gain sur votre investissement
→ Calcul : (197.60 / 498.00) × 100 = 39.68%

---

## 🎯 Exemple Concret

### **Situation**

Vous avez **100€** et 3 actions :

| Action | Coût | Bénéfice % | Bénéfice € |
| ------ | ---- | ---------- | ---------- |
| A      | 40€  | 20%        | 8€         |
| B      | 50€  | 15%        | 7.50€      |
| C      | 30€  | 10%        | 3€         |

### **Algorithme Glouton**

1. Calculer les ratios :

   - A : 20/40 = **0.50** (meilleur)
   - B : 15/50 = **0.30**
   - C : 10/30 = **0.33**

2. Trier : A → C → B

3. Sélectionner :
   - Prendre A (40€) → Reste 60€
   - Prendre C (30€) → Reste 30€
   - B impossible (50€ > 30€)

**Résultat :**

- Coût : 70€
- Bénéfice : 11€
- Actions : A + C

---

## 📚 Pour Aller Plus Loin

### **Vous voulez apprendre plus ?**

1. **Lisez les commentaires dans le code**

   - Chaque ligne est expliquée
   - Les fonctions ont des docstrings

2. **Modifiez le code**

   - Changez le budget (ligne `budget_max=500`)
   - Ajoutez des `print()` pour voir ce qui se passe

3. **Testez avec vos propres données**
   - Créez votre fichier CSV
   - Lancez le programme

### **Ressource utile**

- [Problème du Sac à Dos expliqué](https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_sac_%C3%A0_dos)

---

### **1. Quel algorithme est le meilleur ?**

Ça dépend de vos besoins :

- **Rapidité ?** → Glouton
- **Précision ?** → Dynamique
- **Apprentissage ?** → Force Brute

### **2. Pourquoi trois algorithmes différents ?**

Pour comprendre les compromis entre **vitesse** et **précision** :

- Force Brute : Précis mais lent
- Glouton : Rapide mais approximatif
- Dynamique : Précis ET rapide (le meilleur !)
