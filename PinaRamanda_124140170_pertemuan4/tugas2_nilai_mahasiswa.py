# data mahasiswa. 
mahasiswa = [
    {
        "nama": "Zoldyck",
        "nim": "124140170",
        "nilai_uts": 95,
        "nilai_uas": 90,
        "nilai_tugas": 100
    },
    {
        "nama": "jel",
        "nim": "124140056",
        "nilai_uts": 75,
        "nilai_uas": 80,
        "nilai_tugas": 85
    },
    {
        "nama": "leon",
        "nim": "124140098",
        "nilai_uts": 65,
        "nilai_uas": 70,
        "nilai_tugas": 60
    },
    {
        "nama": "cey",
        "nim": "124140097",
        "nilai_uts": 90,
        "nilai_uas": 95,
        "nilai_tugas": 92
    },
    {
        "nama": "qiwn",
        "nim": "124140055",
        "nilai_uts": 80,
        "nilai_uas": 75,
        "nilai_tugas": 90
    }
]

# Menghitung nilai akhir dan menentukan grade setiap mahasiswa.
for data in mahasiswa:
    nilai_akhir = (
        0.30 * data["nilai_uts"]
        + 0.40 * data["nilai_uas"]
        + 0.30 * data["nilai_tugas"]
    )
    data["nilai_akhir"] = nilai_akhir

    if nilai_akhir >= 80:
        data["grade"] = "A"
    elif nilai_akhir >= 70:
        data["grade"] = "B"
    elif nilai_akhir >= 60:
        data["grade"] = "C"
    elif nilai_akhir >= 50:
        data["grade"] = "D"
    else:
        data["grade"] = "E"

# Menampilkan seluruh data mahasiswa dalam bentuk tabel.
print("=" * 83)
print("                         DATA NILAI MAHASISWA")
print("=" * 83)
print(
    f"{'Nama':<12}"
    f"{'NIM':<15}"
    f"{'UTS':>8}"
    f"{'UAS':>8}"
    f"{'Tugas':>8}"
    f"{'Nilai Akhir':>15}"
    f"{'Grade':>10}"
)
print("-" * 83)

for data in mahasiswa:
    print(
        f"{data['nama']:<12}"
        f"{data['nim']:<15}"
        f"{data['nilai_uts']:>8}"
        f"{data['nilai_uas']:>8}"
        f"{data['nilai_tugas']:>8}"
        f"{data['nilai_akhir']:>15.2f}"
        f"{data['grade']:>10}"
    )

print("=" * 83)

# Mencari mahasiswa dengan nilai akhir tertinggi dan terendah.
nilai_tertinggi = max(mahasiswa, key=lambda data: data["nilai_akhir"])
nilai_terendah = min(mahasiswa, key=lambda data: data["nilai_akhir"])

print("\nMAHASISWA DENGAN NILAI TERTINGGI")
print(f"Nama        : {nilai_tertinggi['nama']}")
print(f"NIM         : {nilai_tertinggi['nim']}")
print(f"Nilai Akhir : {nilai_tertinggi['nilai_akhir']:.2f}")
print(f"Grade       : {nilai_tertinggi['grade']}")

print("\nMAHASISWA DENGAN NILAI TERENDAH")
print(f"Nama        : {nilai_terendah['nama']}")
print(f"NIM         : {nilai_terendah['nim']}")
print(f"Nilai Akhir : {nilai_terendah['nilai_akhir']:.2f}")
print(f"Grade       : {nilai_terendah['grade']}")
