#!/usr/bin/env python3
"""
MiniLang Compiler - Phase 6
Pipeline : Lexer → Parser → Analyse Sémantique → CodeGen → GCC
"""

import sys
import os
import subprocess
import argparse

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator


class Compiler:
    """Compilateur MiniLang complet avec analyse sémantique"""
    
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.semantic_analyzer = SemanticAnalyzer()
        self.codegen = CodeGenerator()
    
    def compile(self, source_file, output_file=None, verbose=False):
        """Compile un fichier .ml en exécutable"""
        
        # 1. Lire le fichier source
        if verbose:
            print(f"📖 Lecture du fichier : {source_file}")
        
        try:
            with open(source_file, 'r') as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé : {source_file}")
            return False
        
        if verbose:
            print(f"✓ {len(source_code)} caractères lus\n")
        
        # 2. Lexer (analyse lexicale)
        if verbose:
            print("🔤 Analyse lexicale (Lexer)...")
        
        tokens = self.lexer.tokenize(source_code)
        
        if verbose:
            print(f"✓ {len(tokens)} tokens générés\n")
        
        # 3. Parser (analyse syntaxique)
        if verbose:
            print("🌳 Analyse syntaxique (Parser)...")
        
        ast = self.parser.parse(source_code)
        
        if ast is None:
            print("❌ Erreur lors du parsing")
            return False
        
        if verbose:
            print(f"✓ AST généré avec {len(ast.statements)} instructions\n")
        
        # 4. Analyse sémantique (NOUVEAU Phase 6 !)
        if verbose:
            print("🔍 Analyse sémantique (vérification de sécurité)...")
        
        errors, warnings = self.semantic_analyzer.analyze(ast)
        
        # Afficher les avertissements
        if warnings:
            print("\n🟡 AVERTISSEMENTS :")
            for warning in warnings:
                print(f"  {warning}")
            print()
        
        # Si erreurs, arrêter la compilation
        if errors:
            print("\n🔴 ERREURS DÉTECTÉES :")
            for error in errors:
                print(f"  {error}")
            print("\n❌ Compilation annulée (corrigez les erreurs ci-dessus)\n")
            return False
        
        if verbose:
            print(f"✓ Aucune erreur sémantique détectée\n")
        
        # 5. Génération de code C
        if verbose:
            print("⚙️  Génération de code C...")
        
        try:
            c_code = self.codegen.generate(ast)
        except Exception as e:
            print(f"❌ Erreur lors de la génération : {e}")
            return False
        
        if verbose:
            print(f"✓ Code C généré ({len(c_code)} caractères)\n")
        
        # 6. Sauvegarder le code C
        c_file = source_file.replace('.ml', '.c')
        
        try:
            with open(c_file, 'w') as f:
                f.write(c_code)
        except Exception as e:
            print(f"❌ Erreur lors de l'écriture du fichier C : {e}")
            return False
        
        if verbose:
            print(f"💾 Code C sauvegardé : {c_file}\n")
        
        # 7. Compiler avec GCC
        if output_file is None:
            output_file = source_file.replace('.ml', '')
        
        if verbose:
            print("🔨 Compilation avec GCC...")
        
        try:
            result = subprocess.run(
                ['gcc', c_file, '-o', output_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ Erreur GCC :\n{result.stderr}")
                return False
            
            if verbose:
                print(f"✓ Exécutable créé : {output_file}\n")
        
        except FileNotFoundError:
            print("❌ GCC n'est pas installé.")
            print("   Installez-le avec : sudo apt install gcc (Linux)")
            print("                    ou : brew install gcc (Mac)")
            return False
        
        # 8. Succès !
        print(f"✅ Compilation réussie !")
        print(f"   Exécutable : {output_file}")
        print(f"   Exécutez avec : ./{output_file}")
        
        return True


def main():
    """Point d'entrée du compilateur"""
    
    parser = argparse.ArgumentParser(
        description='MiniLang Compiler - Phase 6 (avec analyse sémantique)',
        epilog='Exemple : python compiler.py ../examples/hello.ml -o hello'
    )
    
    parser.add_argument(
        'source',
        help='Fichier source .ml à compiler'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Nom du fichier de sortie (par défaut : même nom sans .ml)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbeux (affiche les détails de compilation)'
    )
    
    args = parser.parse_args()
    
    # Vérifier que le fichier existe
    if not os.path.exists(args.source):
        print(f"❌ Fichier non trouvé : {args.source}")
        sys.exit(1)
    
    # Compiler
    compiler = Compiler()
    success = compiler.compile(args.source, args.output, args.verbose)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
