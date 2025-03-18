def messy_calc(a, b, c):
    res = 0
    if a > 0:
        res = a * b
    elif a < 0:
        res = a + b
    else:
        res = b - a

    return res

# Messy usage examples
print(messy_calc(5, 2, 12))
print(messy_calc(-3, 4, 3))
print(messy_calc(0, 7, 8))
print(messy_calc(2,3,7))
print(messy_calc(-4,5,11))
print(messy_calc(1,2,3))
