import os

def calcular(operacion, a, b):
    # BUG: No maneja división por cero
    if operacion == "dividir":
        return a / b
    
    # CODE SMELL: Código duplicado y lógica innecesaria
    if operacion == "suma":
        res = a + b
        return a + b
    
    # VULNERABILIDAD: Uso de eval() con entrada de usuario (Peligro!)
    return eval(f"{a} {operacion} {b}")

# Hardcoded password (Vulnerabilidad de seguridad)
ADMIN_PW = "12345678"

print(calcular("dividir", 10, 0))