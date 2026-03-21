
# 🚀 MiniLang Compiler
 
Un compilateur complet pour un langage de programmation simple et moderne.
 
## 📍 PHASE 1 : Hello World (EN COURS)
 
**Objectif** : Compiler et exécuter notre premier programme MiniLang
 
**Ce que notre compilateur fera** :
```rust
let x = 42
let y = 84
print(x)
print(y)
```
 
**Résultat attendu** :
```
42
84
```
 
## 🛠️ Installation
 
```bash
# Installer les dépendances
pip install ply
```
 
## 💻 Utilisation
 
```bash
# Compiler un programme
python src/compiler.py examples/hello.ml -o hello
 
# Exécuter
./hello
```
 
## 📚 Architecture
 
```
Source (.ml) → Lexer → Parser → Code Generator → C Code → GCC → Executable
```
 
## 📖 Étapes de développement
 
- [ ] Étape 1 : Lexer (analyse lexicale)
- [ ] Étape 2 : Parser (analyse syntaxique)
- [ ] Étape 3 : Code Generator (génération C)
- [ ] Étape 4 : Compiler (orchestration)
- [ ] Étape 5 : Test final
 
## 📄 Licence
 
MIT
