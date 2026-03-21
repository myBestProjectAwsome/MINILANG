from parser import (
    Program, LetStatement, PrintStatement,
    IntegerLiteral, Variable
)


class CodeGenerator:
    """Générateur de code C pour MiniLang"""
    
    def __init__(self):
        self.variables = {}  # Dictionnaire des variables déclarées
        self.indent_level = 0
    
    def indent(self):
        """Retourne l'indentation courante (4 espaces par niveau)"""
        return "    " * self.indent_level
    
    def generate(self, ast):
        """Génère le code C complet à partir de l'AST"""
        if not isinstance(ast, Program):
            raise ValueError("L'AST doit être un Programme")
        
        code = []
        
        # En-tête C (includes)
        code.append("#include <stdio.h>")
        code.append("#include <stdlib.h>")
        code.append("")
        
        # Fonction main
        code.append("int main() {")
        self.indent_level += 1
        
        # Générer chaque instruction du programme
        for statement in ast.statements:
            stmt_code = self.generate_statement(statement)
            code.append(stmt_code)
        
        # Fin de la fonction main
        code.append(self.indent() + "return 0;")
        self.indent_level -= 1
        code.append("}")
        
        return "\n".join(code)
    
    def generate_statement(self, stmt):
        """Génère le code C pour une instruction"""
        if isinstance(stmt, LetStatement):
            return self.generate_let(stmt)
        elif isinstance(stmt, PrintStatement):
            return self.generate_print(stmt)
        else:
            raise ValueError(f"Type d'instruction inconnu : {type(stmt)}")
    
    def generate_let(self, stmt):
        """Génère le code pour : let x = 42"""
        # Générer le code pour la valeur
        value_code = self.generate_expression(stmt.value)
        
        # Enregistrer la variable comme étant de type int
        self.variables[stmt.name] = "int"
        
        # Retourner la déclaration C
        return f"{self.indent()}int {stmt.name} = {value_code};"
    
    def generate_print(self, stmt):
        """Génère le code pour : print(x)"""
        # Générer le code pour l'expression à afficher
        expr_code = self.generate_expression(stmt.expression)
        
        # Pour Phase 1, on suppose que tout est des entiers
        return f'{self.indent()}printf("%d\\n", {expr_code});'
    
    def generate_expression(self, expr):
        """Génère le code C pour une expression"""
        if isinstance(expr, IntegerLiteral):
            # Un nombre : on retourne juste sa valeur
            return str(expr.value)
        
        elif isinstance(expr, Variable):
            # Une variable : vérifier qu'elle est déclarée
            if expr.name not in self.variables:
                raise ValueError(f"Variable non déclarée : {expr.name}")
            return expr.name
        
        else:
            raise ValueError(f"Type d'expression inconnu : {type(expr)}")


# Test du générateur
if __name__ == "__main__":
    from parser import Parser
    
    parser = Parser()
    
    test_code = """
let x = 42
let y = 84
print(x)
print(y)
"""
    
    print("=== Test du Générateur de Code - Phase 1 ===\n")
    print("Code MiniLang :")
    print(test_code)
    
    # Parser le code
    print("🌳 Parsing...")
    ast = parser.parse(test_code)
    
    if not ast:
        print("❌ Erreur de parsing")
        exit(1)
    
    print(f"✅ AST : {ast}\n")
    
    # Générer le code C
    print("⚙️  Génération de code C...")
    codegen = CodeGenerator()
    
    try:
        c_code = codegen.generate(ast)
        print("✅ Code C généré !\n")
        
        print("=" * 50)
        print("CODE C GÉNÉRÉ :")
        print("=" * 50)
        print(c_code)
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
