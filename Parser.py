import ASTNodeDefs as AST


class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []

    # Move to the next position in the code increment by one.
    def advance(self):
        self.position += 1
        if self.position >= len(self.code):
            self.current_char = None
        else:
            self.current_char = self.code[self.position]

    # If the current char is whitespace, move ahead.
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Tokenize the identifier.
    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return ('IDENTIFIER', result)

    # Tokenize numbers, including float handling
    def number(self):
        result = ''
        is_float = False

        # TODO: Update this code to handle floating-point numbers
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            # Handling the case for float
            if self.current_char == '.':
                if is_float:    # A number cannot be float twice
                    raise ValueError(
                        'Invalid number as a number cannot have two decimal points.')
                is_float = True
            result += self.current_char
            self.advance()

        # Making sure the formatting for a float number is correct
        if is_float and (result.startswith('.') or result.endswith('.')):
            raise ValueError(f"Invalid float format: {result}")

        if is_float:
            return ('FNUMBER', float(result))
        else:
            return ('NUMBER', int(result))

    def token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                elif ident[1] == 'else':
                    return ('ELSE', 'else')
                elif ident[1] == 'while':
                    return ('WHILE', 'while')
                elif ident[1] == 'int':
                    return ('INT', 'int')
                elif ident[1] == 'float':
                    return ('FLOAT', 'float')
                return ident  # Generic identifier
            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()
            if self.current_char == '+':
                self.advance()
                return ('PLUS', '+')
            if self.current_char == '-':
                self.advance()
                return ('MINUS', '-')
            if self.current_char == '*':
                self.advance()
                return ('MULTIPLY', '*')
            if self.current_char == '/':
                self.advance()
                return ('DIVIDE', '/')
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('EQ', '==')
                return ('EQUALS', '=')
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('NEQ', '!=')
            if self.current_char == '<':
                self.advance()
                return ('LESS', '<')
            if self.current_char == '>':
                self.advance()
                return ('GREATER', '>')
            if self.current_char == '(':
                self.advance()
                return ('LPAREN', '(')
            if self.current_char == ')':
                self.advance()
                return ('RPAREN', ')')
            if self.current_char == ',':
                self.advance()
                return ('COMMA', ',')
            if self.current_char == ':':
                self.advance()
                return ('COLON', ':')
            # TODO: Implement handling for '{' and '}' tokens here (see `tokens.txt` for exact names)
            # Tokens.txt referred for this part
            if self.current_char == '{':
                self.advance()
                return ('LBRACE', '{')
            if self.current_char == '}':
                self.advance()
                return ('RBRACE', '}')
            if self.current_char == '\n':
                self.advance()
                continue

            raise ValueError(
                f"Illegal character at position {self.position}: {self.current_char}")

        return ('EOF', None)

    # Collect all the tokens in a list.
    def tokenize(self):
        while True:
            token = self.token()
            self.tokens.append(token)
            if token[0] == 'EOF':
                break
        return self.tokens


# Looks good above!


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)
        # Use these to track the variables and their scope
        self.symbol_table = {'global': {}}
        self.scope_counter = 0
        self.scope_stack = ['global']
        self.messages = []

    def error(self, message):
        self.messages.append(message)

    def advance(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)

    # TODO: Implement logic to enter a new scope, add it to symbol table, and update `scope_stack`
    def enter_scope(self):

        new_scope = f"scope_{self.scope_counter}"
        self.scope_counter += 1
        print(f"Entering scope: {new_scope}")

        self.symbol_table[new_scope] = {}   # Entering a new scope
        self.scope_stack.append(new_scope)  # Updating a scope_stack

    # TODO: Implement logic to exit the current scope, removing it from `scope_stack`
    def exit_scope(self):

        if len(self.scope_stack) == 1:
            self.error("Cannot exit global scope.")
        else:
            # Removing scope from scope stack as we are out of it
            remove_scope = self.scope_stack.pop()
            # Upating the symbol table
            del self.symbol_table[remove_scope]

    # Return the current scope name
    def current_scope(self):
        return self.scope_stack[-1]

    # TODO: Check if a variable is already declared in the current scope; if so, log an error
    def checkVarDeclared(self, identifier):

        current_scope = self.current_scope()

        # Checking for an already declared variable in the current scope
        if identifier in self.symbol_table[current_scope]:
            self.error(
                f"Variable {identifier} has already been declared in the current scope")
            return True
        return False

    # TODO: Check if a variable is declared in any accessible scope; if not, log an error
    def checkVarUse(self, identifier):

        # Checking if the variable has been declared in any of the accessible scopes: global or any reachable scope
        print('Symbol Table:', self.symbol_table, self.scope_stack)
        # Needs to be reversed since we have to check for the previous scope
        for i in range(len(self.scope_stack)-1, -1, -1):
            scope = self.scope_stack[i]

            print('Identifier: ', identifier)
            if scope in self.symbol_table and identifier in self.symbol_table[scope]:
                return True

        # Variable hasn't been decared if not previously found in the symbol table
        if identifier not in self.symbol_table[self.current_scope()]:
            self.error(
                f"Variable {identifier} has not been declared in the current or any enclosing scopes")
        return False

    # TODO: Check type mismatch between two entities; log an error if they do not match
    def checkTypeMatch2(self, vType, eType, var, exp):

        # The project only requires us to check for 'int' and 'float' mistmatches
        if (vType == 'int' and eType == 'float') or (vType == 'float' and eType == 'int'):
            self.error(f"Type Mismatch between {vType} and {eType}")
            return False

        return True

    # TODO: Implement logic to add a variable to the current scope in `symbol_table`
    def add_variable(self, name, var_type):

        current_scope = self.current_scope()

        # If not previously added in the symbol table, then add the variable
        if name not in self.symbol_table[current_scope]:
            self.symbol_table[current_scope][name] = var_type

    # TODO: Retrieve the variable type from `symbol_table` if it exists
    def get_variable_type(self, name):

        # Getting the variable type from the symbol table
        for i in range(len(self.scope_stack) - 1, -1, -1):
            scope = self.scope_stack[i]
            if name in self.symbol_table[scope]:
                return self.symbol_table[scope][name]

        return None

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.statement())
        return AST.Block(statements)

    # TODO: Modify the `statement` function to dispatch to declare statement
    def statement(self):

        # Making sure that the flow of code and the syntax of the program is as expected
        if self.current_token[0] in ['INT', 'FLOAT']:
            return self.decl_stmt()
        elif self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'EQUALS':
                return self.assign_stmt()
            elif self.peek() == 'LPAREN':
                return self.function_call()
            else:
                self.error(
                    f"Unexpected token after identifier: {self.current_token}")

        # Handles cases for if and while statements
        elif self.current_token[0] == 'IF':
            return self.if_stmt()
        elif self.current_token[0] == 'WHILE':
            return self.while_stmt()
        else:
            self.error(f"Unexpected token: {self.current_token}")

    # TODO: Implement the declaration statement and handle adding the variable to the symbol table
    def decl_stmt(self):
        """
        Parses a declaration statement.
        Example:
        int x = 5
        float y = 3.5
        TODO: Implement logic to parse type, identifier, and initialization expression and also handle type checking
        """

        var_type = self.current_token[1]
        self.advance()

        # Declaration statement starts with an identifier = expression
        if self.current_token[0] != 'IDENTIFIER':
            self.error(f"Expected an identifier, got {self.current_token}")
            return None

        var_name = self.current_token[1]
        # Checking for an already declared variable in the current scope, and handles errors if needed
        self.checkVarDeclared(var_name)

        self.advance()

        expression = None
        # Moving to equals
        if self.current_token[0] == 'EQUALS':
            self.advance()
            # Moving to expression
            expression = self.expression()
            expr_type = expression.value_type

            # Checking for type mismatch between identifier and expression
            self.checkTypeMatch2(var_type, expr_type, var_name, expression)

        # Adding variable to symbol table to the symbol table
        self.add_variable(var_name, var_type)

        return AST.Declaration(var_type, var_name, expression)

    # TODO: Parse assignment statements, handle type checking
    def assign_stmt(self):
        """
        Parses an assignment statement.
        Example:
        x = 10
        x = y + 5
        TODO: Implement logic to handle assignment, including type checking.
        """

        if self.current_token[0] != 'IDENTIFIER':
            self.error(
                f"Expected an identifier for assignment, got {self.current_token}")
        var_name = self.current_token[1]

        # Checking if the variable has been declared in any of the accessible scopes
        self.checkVarUse(var_name)
        self.advance()

        # Getting equals
        if self.current_token[0] != 'EQUALS':
            self.error(f"Expected '=', got {self.current_token}")
        self.advance()

        # Getting expression
        expression = self.expression()

        # Checking for type mismatches in the expression
        var_type = self.get_variable_type(var_name)
        print(var_type, expression.value_type)
        self.checkTypeMatch2(
            var_type, expression.value_type, var_name, expression)

        return AST.Assignment(var_name, expression)

    # TODO: Implement the logic to parse the if condition and blocks of code
    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition {
            # statements
        }
        else {
            # statements
        }
        TODO: Implement the logic to parse the if condition and blocks of code.
        """

        # If condition {}   else{}
        if self.current_token[0] != 'IF':
            self.error(f"Expected 'IF', got {self.current_token}")
        self.advance()

        # Condition expected after 'if'
        condition = self.boolean_expression()

        # Curly Braces expected after the condition statememt
        if self.current_token[0] != 'LBRACE':
            self.error(f"Expected '{{', got {self.current_token}")
        self.advance()
        self.enter_scope()
        then_block = self.block()

        if self.current_token[0] != 'RBRACE':
            self.error(f"Expected '}}', got {self.current_token}")
        self.advance()
        self.exit_scope()

        else_block = None

        # Handling else block similarly to the if block
        if self.current_token[0] == 'ELSE':
            self.advance()

            if self.current_token[0] != 'LBRACE':
                self.error(f"Expected '{{', got {self.current_token}")
            self.advance()
            self.enter_scope()
            else_block = self.block()

            if self.current_token[0] != 'RBRACE':
                self.error(f"Expected '}}', got {self.current_token}")
                return None
            self.advance()
            self.exit_scope()
        return AST.IfStatement(condition, then_block, else_block)

    # TODO: Implement the logic to parse while loops with a condition and a block of statements
    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition {
            # statements
        }
        TODO: Implement the logic to parse while loops with a condition and a block of statements.
        """

        if self.current_token[0] != 'WHILE':
            self.error(f"Expected 'WHILE', got {self.current_token}")
        self.advance()

        condition = self.boolean_expression()

        if self.current_token[0] != 'LBRACE':
            self.error(f"Expected '{{', got {self.current_token}")
        self.advance()
        self.enter_scope()
        block = self.block()

        if self.current_token[0] != 'RBRACE':
            self.error(f"Expected '}}', got {self.current_token}")
        self.advance()
        self.exit_scope()

        return AST.WhileStatement(condition, block)

    # TODO: Implement logic to capture multiple statements as part of a block
    def block(self):
        """
        Parses a block of statements. A block is a collection of statements grouped by `{}`.
        Example:

        x = 5
        y = 10

        TODO: Implement logic to capture multiple statements as part of a block.
        """

        # Storing the statements in an array
        statements = []
        while self.current_token[0] != 'RBRACE' and self.current_token[0] != 'EOF':
            statements.append(self.statement())

        return AST.Block(statements)

    # TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence and type checking
    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence and type checking.
        """
        left = self.term()      # Left Term
        while self.current_token[0] in ['PLUS', 'MINUS']:
            operator = self.current_token[0]
            self.advance()
            right = self.term()   # Right term

            # Checking for type mismatch
            self.checkTypeMatch2(
                left.value_type, right.value_type, left, right)

            left = AST.BinaryOperation(
                left, operator, right, value_type=left.value_type)

        return left

    # TODO: Implement parsing for boolean expressions and check for type compatibility
    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        TODO: Implement parsing for boolean expressions and check for type compatibility.
        """

        left = self.expression()  # Left term

        # Boolean operator expected
        if (self.current_token[0] != 'EQ') and (self.current_token[0] != 'NEQ') and (self.current_token[0] != 'LESS') and (self.current_token[0] != 'GREATER'):
            self.error(
                f"Expected a boolean operator, got {self.current_token}")

        operator = self.current_token[0]
        self.advance()
        right = self.expression()  # Right term

        self.checkTypeMatch2(left.value_type, right.value_type, left, right)

        return AST.BooleanExpression(left, operator, right)

    # TODO: Implement parsing for multiplication and division and check for type compatibility
    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        TODO: Implement parsing for multiplication and division and check for type compatibility.
        """

        # Checking type compatibility for multiplication and division products

        left = self.factor()  # Left term

        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token[0]
            self.advance()
            right = self.factor()   # Right term
            self.checkTypeMatch2(
                left.value_type, right.value_type, left, right)

            left = AST.BinaryOperation(
                left, op, right, value_type=left.value_type)
        return left

    def factor(self):
        if self.current_token[0] == 'NUMBER':
            # handle int
            num = self.current_token[1]
            self.advance()
            return AST.Factor(num, 'int')
        elif self.current_token[0] == 'FNUMBER':
            # handle float
            num = self.current_token[1]
            self.advance()
            return AST.Factor(num, 'float')
        elif self.current_token[0] == 'IDENTIFIER':
            # TODO: Ensure that you parse the identifier correctly, retrieve its type from the symbol table, and check if it has been declared in the current or any enclosing scopes.
            var_name = self.current_token[1]
            # Checking if the variable has been declared in any of the accessible scopes
            self.checkVarUse(var_name)

            var_type = self.get_variable_type(var_name)
            self.advance()
            return AST.Factor(var_name, var_type)

        # Parsing identifier correctly
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self.expression()
            self.expect('RPAREN')
            return expr
        else:
            self.error(
                f"Unexpected token in factor: {self.current_token}")

    # These function had already been implemented for us

    def function_call(self):
        func_name = self.current_token[1]
        self.advance()
        self.expect('LPAREN')
        args = self.arg_list()
        self.expect('RPAREN')

        return AST.FunctionCall(func_name, args)

    def arg_list(self):
        """
        Parses a list of function arguments.
        Example:
        (x, y + 5)
        """
        args = []
        if self.current_token[0] != 'RPAREN':
            args.append(self.expression())
            while self.current_token[0] == 'COMMA':
                self.advance()
                args.append(self.expression())

        return args

    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise ValueError(
                f"Expected token {token_type}, but got {self.current_token[0]}")

    def peek(self):
        return self.tokens[0][0] if self.tokens else None
