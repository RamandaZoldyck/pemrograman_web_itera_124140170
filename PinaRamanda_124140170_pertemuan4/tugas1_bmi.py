print("=" * 40)
print("       PROGRAM PENGHITUNG BMI")
print("=" * 40)

berat = float(input("Masukkan berat badan (kg): "))
tinggi = float(input("Masukkan tinggi badan (m): "))

if berat <= 0 or tinggi <= 0:
    print("Berat dan tinggi badan harus lebih dari 0.")
else:
    bmi = berat / (tinggi * tinggi)

    if bmi < 18.5:
        kategori = "Berat badan kurang"
    elif bmi < 25:
        kategori = "Berat badan normal"
    elif bmi < 30:
        kategori = "Berat badan berlebih"
    else:
        kategori = "Obesitas"

    print("\n========== HASIL BMI ==========")
    print(f"Berat Badan : {berat:.2f} kg")
    print(f"Tinggi Badan: {tinggi:.2f} m")
    print(f"Nilai BMI   : {bmi:.2f}")
    print(f"Kategori    : {kategori}")
    print("=" * 40)
