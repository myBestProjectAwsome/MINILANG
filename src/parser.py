"""
MiniLang Parser - Phase 4
Support : let, print, arithmétique, if/else, comparaisons
"""

import ply.yacc as yacc
from lexer import Lexer


# ============= Définitions AST =============

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


class IfStatement(ASTNode):
    """Instruction if : if condition { ... } else { ... }"""
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
    
    def __repr__(self):
        if self.else_block:
            return f"If({self.condition}) Then({len(self.then_block)}) Else({len(self.else_block)})"
        return f"If({self.condition}) Then({len(self.then_block)})"


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


class BinaryOp(ASTNode):
    """Opération binaire : x + y, a > b"""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"BinOp({self.left} {self.operator} {self.right})"


# ============= Parser =============

class Parser:
    """Parser MiniLang - Phase 4"""
    
    # Récupérer les tokens du lexer
    tokens = Lexer.tokens
    
    # Priorité des opérateurs
    precedence = (
        ('left', 'EQ', 'NE'),              # Comparaison égalité
        ('left', 'LT', 'LE', 'GT', 'GE'),  # Comparaison ordre
        ('left', 'PLUS', 'MINUS'),         # Addition/Soustraction
        ('left', 'MULTIPLY', 'DIVIDE'),    # Multiplication/Division
    )
    
    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)
    
    # Programme = liste d'instructions
    def p_program(self, p):
        """program : statement_list"""
        p[0] = Program(p[1])
    
    # Liste d'instructions
    def p_statement_list(self, p):
        """statement_list : statement_list statement
                         | statement"""
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]
    
    # Instruction : let
    def p_statement_let(self, p):
        """statement : LET IDENTIFIER ASSIGN expression"""
        p[0] = LetStatement(p[2], p[4])
    
    # Instruction : print
    def p_statement_print(self, p):
        """statement : PRINT LPAREN expression RPAREN"""
        p[0] = PrintStatement(p[3])
    
    # Instruction : if ... else (NOUVEAU Phase 4)
    def p_statement_if(self, p):
        """statement : IF expression LBRACE statement_list RBRACE
                     | IF expression LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE"""
        if len(p) == 6:
            # if sans else
            p[0] = IfStatement(p[2], p[4], None)
        else:
            # if avec else
            p[0] = IfStatement(p[2], p[4], p[8])
    
    # Expression : comparaison (NOUVEAU Phase 4)
    def p_expression_comparison(self, p):
        """expression : expression EQ expression
                      | expression NE expression
                      | expression LT expression
                      | expression LE expression
                      | expression GT expression
                      | expression GE expression"""
        p[0] = BinaryOp(p[1], p[2], p[3])
    
    # Expression : opération arithmétique
    def p_expression_binop(self, p):
        """expression : expression PLUS expression
                      | expression MINUS expression
                      | expression MULTIPLY expression
                      | expression DIVIDE expression"""
        p[0] = BinaryOp(p[1], p[2], p[3])
    
    # Expression : entier
    def p_expression_integer(self, p):
        """expression : INTEGER"""
        p[0] = IntegerLiteral(p[1])
    
    # Expression : variable
    def p_expression_variable(self, p):
        """expression : IDENTIFIER"""
        p[0] = Variable(p[1])
    
    # Expression : parenthèses
    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = p[2]
    
    # Gestion des erreurs
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

if x > 10 {
    print(1)
} else {
    print(0)
}
"""
    
    print("=== Test du Parser - Phase 4 ===\n")
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
