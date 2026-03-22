# 🚀 MiniLang Compiler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

> Un compilateur éducatif avec double backend C/LLVM et détection d'overflow à la compilation

## ✨ Pourquoi MiniLang ?

MiniLang a commencé comme un projet de cours sur la construction de compilateurs, mais a évolué vers quelque chose de plus ambitieux :

- 🔥 **Double Backend** - Génère du code C (via GCC) ET du LLVM IR
- 🛡️ **Détection d'overflow à la compilation** - Attrape les débordements d'entiers AVANT l'exécution (comme Rust)
- 🎯 **Messages d'erreur intelligents** - Suggestions de correction basées sur des heuristiques
- 📚 **Architecture claire** - Design extensible, code de qualité production
- ⚡ **Performances natives** - Compilation directe en code machine, pas d'interpréteur

## 🚀 Démarrage rapide

### Installation

```bash
git clone https://github.com/myBestProjectAwsome/MINILANG.git
cd MINILANG
pip install ply
```

### Votre premier programme

```rust
# hello.ml
let x = 42
let y = 84
print(x)
print(y)
```

```bash
python src/compiler.py examples/hello.ml -o hello
./hello
```

**Sortie :**
```
42
84
```

## 📖 Fonctionnalités du langage

### Variables & Arithmétique

```rust
let x = 10 + 5
let y = x * 2
let z = y - 3
print(z)  # 27
```

### Structures de contrôle

```rust
let x = 42

if x > 10 {
    print(1)
} else {
    print(0)
}
```

### Boucles

```rust
let sum = 0
let i = 1

while i <= 10 {
    sum = sum + i
    i = i + 1
}

print(sum)  # 55
```

### Toutes les fonctionnalités

- ✅ Variables avec `let`
- ✅ Assignation mutable (`x = x + 1`)
- ✅ Opérateurs arithmétiques : `+`, `-`, `*`, `/`
- ✅ Opérateurs de comparaison : `==`, `!=`, `<`, `<=`, `>`, `>=`
- ✅ Conditions : `if` / `else`
- ✅ Boucles : `while`
- ✅ Affichage : `print()`
- ✅ Commentaires : `#`

## 🔥 Fonctionnalités uniques

### 1. Détection d'overflow à la compilation

La plupart des langages détectent l'overflow seulement à l'exécution (ou pas du tout). MiniLang l'attrape pendant la compilation :

```bash
$ cat overflow.ml
let x = 2000000000
let y = 2000000000 + 2000000000

$ python src/compiler.py overflow.ml
```

**Sortie :**
```
❌ Overflow détecté : 2000000000 + 2000000000 = 4000000000
   (dépasse les limites int32 : max 2147483647)
❌ Compilation annulée
```

### 2. Messages d'erreur intelligents

```bash
$ cat typo.ml
let value = 42
print(valu)  # Typo !

$ python src/compiler.py typo.ml
```

**Sortie :**
```
❌ Variable 'valu' non déclarée
  → Vouliez-vous dire 'value' ?
```

### 3. Double Backend

**Backend C :**
```bash
python src/compiler.py hello.ml -o hello
# Génère hello.c, compile avec GCC
```

**Backend LLVM :**
```bash
python src/compiler_llvm.py hello.ml -o hello
# Génère du LLVM IR, optimise avec LLVM
```

## 🏗️ Architecture

```
┌─────────────────┐
│  Code Source    │  Fichier .ml
│   (MiniLang)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Lexer       │  Tokenisation
│  (PLY/Lex)      │  → Mots-clés, opérateurs, littéraux
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Parser      │  Analyse syntaxique
│  (PLY/Yacc)     │  → Arbre syntaxique abstrait (AST)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Analyseur     │  Validation
│   Sémantique    │  → Vérification de types
│                 │  → Détection d'overflow
│                 │  → Suivi des variables
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Générateur de  │
│      Code       │
│                 │
│  ┌───────────┐  │
│  │Backend C  │──┼──→ Fichier .c → GCC → Binaire
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │Backend    │──┼──→ LLVM IR → llc → Binaire
│  │LLVM       │  │
│  └───────────┘  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Binaire Natif   │
│   (x86-64)      │
└─────────────────┘
```

### Composants clés

| Composant | Technologie | Responsabilité |
|-----------|-----------|----------------|
| **Lexer** | Python PLY | Tokenise le code source |
| **Parser** | Parser LALR | Construit l'AST depuis les tokens |
| **Analyseur Sémantique** | Custom | Vérification de types, détection d'overflow |
| **Backend C** | CodeGen → GCC | Génère du C, compile avec GCC |
| **Backend LLVM** | llvmlite | Génère du LLVM IR, optimise |

## 📚 Exemples

### Exemple 1 : Somme des nombres de 1 à 10

```rust
# examples/loops.ml
let i = 0

while i < 5 {
    print(i)
    i = i + 1
}

let sum = 0
let j = 1

while j <= 10 {
    sum = sum + j
    j = j + 1
}

print(sum)
```

**Sortie :**
```
0
1
2
3
4
55
```

### Exemple 2 : Logique conditionnelle

```rust
# examples/conditions.ml
let x = 42

if x > 10 {
    print(1)
} else {
    print(0)
}

let y = 5

if y > 10 {
    print(100)
} else {
    print(200)
}
```

**Sortie :**
```
1
200
```

### Exemple 3 : Détection d'erreur

```rust
# examples/error_undeclared.ml
let x = 42
print(y)  # Erreur : y n'existe pas
```

**Compilation :**
```bash
$ python src/compiler.py examples/error_undeclared.ml

🔴 ERREURS DÉTECTÉES :
  ❌ Variable 'y' non déclarée

❌ Compilation annulée (corrigez les erreurs ci-dessus)
```

## 🛣️ Roadmap

### Terminé ✅

- [x] Analyse lexicale (Lexer)
- [x] Analyse syntaxique (Parser)
- [x] Génération d'AST
- [x] Analyse sémantique
- [x] Vérification des déclarations de variables
- [x] Détection d'overflow
- [x] Génération de code C
- [x] Génération de LLVM IR
- [x] Intégration GCC
- [x] Récupération d'erreurs

### En cours 🚧

- [ ] Définitions et appels de fonctions
- [ ] Support des nombres flottants
- [ ] Type booléen (`true`/`false`)

### Planifié 📋

- [ ] Tableaux et indexation
- [ ] Type string et opérations
- [ ] Boucles for (sucre syntaxique sur while)
- [ ] Opérateurs logiques (`&&`, `||`, `!`)
- [ ] Instructions Break/Continue
- [ ] Système de modules
- [ ] Bibliothèque standard
- [ ] Auto-hébergement (compilateur écrit en MiniLang)
- [ ] REPL (mode interactif)
- [ ] Intégration debugger

## 🧪 Tests

```bash
# Exécuter tous les exemples
python src/compiler.py examples/hello.ml -o test_hello && ./test_hello
python src/compiler.py examples/loops.ml -o test_loops && ./test_loops
python src/compiler.py examples/conditions.ml -o test_conditions && ./test_conditions

# Tester la détection d'erreurs
python src/compiler.py examples/error_undeclared.ml  # Doit échouer gracieusement
```

## 🔧 Développement

### Structure du projet

```
MINILANG/
├── src/
│   ├── lexer.py          # Tokenisation
│   ├── parser.py         # Génération d'AST
│   ├── semantic.py       # Analyse sémantique
│   ├── codegen.py        # Générateur de code C
│   ├── llvm_backend.py   # Générateur LLVM IR
│   ├── compiler.py       # Compilateur C principal
│   └── compiler_llvm.py  # Compilateur LLVM principal
├── examples/
│   ├── hello.ml
│   ├── loops.ml
│   ├── conditions.ml
│   ├── arithmetic.ml
│   ├── test_valid.ml
│   └── error_undeclared.ml
├── README.md
├── LICENSE
└── requirements.txt
```

### Dépendances

```bash
pip install -r requirements.txt
```

**requirements.txt :**
```
ply==3.11
llvmlite>=0.40.0  # Pour le backend LLVM
```

## 💻 Utilisation avancée

### Mode verbeux

```bash
python src/compiler.py examples/hello.ml -o hello -v
```

**Affiche :**
```
📖 Lecture du fichier : examples/hello.ml
✓ 132 caractères lus

🔤 Analyse lexicale (Lexer)...
✓ 16 tokens générés

🌳 Analyse syntaxique (Parser)...
✓ AST généré avec 4 instructions

🔍 Analyse sémantique (vérification de sécurité)...
✓ Aucune erreur sémantique détectée

⚙️  Génération de code C...
✓ Code C généré (146 caractères)

💾 Code C sauvegardé : examples/hello.c

🔨 Compilation avec GCC...
✓ Exécutable créé : hello

✅ Compilation réussie !
   Exécutable : hello
   Exécutez avec : ./hello
```

### Voir le code C généré

```bash
python src/compiler.py examples/hello.ml -o hello
cat examples/hello.c
```

**Code généré :**
```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int x = 42;
    int y = 84;
    printf("%d\n", x);
    printf("%d\n", y);
    return 0;
}
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Que vous souhaitiez :

- 🐛 Signaler des bugs
- 💡 Suggérer des fonctionnalités
- 📖 Améliorer la documentation
- 🔧 Soumettre des PRs

### Bonnes premières issues

- [ ] Ajouter le support des boucles `for` (désucrées en `while`)
- [ ] Implémenter le type booléen (`true`, `false`)
- [ ] Ajouter plus de vérifications sémantiques (division par zéro)
- [ ] Améliorer les messages d'erreur
- [ ] Écrire plus de cas de test

## 📄 Licence

Licence MIT - voir le fichier [LICENSE](LICENSE) pour les détails.

## 🙏 Remerciements

Ce projet a été inspiré par :

- **The Dragon Book** - Compilers: Principles, Techniques, and Tools (Aho, Lam, Sethi, Ullman)
- **Le projet LLVM** - Infrastructure de compilation moderne
- **Rust** - Design de langage orienté sécurité
- **Python PLY** - Générateur de parser puissant

Remerciements spéciaux au cours de construction de compilateurs de l'EPITA pour les fondations.

## 📫 Contact

- **GitHub Issues** : [Créer une issue](https://github.com/myBestProjectAwsome/MINILANG/issues)
- **Pull Requests** : [Contribuer](https://github.com/myBestProjectAwsome/MINILANG/pulls)

---

**Construit avec ❤️ comme un voyage d'apprentissage dans la construction de compilateurs**

*Si vous trouvez ce projet utile, n'hésitez pas à lui donner une ⭐ sur GitHub !*
