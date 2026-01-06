# code2.py - un autre code volontairement erroné et plus long

def greet(name):
print("Hello " + name)  # IndentationError

greet("World")

y = 10
if y = 5:  # SyntaxError, mauvais opérateur
    print("Y is 5")

def factorial(n):
    if n == 0:
        return 1
    else:
    return n * factorial(n-1)  # IndentationError

def divide(a, b):
    return a/b  # Warning : division sans gestion de ZeroDivisionError

# Variable jamais utilisée
unused_var = 123
