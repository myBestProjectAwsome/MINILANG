"""
MiniLang Semantic Analyzer - Phase 6
Vérifie la cohérence du programme AVANT compilation
Détecte : variables non déclarées, overflow, erreurs de logique
"""

from parser import (
    Program, LetStatement, AssignStatement, PrintStatement,
    IfStatement, WhileStatement,
    IntegerLiteral, Variable, BinaryOp
)


class SemanticError:
    """Représente une erreur sémantique"""
    def __init__(self, message, line=None):
        self.message = message
        self.line = line
    
    def __str__(self):
        if self.line:
            return f"❌ Ligne {self.line} : {self.message}"
        return f"❌ {self.message}"


class SemanticAnalyzer:
    """Analyseur sémantique pour MiniLang"""
    
    def __init__(self):
        self.symbol_table = {}  # {nom_variable: info}
        self.errors = []
        self.warnings = []
    
    def analyze(self, ast):
        """
        Analyse l'AST et retourne les erreurs trouvées
        
        Returns:
            (errors, warnings) : listes d'erreurs et avertissements
        """
        if not isinstance(ast, Program):
            raise ValueError("L'AST doit être un Programme")
        
        # Analyser chaque instruction
        for statement in ast.statements:
            self.analyze_statement(statement)
        
        return self.errors, self.warnings
    
    def analyze_statement(self, stmt):
        """Analyse une instruction"""
        if isinstance(stmt, LetStatement):
            self.analyze_let(stmt)
        elif isinstance(stmt, AssignStatement):
            self.analyze_assign(stmt)
        elif isinstance(stmt, PrintStatement):
            self.analyze_print(stmt)
        elif isinstance(stmt, IfStatement):
            self.analyze_if(stmt)
        elif isinstance(stmt, WhileStatement):
            self.analyze_while(stmt)
    
    def analyze_let(self, stmt):
        """Analyse : let x = expression"""
        # Vérifier l'expression
        self.check_expression(stmt.value)
        
        # Vérifier si variable déjà déclarée (warning)
        if stmt.name in self.symbol_table:
            self.warnings.append(
                f"⚠️  Variable '{stmt.name}' redéclarée (précédente déclaration écrasée)"
            )
        
        # Enregistrer la variable
        self.symbol_table[stmt.name] = {
            'type': 'int',
            'declared': True,
            'used': False
        }
    
    def analyze_assign(self, stmt):
        """Analyse : x = expression"""
        # Vérifier que la variable existe
        if stmt.name not in self.symbol_table:
            self.errors.append(
                SemanticError(
                    f"Variable '{stmt.name}' non déclarée. "
                    f"Utilisez 'let {stmt.name} = ...' pour la déclarer."
                )
            )
            # Suggérer une correction si nom similaire existe
            suggestion = self.suggest_variable(stmt.name)
            if suggestion:
                self.errors.append(
                    SemanticError(f"  → Vouliez-vous dire '{suggestion}' ?")
                )
        else:
            # Marquer comme utilisée
            self.symbol_table[stmt.name]['used'] = True
        
        # Vérifier l'expression
        self.check_expression(stmt.value)
    
    def analyze_print(self, stmt):
        """Analyse : print(expression)"""
        self.check_expression(stmt.expression)
    
    def analyze_if(self, stmt):
        """Analyse : if ... else"""
        # Vérifier la condition
        self.check_expression(stmt.condition)
        
        # Vérifier le bloc then
        for then_stmt in stmt.then_block:
            self.analyze_statement(then_stmt)
        
        # Vérifier le bloc else (si existe)
        if stmt.else_block:
            for else_stmt in stmt.else_block:
                self.analyze_statement(else_stmt)
    
    def analyze_while(self, stmt):
        """Analyse : while"""
        # Vérifier la condition
        self.check_expression(stmt.condition)
        
        # Vérifier le corps de la boucle
        for body_stmt in stmt.body:
            self.analyze_statement(body_stmt)
    
    def check_expression(self, expr):
        """Vérifie une expression et retourne son type"""
        if isinstance(expr, IntegerLiteral):
            # Vérifier overflow
            if expr.value > 2147483647 or expr.value < -2147483648:
                self.errors.append(
                    SemanticError(
                        f"Overflow : La valeur {expr.value} dépasse les limites "
                        f"d'un entier 32-bit (max: 2147483647)"
                    )
                )
            return 'int'
        
        elif isinstance(expr, Variable):
            # Vérifier que la variable existe
            if expr.name not in self.symbol_table:
                self.errors.append(
                    SemanticError(f"Variable '{expr.name}' non déclarée")
                )
                # Suggérer correction
                suggestion = self.suggest_variable(expr.name)
                if suggestion:
                    self.errors.append(
                        SemanticError(f"  → Vouliez-vous dire '{suggestion}' ?")
                    )
            else:
                # Marquer comme utilisée
                self.symbol_table[expr.name]['used'] = True
            return 'int'
        
        elif isinstance(expr, BinaryOp):
            # Vérifier les deux côtés
            left_type = self.check_expression(expr.left)
            right_type = self.check_expression(expr.right)
            
            # Détection d'overflow potentiel
            if expr.operator in ['+', '-', '*']:
                self.check_overflow_binop(expr)
            
            return 'int'
        
        return 'unknown'
    
    def check_overflow_binop(self, expr):
        """Détecte les overflow potentiels dans les opérations"""
        # Si les deux opérandes sont des littéraux, on peut vérifier
        if isinstance(expr.left, IntegerLiteral) and isinstance(expr.right, IntegerLiteral):
            left_val = expr.left.value
            right_val = expr.right.value
            
            try:
                if expr.operator == '+':
                    result = left_val + right_val
                elif expr.operator == '-':
                    result = left_val - right_val
                elif expr.operator == '*':
                    result = left_val * right_val
                else:
                    return
                
                # Vérifier overflow
                if result > 2147483647 or result < -2147483648:
                    self.errors.append(
                        SemanticError(
                            f"Overflow détecté : {left_val} {expr.operator} {right_val} = {result} "
                            f"(dépasse les limites int32)"
                        )
                    )
            except:
                pass
    
    def suggest_variable(self, name):
        """Suggère une variable similaire (distance de Levenshtein simple)"""
        if not self.symbol_table:
            return None
        
        # Chercher une variable avec un nom proche
        for var_name in self.symbol_table.keys():
            # Simple heuristique : première lettre identique et longueur similaire
            if var_name[0] == name[0] and abs(len(var_name) - len(name)) <= 2:
                return var_name
        
        return None
    
    def check_unused_variables(self):
        """Vérifie les variables déclarées mais jamais utilisées"""
        for var_name, info in self.symbol_table.items():
            if not info['used']:
                self.warnings.append(
                    f"⚠️  Variable '{var_name}' déclarée mais jamais utilisée"
                )


# Test de l'analyseur
if __name__ == "__main__":
    from parser import Parser
    
    # Test 1 : Variable non déclarée
    test_code_1 = """
let x = 42
print(y)
"""
    
    print("=== Test 1 : Variable non déclarée ===\n")
    print("Code :")
    print(test_code_1)
    
    parser = Parser()
    ast = parser.parse(test_code_1)
    
    if ast:
        analyzer = SemanticAnalyzer()
        errors, warnings = analyzer.analyze(ast)
        
        if errors:
            print("\n🔴 ERREURS :")
            for error in errors:
                print(f"  {error}")
        
        if warnings:
            print("\n🟡 AVERTISSEMENTS :")
            for warning in warnings:
                print(f"  {warning}")
        
        if not errors and not warnings:
            print("\n✅ Aucune erreur !")
    
    print("\n" + "="*60 + "\n")
    
    # Test 2 : Overflow
    test_code_2 = """
let x = 2000000000
let y = 2000000000 + 2000000000
"""
    
    print("=== Test 2 : Overflow ===\n")
    print("Code :")
    print(test_code_2)
    
    ast = parser.parse(test_code_2)
    
    if ast:
        analyzer = SemanticAnalyzer()
        errors, warnings = analyzer.analyze(ast)
        
        if errors:
            print("\n🔴 ERREURS :")
            for error in errors:
                print(f"  {error}")
        
        if warnings:
            print("\n🟡 AVERTISSEMENTS :")
            for warning in warnings:
                print(f"  {warning}")
        
        if not errors and not warnings:
            print("\n✅ Aucune erreur !")
