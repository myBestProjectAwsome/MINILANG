"""
MiniLang Lexer - Phase 4
Support : let, print, arithmétique, if/else, comparaisons
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
        'IF',        # NOUVEAU Phase 4
        'ELSE',      # NOUVEAU Phase 4
        
        # Opérateurs arithmétiques
        'PLUS',
        'MINUS',
        'MULTIPLY',
        'DIVIDE',
        
        # Opérateurs de comparaison (NOUVEAU Phase 4)
        'EQ',        # ==
        'NE',        # !=
        'LT',        # <
        'LE',        # <=
        'GT',        # >
        'GE',        # >=
        
        # Opérateurs
        'ASSIGN',
        
        # Délimiteurs
        'LPAREN',
        'RPAREN',
        'LBRACE',    # NOUVEAU Phase 4 : {
        'RBRACE',    # NOUVEAU Phase 4 : }
    )
    
    # Mots-clés réservés
    reserved = {
        'let': 'LET',
        'print': 'PRINT',
        'if': 'IF',      # NOUVEAU Phase 4
        'else': 'ELSE',  # NOUVEAU Phase 4
    }
    
    # Règles simples (symboles)
    t_ASSIGN = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'   # NOUVEAU Phase 4
    t_RBRACE = r'\}'   # NOUVEAU Phase 4
    
    # Opérateurs arithmétiques
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    
    # Opérateurs de comparaison (NOUVEAU Phase 4)
    # IMPORTANT : == avant = pour éviter les conflits
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
    
    # Code de test
    test_code = """
    let x = 42
    
    if x > 10 {
        print(1)
    } else {
        print(0)
    }
    """
    
    print("=== Test du Lexer - Phase 4 ===\n")
    print("Code source :")
    print(test_code)
    
    print("\nTokens générés :")
    tokens = lexer.tokenize(test_code)
    for tok in tokens:
        print(f"  {tok.type:12} : {tok.value}")
