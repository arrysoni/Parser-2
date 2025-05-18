# 🔍 Custom Language Parser – Scoping Rules, Type Checking & Expression Handling

## 📚 Project Description

This project implements a **custom parser and lexer** for a simplified programming language with support for:
- **Lexical analysis**
- **Scoping rules**
- **Symbol table management**
- **Type checking**
- **Control flow (if, else, while)**
- **Arithmetic and Boolean expressions**

It simulates a frontend component of a compiler by converting source code into an abstract syntax tree (AST) and validating semantic correctness.

---

## 🧠 Key Features

### ✅ 1. **Lexer**
- Tokenizes:
  - Keywords: `int`, `float`, `if`, `else`, `while`
  - Symbols: `=`, `==`, `!=`, `<`, `>`, `+`, `-`, `*`, `/`, `{`, `}`, `(`, `)`
  - Numbers: Integers and floats (with float format validation)
  - Identifiers
- Skips whitespace and handles multi-character tokens
- Raises error on invalid characters

### ✅ 2. **Parser**
Implements a top-down recursive descent parser with semantic checks.

#### 🔄 Scoping Support
- Maintains a symbol table per scope using `scope_stack`
- Supports nested scopes via `{}` blocks
- Logs error on:
  - Redeclaration in same scope
  - Usage of undeclared variables

#### ✅ Type Checking
- Enforces type consistency for:
  - Declarations
  - Assignments
  - Binary operations (e.g., `int + float` ➝ ❌)
- Supports type-aware AST node construction (`value_type` annotations)

---

## 🔧 Supported Statements

| Statement Type      | Syntax Example                         | Notes                                 |
|---------------------|----------------------------------------|----------------------------------------|
| Variable Declaration| `int a = 5;`                           | Must be declared before use           |
| Assignment          | `a = b + 1;`                           | Type must match declaration           |
| If Statement        | `if a < b { ... } else { ... }`        | Scope opens for then/else blocks      |
| While Loop          | `while a != b { ... }`                 | Scope opens within loop body          |
| Function Call       | `foo(x, y)`                            | Supports basic function call parsing  |

---

## 🧩 Expression Support

- **Arithmetic**: `+`, `-`, `*`, `/`
- **Boolean**: `==`, `!=`, `<`, `>`
- **Grouped expressions**: `(a + b)`
- Supports type validation across operands

---

## 🧠 ASTNodeDefs Dependency

All expressions and statements are returned as instances of classes like:
- `AST.Declaration`
- `AST.Assignment`
- `AST.Block`
- `AST.BinaryOperation`
- `AST.IfStatement`, `AST.WhileStatement`, etc.

These must be defined in the `ASTNodeDefs` module imported as `AST`.

---

## 🔍 Error Handling

All semantic errors are appended to `self.messages`, including:
- Redeclaration in same scope
- Usage of undeclared variables
- Type mismatch
- Invalid syntax tokens

---

## 📁 File Structure

| File            | Description                          |
|-----------------|--------------------------------------|
| `Parser.py`     | Contains the `Lexer` and `Parser` classes |
| `ASTNodeDefs.py`| Defines the required AST node types  |
| `main.py`       | (Optional) To run and test the parser |
| `tests/`        | Contains sample code snippets for testing |

---

## 🚀 How to Run

### 1. Prepare input:
Write your program snippet in a `.txt` file or multiline string.

### 2. Tokenize:
```python
lexer = Lexer(code)
tokens = lexer.tokenize()


parser = Parser(tokens)
ast = parser.parse()


for msg in parser.messages:
    print("Error:", msg)

Error: Type Mismatch between int and float
