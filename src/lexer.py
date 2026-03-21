"""
MiniLang Lexer - Phase 5
Support : let, print, arithmétique, if/else, while
"""

import ply.lex as lex


class Lexer:
    """Analyseur lexical pour MiniLang"""
    
    # Liste des tokens
    tokens = (
        # Littéraux
        'INTEGER',
        'IDENTIFIER',
        
        # Mots-clés
        'LET',
        'PRINT',
        'IF',
        'ELSE',
        'WHILE',     # NOUVEAU Phase 5
        
        # Opérateurs arithmétiques
        'PLUS',
        'MINUS',
        'MULTIPLY',
        'DIVIDE',
        
        # Opérateurs de comparaison
        'EQ',
        'NE',
        'LT',
        'LE',
        'GT',
        'GE',
        
        # Opérateurs
        'ASSIGN',
        
        # Délimiteurs
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
    )
    
    # Mots-clés réservés
    reserved = {
        'let': 'LET',
        'print': 'PRINT',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',  # NOUVEAU Phase 5
    }
    
    # Règles simples (symboles)
    t_ASSIGN = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    
    # Opérateurs arithmétiques
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    
    # Opérateurs de comparaison
    t_EQ = r'=='
    t_NE = r'!='
    t_LE = r'<='
    t_GE = r'>='
    t_LT = r'<'
    t_GT = r'>'
    
    # Ignorer espaces et tabulations
    t_ignore = ' \t'
    
    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        # Vérifier si c'est un mot-clé
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t
    
    def t_COMMENT(self, t):
        r'\#.*'
        pass  # Ignorer les commentaires
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    def t_error(self, t):
        print(f"Caractère illégal '{t.value[0]}' à la ligne {t.lineno}")
        t.lexer.skip(1)
    
    def __init__(self):
        self.lexer = lex.lex(module=self)
    
    def tokenize(self, data):
        """Tokenize le code source et retourne la liste des tokens"""
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens


# Test du lexer
if __name__ == "__main__":
    lexer = Lexer()
    
    test_code = """
    let i = 0
    
    while i < 5 {
        print(i)
        i = i + 1
    }
    """
    
    print("=== Test du Lexer - Phase 5 ===\n")
    print("Code source :")
    print(test_code)
    
    print("\nTokens générés :")
    tokens = lexer.tokenize(test_code)
    for tok in tokens:
        print(f"  {tok.type:12} : {tok.value}")
