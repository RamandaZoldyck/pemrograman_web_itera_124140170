PI = 3.14159


def luas_persegi(sisi):
    """Menghitung luas persegi dari parameter sisi dan mengembalikan luasnya."""
    return sisi * sisi


def keliling_persegi(sisi):
    """Menghitung keliling persegi dari parameter sisi dan mengembalikan hasilnya."""
    return 4 * sisi


def luas_persegi_panjang(panjang, lebar):
    """Menghitung luas persegi panjang dari panjang dan lebar, lalu mengembalikannya."""
    return panjang * lebar


def keliling_persegi_panjang(panjang, lebar):
    """Menghitung keliling persegi panjang dari panjang dan lebar, lalu mengembalikannya."""
    return 2 * (panjang + lebar)


def luas_lingkaran(jari_jari):
    """Menghitung luas lingkaran dari jari-jari dan mengembalikan luasnya."""
    return PI * jari_jari * jari_jari


def keliling_lingkaran(jari_jari):
    """Menghitung keliling lingkaran dari jari-jari dan mengembalikan hasilnya."""
    return 2 * PI * jari_jari


def celsius_ke_fahrenheit(celsius):
    """Mengubah suhu Celsius menjadi Fahrenheit dan mengembalikan hasil konversi."""
    return (celsius * 9 / 5) + 32


def celsius_ke_kelvin(celsius):
    """Mengubah suhu Celsius menjadi Kelvin dan mengembalikan hasil konversi."""
    return celsius + 273.15
