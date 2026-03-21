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
    let y = 84
    print(x)
    print(y)
    """
    
    print("=== Test du Lexer - Phase 1 ===\n")
    print("Code source :")
    print(test_code)
    
    print("\nTokens générés :")
    tokens = lexer.tokenize(test_code)
    for tok in tokens:
        print(f"  {tok.type:12} : {tok.value}")
