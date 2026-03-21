"""
MiniLang Code Generator - Phase 5
Support : let, print, arithmétique, if/else, while, assignation
"""

from parser import (
    Program, LetStatement, AssignStatement, PrintStatement,
    IfStatement, WhileStatement,
    IntegerLiteral, Variable, BinaryOp
)


class CodeGenerator:
    """Générateur de code C pour MiniLang"""
    
    def __init__(self):
        self.variables = {}
        self.indent_level = 0
    
    def indent(self):
        return "    " * self.indent_level
    
    def generate(self, ast):
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
        if isinstance(stmt, LetStatement):
            return self.generate_let(stmt)
        elif isinstance(stmt, AssignStatement):
            return self.generate_assign(stmt)
        elif isinstance(stmt, PrintStatement):
            return self.generate_print(stmt)
        elif isinstance(stmt, IfStatement):
            return self.generate_if(stmt)
        elif isinstance(stmt, WhileStatement):
            return self.generate_while(stmt)
        else:
            raise ValueError(f"Type d'instruction inconnu : {type(stmt)}")
    
    def generate_let(self, stmt):
        """let x = 42"""
        value_code = self.generate_expression(stmt.value)
        self.variables[stmt.name] = "int"
        return f"{self.indent()}int {stmt.name} = {value_code};"
    
    def generate_assign(self, stmt):
        """x = 10 (NOUVEAU Phase 5)"""
        if stmt.name not in self.variables:
            raise ValueError(f"Variable non déclarée : {stmt.name}")
        value_code = self.generate_expression(stmt.value)
        return f"{self.indent()}{stmt.name} = {value_code};"
    
    def generate_print(self, stmt):
        """print(x)"""
        expr_code = self.generate_expression(stmt.expression)
        return f'{self.indent()}printf("%d\\n", {expr_code});'
    
    def generate_if(self, stmt):
        """if ... else"""
        code = []
        condition_code = self.generate_expression(stmt.condition)
        code.append(f"{self.indent()}if ({condition_code}) {{")
        
        self.indent_level += 1
        for then_stmt in stmt.then_block:
            stmt_code = self.generate_statement(then_stmt)
            if isinstance(stmt_code, list):
                code.extend(stmt_code)
            else:
                code.append(stmt_code)
        self.indent_level -= 1
        
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
    
    def generate_while(self, stmt):
        """while ... (NOUVEAU Phase 5)"""
        code = []
        condition_code = self.generate_expression(stmt.condition)
        code.append(f"{self.indent()}while ({condition_code}) {{")
        
        self.indent_level += 1
        for body_stmt in stmt.body:
            stmt_code = self.generate_statement(body_stmt)
            if isinstance(stmt_code, list):
                code.extend(stmt_code)
            else:
                code.append(stmt_code)
        self.indent_level -= 1
        
        code.append(f"{self.indent()}}}")
        return code
    
    def generate_expression(self, expr):
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
let i = 0

while i < 5 {
    print(i)
    i = i + 1
}
"""
    
    print("=== Test du Générateur - Phase 5 ===\n")
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
