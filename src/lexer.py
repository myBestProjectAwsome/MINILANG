"""
MiniLang Lexer - Phase 3
Transforme le code source en tokens (mots-clés, nombres, symboles)
Support : let, print, opérateurs arithmétiques (+, -, *, /)
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
        
        # Opérateurs arithmétiques (AJOUTÉ pour Phase 3)
        'PLUS',
        'MINUS',
        'MULTIPLY',
        'DIVIDE',
        
        # Opérateurs
        'ASSIGN',
        
        # Délimiteurs
        'LPAREN',
        'RPAREN',
    )
    
    # Mots-clés réservés
    reserved = {
        'let': 'LET',
        'print': 'PRINT',
    }
    
    # Règles simples (symboles)
    t_ASSIGN = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    
    # Opérateurs arithmétiques (AJOUTÉ pour Phase 3)
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    
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
    let x = 10 + 5
    let y = x * 2
    let z = y - 3
    print(z)
    """
    
    print("=== Test du Lexer - Phase 3 ===\n")
    print("Code source :")
    print(test_code)
    
    print("\nTokens générés :")
    tokens = lexer.tokenize(test_code)
    for tok in tokens:
        print(f"  {tok.type:12} : {tok.value}")
