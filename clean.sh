#!/bin/bash
# Script de nettoyage du repo MiniLang

echo "🧹 Nettoyage du repo MiniLang..."

# Supprimer les fichiers Python compilés
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Supprimer les fichiers de parsing
rm -f src/parser.out src/parsetab.py

# Supprimer les exécutables de test
rm -f hello arithmetic conditions loops test_valid
rm -f loops_llvm loops_c hello_llvm

# Supprimer les fichiers C générés
rm -f examples/*.c examples/*.ll

echo "✅ Nettoyage terminé !"
echo ""
echo "Fichiers restants :"
ls -la
