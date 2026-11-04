import math_operations

from math_operations import (
    luas_persegi,
    keliling_persegi,
    celsius_ke_fahrenheit,
    celsius_ke_kelvin
)


print("=" * 50)
print("          PROGRAM OPERASI MATEMATIKA")
print("=" * 50)

# 1. Persegi
print("\n1. PERSEGI")
sisi = 5
print(f"Sisi     : {sisi}")
print(f"Luas     : {luas_persegi(sisi)}")
print(f"Keliling : {keliling_persegi(sisi)}")

# 2. Persegi panjang
print("\n2. PERSEGI PANJANG")
panjang = 10
lebar = 5
print(f"Panjang  : {panjang}")
print(f"Lebar    : {lebar}")
print(
    f"Luas     : "
    f"{math_operations.luas_persegi_panjang(panjang, lebar)}"
)
print(
    f"Keliling : "
    f"{math_operations.keliling_persegi_panjang(panjang, lebar)}"
)

# 3. Lingkaran
print("\n3. LINGKARAN")
jari_jari = 7
print(f"Jari-jari: {jari_jari}")
print(f"Luas     : {math_operations.luas_lingkaran(jari_jari):.2f}")
print(f"Keliling : {math_operations.keliling_lingkaran(jari_jari):.2f}")

# 4. Konversi temperatur
print("\n4. KONVERSI TEMPERATUR")
suhu = 30
print(f"Celsius    : {suhu} C")
print(f"Fahrenheit : {celsius_ke_fahrenheit(suhu):.2f} F")
print(f"Kelvin     : {celsius_ke_kelvin(suhu):.2f} K")

print(f"\nKonstanta PI: {math_operations.PI}")
print("\n" + "=" * 50)
print("             PROGRAM SELESAI")
print("=" * 50)
