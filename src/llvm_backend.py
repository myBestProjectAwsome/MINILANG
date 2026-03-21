"""
MiniLang LLVM Backend - Phase 7
Génère du code LLVM IR optimisé au lieu de C
"""

from llvmlite import ir, binding
from parser import (
    Program, LetStatement, AssignStatement, PrintStatement,
    IfStatement, WhileStatement,
    IntegerLiteral, Variable, BinaryOp
)


class LLVMCodeGenerator:
    """Générateur de code LLVM pour MiniLang"""
    
    def __init__(self):
        # Initialiser LLVM (nouvelle API - auto-initialisé)
        # binding.initialize() est dépréciée, LLVM s'initialise automatiquement
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()
        
        # Créer le module LLVM
        self.module = ir.Module(name="minilang_module")
        self.module.triple = binding.get_default_triple()
        
        # Types LLVM de base
        self.int_type = ir.IntType(32)  # int32
        self.void_type = ir.VoidType()
        
        # Variables (nom -> pointeur LLVM)
        self.variables = {}
        
        # Fonction printf (pour print)
        self.printf_func = None
        
        # Format string pour printf (créée une seule fois)
        self.fmt_str = None
        
        # Compteur pour noms uniques
        self.counter = 0
        
        # Builder (pour construire les instructions)
        self.builder = None
        
    def generate(self, ast):
        """
        Génère le code LLVM complet à partir de l'AST
        
        Returns:
            str: Code LLVM IR sous forme de texte
        """
        if not isinstance(ast, Program):
            raise ValueError("L'AST doit être un Programme")
        
        # 1. Déclarer la fonction printf (pour print)
        self._declare_printf()
        
        # 2. Créer la fonction main
        main_func_type = ir.FunctionType(self.int_type, [])
        main_func = ir.Function(self.module, main_func_type, name="main")
        
        # 3. Créer le bloc d'entrée de main
        entry_block = main_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry_block)
        
        # 4. Générer le code pour chaque instruction
        for statement in ast.statements:
            self.generate_statement(statement)
        
        # 5. Retourner 0 à la fin de main
        self.builder.ret(ir.Constant(self.int_type, 0))
        
        # 6. Retourner le code LLVM IR
        return str(self.module)
    
    def _declare_printf(self):
        """Déclare la fonction printf de la libc"""
        # printf prend un char* suivi d'arguments variables
        voidptr_type = ir.IntType(8).as_pointer()
        printf_type = ir.FunctionType(
            self.int_type,  # retourne int
            [voidptr_type],  # prend char* (format string)
            var_arg=True  # arguments variables
        )
        self.printf_func = ir.Function(
            self.module,
            printf_type,
            name="printf"
        )
    
    def generate_statement(self, stmt):
        """Génère le code LLVM pour une instruction"""
        if isinstance(stmt, LetStatement):
            self.generate_let(stmt)
        elif isinstance(stmt, AssignStatement):
            self.generate_assign(stmt)
        elif isinstance(stmt, PrintStatement):
            self.generate_print(stmt)
        elif isinstance(stmt, IfStatement):
            self.generate_if(stmt)
        elif isinstance(stmt, WhileStatement):
            self.generate_while(stmt)
    
    def generate_let(self, stmt):
        """Génère : let x = 42"""
        # Allouer de l'espace pour la variable sur la pile
        var_ptr = self.builder.alloca(self.int_type, name=stmt.name)
        
        # Calculer la valeur
        value = self.generate_expression(stmt.value)
        
        # Stocker la valeur dans la variable
        self.builder.store(value, var_ptr)
        
        # Enregistrer la variable
        self.variables[stmt.name] = var_ptr
    
    def generate_assign(self, stmt):
        """Génère : x = 10"""
        if stmt.name not in self.variables:
            raise ValueError(f"Variable non déclarée : {stmt.name}")
        
        # Calculer la nouvelle valeur
        value = self.generate_expression(stmt.value)
        
        # Stocker dans la variable
        var_ptr = self.variables[stmt.name]
        self.builder.store(value, var_ptr)
    
    def generate_print(self, stmt):
        """Génère : print(x)"""
        # Créer la format string une seule fois
        if self.fmt_str is None:
            fmt = "%d\n\0"
            fmt_bytes = bytearray(fmt.encode("utf8"))
            fmt_type = ir.ArrayType(ir.IntType(8), len(fmt_bytes))
            fmt_global = ir.GlobalVariable(self.module, fmt_type, name=".fmt")
            fmt_global.linkage = 'internal'
            fmt_global.global_constant = True
            fmt_global.initializer = ir.Constant(fmt_type, fmt_bytes)
            self.fmt_str = fmt_global
        
        # Obtenir un pointeur vers le format string
        fmt_ptr = self.builder.bitcast(
            self.fmt_str,
            ir.IntType(8).as_pointer()
        )
        
        # Calculer l'expression à afficher
        value = self.generate_expression(stmt.expression)
        
        # Appeler printf
        self.builder.call(self.printf_func, [fmt_ptr, value])
    
    def generate_if(self, stmt):
        """Génère : if condition { ... } else { ... }"""
        # Évaluer la condition
        condition = self.generate_expression(stmt.condition)
        
        # Convertir en booléen (!=0)
        bool_condition = self.builder.icmp_signed(
            '!=',
            condition,
            ir.Constant(self.int_type, 0)
        )
        
        # Créer les blocs
        then_block = self.builder.function.append_basic_block(name="if.then")
        else_block = self.builder.function.append_basic_block(name="if.else")
        merge_block = self.builder.function.append_basic_block(name="if.end")
        
        # Branchement conditionnel
        self.builder.cbranch(bool_condition, then_block, else_block)
        
        # Générer le bloc then
        self.builder.position_at_end(then_block)
        for then_stmt in stmt.then_block:
            self.generate_statement(then_stmt)
        self.builder.branch(merge_block)
        
        # Générer le bloc else
        self.builder.position_at_end(else_block)
        if stmt.else_block:
            for else_stmt in stmt.else_block:
                self.generate_statement(else_stmt)
        self.builder.branch(merge_block)
        
        # Continuer après le if
        self.builder.position_at_end(merge_block)
    
    def generate_while(self, stmt):
        """Génère : while condition { ... }"""
        # Créer les blocs
        cond_block = self.builder.function.append_basic_block(name="while.cond")
        body_block = self.builder.function.append_basic_block(name="while.body")
        end_block = self.builder.function.append_basic_block(name="while.end")
        
        # Aller au bloc de condition
        self.builder.branch(cond_block)
        
        # Générer la condition
        self.builder.position_at_end(cond_block)
        condition = self.generate_expression(stmt.condition)
        bool_condition = self.builder.icmp_signed(
            '!=',
            condition,
            ir.Constant(self.int_type, 0)
        )
        self.builder.cbranch(bool_condition, body_block, end_block)
        
        # Générer le corps de la boucle
        self.builder.position_at_end(body_block)
        for body_stmt in stmt.body:
            self.generate_statement(body_stmt)
        self.builder.branch(cond_block)  # Retour à la condition
        
        # Continuer après la boucle
        self.builder.position_at_end(end_block)
    
    def generate_expression(self, expr):
        """Génère le code LLVM pour une expression"""
        if isinstance(expr, IntegerLiteral):
            return ir.Constant(self.int_type, expr.value)
        
        elif isinstance(expr, Variable):
            if expr.name not in self.variables:
                raise ValueError(f"Variable non déclarée : {expr.name}")
            # Charger la valeur depuis la mémoire
            var_ptr = self.variables[expr.name]
            return self.builder.load(var_ptr, name=expr.name)
        
        elif isinstance(expr, BinaryOp):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)
            
            # Opérations arithmétiques
            if expr.operator == '+':
                return self.builder.add(left, right, name='add')
            elif expr.operator == '-':
                return self.builder.sub(left, right, name='sub')
            elif expr.operator == '*':
                return self.builder.mul(left, right, name='mul')
            elif expr.operator == '/':
                return self.builder.sdiv(left, right, name='div')
            
            # Opérations de comparaison
            elif expr.operator == '==':
                return self.builder.icmp_signed('==', left, right, name='eq')
            elif expr.operator == '!=':
                return self.builder.icmp_signed('!=', left, right, name='ne')
            elif expr.operator == '<':
                return self.builder.icmp_signed('<', left, right, name='lt')
            elif expr.operator == '<=':
                return self.builder.icmp_signed('<=', left, right, name='le')
            elif expr.operator == '>':
                return self.builder.icmp_signed('>', left, right, name='gt')
            elif expr.operator == '>=':
                return self.builder.icmp_signed('>=', left, right, name='ge')
            
            else:
                raise ValueError(f"Opérateur inconnu : {expr.operator}")
        
        else:
            raise ValueError(f"Type d'expression inconnu : {type(expr)}")
    
    def compile_to_object(self, output_file):
        """Compile le module LLVM en fichier objet"""
        # Créer le target machine
        target = binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        
        # Compiler en fichier objet
        mod = binding.parse_assembly(str(self.module))
        mod.verify()
        
        with open(output_file, 'wb') as f:
            f.write(target_machine.emit_object(mod))


# Test du backend LLVM
if __name__ == "__main__":
    from parser import Parser
    
    test_code = """
let x = 10 + 5
let y = x * 2
print(y)
"""
    
    print("=== Test du Backend LLVM - Phase 7 ===\n")
    print("Code MiniLang :")
    print(test_code)
    
    # Parser
    parser = Parser()
    ast = parser.parse(test_code)
    
    if ast:
        print("\n⚙️  Génération de code LLVM...\n")
        
        # Générer LLVM IR
        llvm_gen = LLVMCodeGenerator()
        llvm_ir = llvm_gen.generate(ast)
        
        print("=" * 60)
        print("CODE LLVM IR GÉNÉRÉ :")
        print("=" * 60)
        print(llvm_ir)
        print("=" * 60)
