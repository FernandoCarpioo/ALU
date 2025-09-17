import random

def alu(a, b, op, width):
    mask = (1 << width) - 1
    a &= mask
    b &= mask
    resultado = 0
    C = 0
    V = 0

    if op == 'ADD':
        tmp = a + b
        result = tmp & mask
        C = int(tmp > mask)
        V = int(((a ^ b) & (1 << (width-1))) == 0 and ((a ^ resultado) & (1 << (width-1))) != 0)

    elif op == 'SUB':
        tmp = a - b
        result = tmp & mask
        C = int(a >= b)
        V = int(((a ^ b) & (1 << (width-1))) != 0 and ((a ^ resultado) & (1 << (width-1))) != 0)

    elif op == 'AND':
        resultado = a & b

    elif op == 'OR':
        resultado = a | b

    elif op == 'NOT':
        resultado = (~a) & mask

    else:
        raise ValueError("Operación no soportada")

    Z = int(resultado == 0)
    N = int(resultado & (1 << (width-1)) != 0)

    return resultado, Z, N, C, V



print("\n=== Pruebas del testbench VHDL ===")

# Vectores del testbench (A, B, operación con nombre directo)
test_vectors = [
    # Bandera Negative
    ("0003", "0002", "ADD"),  # 3 + 2
    ("0002", "0003", "SUB"),  # 2 - 3 (negativo)
    ("0003", "0002", "AND"),  # and
    ("0003", "0002", "OR"),   # or
    ("0003", "0002", "NOT"),  # not

    # Bandera Carry
    ("FFFF", "0001", "ADD"),  # 65535 + 1 => acarreo
    ("FFFF", "0001", "SUB"),  # 65535 - 1
    ("FFFF", "0001", "AND"),  # and
    ("FFFF", "0001", "OR"),   # or
    ("FFFF", "0001", "NOT"),  # not

    # Bandera Zero
    ("0096", "04D2", "ADD"),  # 150 + 1234
    ("04D2", "04D2", "SUB"),  # 1234 - 1234 (cero)
    ("0096", "04D2", "AND"),  # and
    ("0096", "04D2", "OR"),   # or
    ("0096", "04D2", "NOT"),  # not

    # Bandera Overflow
    ("7530", "0BB8", "ADD"),  # 30000 + 3000 (overflow)
    ("7530", "0BB8", "SUB"),  # 30000 - 3000
    ("7530", "0BB8", "AND"),  # and
    ("7530", "0BB8", "OR"),   # or
    ("7530", "0BB8", "NOT")   # not
]

# Ejecutar las pruebas con la función alu
width = 16
for A_hex, B_hex, op in test_vectors:
    A = int(A_hex, 16)
    B = int(B_hex, 16)
    resultado, Z, N, C, V = alu(A, B, op, width)
    print(f"A={A_hex}, B={B_hex}, Op={op} => R={hex(resultado)}, Z={Z}, N={N}, C={C}, V={V}")
