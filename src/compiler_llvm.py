#!/usr/bin/env python3
"""
MiniLang Compiler - Phase 7 (Backend LLVM)
Pipeline : Lexer → Parser → Sémantique → LLVM → Exécutable
"""

import sys
import os
import subprocess
import argparse

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from llvm_backend import LLVMCodeGenerator


class LLVMCompiler:
    """Compilateur MiniLang avec backend LLVM"""
    
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.semantic_analyzer = SemanticAnalyzer()
        self.llvm_codegen = None  # Créé pour chaque compilation
    
    def compile(self, source_file, output_file=None, verbose=False, show_ir=False):
        """Compile un fichier .ml en exécutable via LLVM"""
        
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
        
        # 2. Lexer
        if verbose:
            print("🔤 Analyse lexicale (Lexer)...")
        
        tokens = self.lexer.tokenize(source_code)
        
        if verbose:
            print(f"✓ {len(tokens)} tokens générés\n")
        
        # 3. Parser
        if verbose:
            print("🌳 Analyse syntaxique (Parser)...")
        
        ast = self.parser.parse(source_code)
        
        if ast is None:
            print("❌ Erreur lors du parsing")
            return False
        
        if verbose:
            print(f"✓ AST généré avec {len(ast.statements)} instructions\n")
        
        # 4. Analyse sémantique
        if verbose:
            print("🔍 Analyse sémantique (sécurité)...")
        
        errors, warnings = self.semantic_analyzer.analyze(ast)
        
        if warnings:
            print("\n🟡 AVERTISSEMENTS :")
            for warning in warnings:
                print(f"  {warning}")
            print()
        
        if errors:
            print("\n🔴 ERREURS :")
            for error in errors:
                print(f"  {error}")
            print("\n❌ Compilation annulée\n")
            return False
        
        if verbose:
            print(f"✓ Aucune erreur détectée\n")
        
        # 5. Génération de code LLVM IR
        if verbose:
            print("⚡ Génération de code LLVM IR...")
        
        try:
            self.llvm_codegen = LLVMCodeGenerator()
            llvm_ir = self.llvm_codegen.generate(ast)
        except Exception as e:
            print(f"❌ Erreur lors de la génération LLVM : {e}")
            import traceback
            traceback.print_exc()
            return False
        
        if verbose:
            print(f"✓ LLVM IR généré ({len(llvm_ir)} caractères)\n")
        
        # Afficher le code LLVM IR si demandé
        if show_ir:
            print("=" * 60)
            print("CODE LLVM IR :")
            print("=" * 60)
            print(llvm_ir)
            print("=" * 60 + "\n")
        
        # 6. Sauvegarder le LLVM IR
        ir_file = source_file.replace('.ml', '.ll')
        
        try:
            with open(ir_file, 'w') as f:
                f.write(llvm_ir)
        except Exception as e:
            print(f"❌ Erreur lors de l'écriture du fichier IR : {e}")
            return False
        
        if verbose:
            print(f"💾 LLVM IR sauvegardé : {ir_file}\n")
        
        # 7. Compiler avec LLVM (llc + gcc)
        if output_file is None:
            output_file = source_file.replace('.ml', '')
        
        if verbose:
            print("🔨 Compilation avec LLVM...")
        
        # Option 1 : Compiler directement avec lli (interpréteur LLVM)
        # Option 2 : Compiler avec llc puis linker
        # Option 3 : Utiliser clang directement sur le .ll
        
        try:
            # Utiliser clang pour compiler le LLVM IR
            result = subprocess.run(
                ['clang', ir_file, '-o', output_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ Erreur clang :\n{result.stderr}")
                print("\n💡 Astuce : Installez clang avec 'sudo apt install clang'")
                return False
            
            if verbose:
                print(f"✓ Exécutable créé : {output_file}\n")
        
        except FileNotFoundError:
            print("❌ clang n'est pas installé.")
            print("   Installez-le avec : sudo apt install clang")
            return False
        
        # 8. Succès !
        print(f"✅ Compilation LLVM réussie !")
        print(f"   Backend : LLVM (optimisé)")
        print(f"   Exécutable : {output_file}")
        print(f"   Exécutez avec : ./{output_file}")
        
        return True


def main():
    """Point d'entrée du compilateur LLVM"""
    
    parser = argparse.ArgumentParser(
        description='MiniLang Compiler - Phase 7 (Backend LLVM)',
        epilog='Exemple : python compiler_llvm.py examples/hello.ml -o hello'
    )
    
    parser.add_argument(
        'source',
        help='Fichier source .ml à compiler'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Nom du fichier de sortie'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbeux'
    )
    
    parser.add_argument(
        '--show-ir',
        action='store_true',
        help='Afficher le code LLVM IR généré'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"❌ Fichier non trouvé : {args.source}")
        sys.exit(1)
    
    compiler = LLVMCompiler()
    success = compiler.compile(
        args.source,
        args.output,
        args.verbose,
        args.show_ir
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
