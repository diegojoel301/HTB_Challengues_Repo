import random

# El valor objetivo que queremos encontrar
target_value = 608905406

# Banderas para saber si encontramos la semilla
found = False

# Probar todas las posibles semillas
for seed in range(2**32):
    random.seed(seed)
    if random.randint(0, 2**31 - 1) == target_value:
        print(f"Found seed: {seed}")
        found = True
        break

if not found:
    print("Seed not found.")

