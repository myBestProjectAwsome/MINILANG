"""
MiniLang Code Generator - Phase 4
Support : let, print, arithmétique, if/else
"""

from parser import (
    Program, LetStatement, PrintStatement, IfStatement,
    IntegerLiteral, Variable, BinaryOp
)


class CodeGenerator:
    """Générateur de code C pour MiniLang"""
    
    def __init__(self):
        self.variables = {}
        self.indent_level = 0
    
    def indent(self):
        """Retourne l'indentation courante"""
        return "    " * self.indent_level
    
    def generate(self, ast):
        """Génère le code C complet"""
        if not isinstance(ast, Program):
            raise ValueError("L'AST doit être un Programme")
        
        code = []
        code.append("#include <stdio.h>")
        code.append("#include <stdlib.h>")
        code.append("")
        code.append("int main() {")
        self.indent_level += 1
        
        for statement in ast.statements:
            stmt_code = self.generate_statement(statement)
            if isinstance(stmt_code, list):
                code.extend(stmt_code)
            else:
                code.append(stmt_code)
        
        code.append(self.indent() + "return 0;")
        self.indent_level -= 1
        code.append("}")
        
        return "\n".join(code)
    
    def generate_statement(self, stmt):
        """Génère le code pour une instruction"""
        if isinstance(stmt, LetStatement):
            return self.generate_let(stmt)
        elif isinstance(stmt, PrintStatement):
            return self.generate_print(stmt)
        elif isinstance(stmt, IfStatement):
            return self.generate_if(stmt)
        else:
            raise ValueError(f"Type d'instruction inconnu : {type(stmt)}")
    
    def generate_let(self, stmt):
        """Génère : let x = 42"""
        value_code = self.generate_expression(stmt.value)
        self.variables[stmt.name] = "int"
        return f"{self.indent()}int {stmt.name} = {value_code};"
    
    def generate_print(self, stmt):
        """Génère : print(x)"""
        expr_code = self.generate_expression(stmt.expression)
        return f'{self.indent()}printf("%d\\n", {expr_code});'
    
    def generate_if(self, stmt):
        """Génère : if ... else (NOUVEAU Phase 4)"""
        code = []
        
        # Condition
        condition_code = self.generate_expression(stmt.condition)
        code.append(f"{self.indent()}if ({condition_code}) {{")
        
        # Bloc then
        self.indent_level += 1
        for then_stmt in stmt.then_block:
            stmt_code = self.generate_statement(then_stmt)
            if isinstance(stmt_code, list):
                code.extend(stmt_code)
            else:
                code.append(stmt_code)
        self.indent_level -= 1
        
        # Bloc else (optionnel)
        if stmt.else_block:
            code.append(f"{self.indent()}}} else {{")
            self.indent_level += 1
            for else_stmt in stmt.else_block:
                stmt_code = self.generate_statement(else_stmt)
                if isinstance(stmt_code, list):
                    code.extend(stmt_code)
                else:
                    code.append(stmt_code)
            self.indent_level -= 1
        
        code.append(f"{self.indent()}}}")
        
        return code
    
    def generate_expression(self, expr):
        """Génère le code pour une expression"""
        if isinstance(expr, IntegerLiteral):
            return str(expr.value)
        
        elif isinstance(expr, Variable):
            if expr.name not in self.variables:
                raise ValueError(f"Variable non déclarée : {expr.name}")
            return expr.name
        
        elif isinstance(expr, BinaryOp):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)
            return f"({left} {expr.operator} {right})"
        
        else:
            raise ValueError(f"Type d'expression inconnu : {type(expr)}")


# Test
if __name__ == "__main__":
    from parser import Parser
    
    parser = Parser()
    
    test_code = """
let x = 42

if x > 10 {
    print(1)
} else {
    print(0)
}
"""
    
    print("=== Test du Générateur - Phase 4 ===\n")
    print("Code MiniLang :")
    print(test_code)
    
    ast = parser.parse(test_code)
    
    if ast:
        print("⚙️  Génération de code C...\n")
        codegen = CodeGenerator()
        c_code = codegen.generate(ast)
        
        print("=" * 50)
        print("CODE C GÉNÉRÉ :")
        print("=" * 50)
        print(c_code)
        print("=" * 50)
