import ply.yacc as yacc
from lexer import Lexer


# ============= Définitions AST (Arbre de Syntaxe Abstraite) =============

class ASTNode:
    """Classe de base pour tous les nœuds AST"""
    pass


class Program(ASTNode):
    """Programme complet = liste d'instructions"""
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"Program({len(self.statements)} instructions)"


class LetStatement(ASTNode):
    """Déclaration de variable : let x = 42"""
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"Let({self.name} = {self.value})"


class PrintStatement(ASTNode):
    """Instruction print : print(x)"""
    def __init__(self, expression):
        self.expression = expression
    
    def __repr__(self):
        return f"Print({self.expression})"


class IntegerLiteral(ASTNode):
    """Littéral entier : 42"""
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Int({self.value})"


class Variable(ASTNode):
    """Variable : x, y, counter"""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Var({self.name})"


# ============= Parser =============

class Parser:
    """Parser MiniLang - Phase 1"""
    
    # Récupérer les tokens du lexer
    tokens = Lexer.tokens
    
    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)
    
    # Règle principale : un programme = liste d'instructions
    def p_program(self, p):
        """program : statement_list"""
        p[0] = Program(p[1])
    
    # Liste d'instructions (une ou plusieurs)
    def p_statement_list(self, p):
        """statement_list : statement_list statement
                         | statement"""
        if len(p) == 3:
            # Plusieurs instructions : on ajoute à la liste
            p[0] = p[1] + [p[2]]
        else:
            # Une seule instruction : on crée une liste
            p[0] = [p[1]]
    
    # Instruction : let x = 42
    def p_statement_let(self, p):
        """statement : LET IDENTIFIER ASSIGN expression"""
        p[0] = LetStatement(p[2], p[4])
    
    # Instruction : print(x)
    def p_statement_print(self, p):
        """statement : PRINT LPAREN expression RPAREN"""
        p[0] = PrintStatement(p[3])
    
    # Expression : un nombre entier
    def p_expression_integer(self, p):
        """expression : INTEGER"""
        p[0] = IntegerLiteral(p[1])
    
    # Expression : une variable
    def p_expression_variable(self, p):
        """expression : IDENTIFIER"""
        p[0] = Variable(p[1])
    
    # Gestion des erreurs de syntaxe
    def p_error(self, p):
        if p:
            print(f"❌ Erreur de syntaxe à la ligne {p.lineno}, token '{p.value}'")
        else:
            print("❌ Erreur de syntaxe : fin de fichier inattendue")
    
    def parse(self, code):
        """Parse le code source et retourne l'AST"""
        return self.parser.parse(code, lexer=self.lexer.lexer)


# Test du parser
if __name__ == "__main__":
    parser = Parser()
    
    test_code = """
let x = 42
let y = 84
print(x)
print(y)
"""
    
    print("=== Test du Parser - Phase 1 ===\n")
    print("Code source :")
    print(test_code)
    
    print("\n🌳 Parsing...")
    ast = parser.parse(test_code)
    
    if ast:
        print(f"\n✅ AST généré : {ast}")
        print("\nDétail des instructions :")
        for i, stmt in enumerate(ast.statements, 1):
            print(f"  {i}. {stmt}")
    else:
        print("\n❌ Échec du parsing")
