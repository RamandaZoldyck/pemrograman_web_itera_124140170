// ==========================================
// DATA KERANJANG
// ==========================================

// Mengambil data keranjang dari localStorage
let keranjang = JSON.parse(
    localStorage.getItem("keranjangKantinCeria")
) || [];


// ==========================================
// ELEMENT HTML
// ==========================================

const formBarang = document.getElementById("formBarang");

const namaBarang = document.getElementById("namaBarang");
const hargaBarang = document.getElementById("hargaBarang");
const qtyBarang = document.getElementById("qtyBarang");

const errorNama = document.getElementById("errorNama");
const errorHarga = document.getElementById("errorHarga");
const errorQty = document.getElementById("errorQty");

const keranjangBody = document.getElementById("keranjangBody");
const jumlahItem = document.getElementById("jumlahItem");

const totalBelanja = document.getElementById("totalBelanja");
const diskon = document.getElementById("diskon");
const totalAkhir = document.getElementById("totalAkhir");

const uangBayar = document.getElementById("uangBayar");
const kembalian = document.getElementById("kembalian");

const resetButton = document.getElementById("resetButton");


// ==========================================
// FORMAT RUPIAH
// ==========================================

function formatRupiah(angka) {
    return "Rp " + angka.toLocaleString("id-ID");
}


// ==========================================
// VALIDASI FORM BARANG
// ==========================================

function validasiBarang() {

    let valid = true;

    // Menghapus pesan error sebelumnya
    errorNama.textContent = "";
    errorHarga.textContent = "";
    errorQty.textContent = "";


    // --------------------------------------
    // VALIDASI NAMA BARANG
    // --------------------------------------

    let nama = namaBarang.value.trim();

    if (nama === "") {

        errorNama.textContent = "Nama barang wajib diisi.";
        valid = false;

    } else if (nama.length < 3) {

        errorNama.textContent = "Nama barang minimal 3 karakter.";
        valid = false;
    }


    // --------------------------------------
    // VALIDASI HARGA SATUAN
    // --------------------------------------

    let harga = Number(hargaBarang.value);

    if (hargaBarang.value.trim() === "") {

        errorHarga.textContent = "Harga satuan wajib diisi.";
        valid = false;

    } else if (!Number.isInteger(harga)) {

        errorHarga.textContent = "Harga harus berupa angka bulat.";
        valid = false;

    } else if (harga < 500) {

        errorHarga.textContent = "Harga minimal Rp 500.";
        valid = false;
    }


    // --------------------------------------
    // VALIDASI QTY
    // --------------------------------------

    let qty = Number(qtyBarang.value);

    if (qtyBarang.value.trim() === "") {

        errorQty.textContent = "Jumlah barang wajib diisi.";
        valid = false;

    } else if (!Number.isInteger(qty)) {

        errorQty.textContent = "Jumlah harus berupa angka bulat.";
        valid = false;

    } else if (qty < 1) {

        errorQty.textContent = "Jumlah minimal 1.";
        valid = false;
    }


    return valid;
}


// ==========================================
// TAMBAH BARANG
// ==========================================

formBarang.addEventListener("submit", function(event) {

    // Mencegah halaman refresh
    event.preventDefault();


    // Menjalankan validasi
    if (!validasiBarang()) {
        return;
    }


    // Mengambil data dari input
    let nama = namaBarang.value.trim();
    let harga = Number(hargaBarang.value);
    let qty = Number(qtyBarang.value);


    // Menghitung subtotal
    let subtotal = harga * qty;


    // Membuat object barang
    let barang = {
        nama: nama,
        harga: harga,
        qty: qty,
        subtotal: subtotal
    };


    // Menambahkan barang ke keranjang
    keranjang.push(barang);


    // Menyimpan keranjang ke localStorage
    localStorage.setItem(
        "keranjangKantinCeria",
        JSON.stringify(keranjang)
    );


    // Menampilkan keranjang
    tampilkanKeranjang();


    // Reset form
    formBarang.reset();


    // Menghapus pesan error
    errorNama.textContent = "";
    errorHarga.textContent = "";
    errorQty.textContent = "";
});


// ==========================================
// MENAMPILKAN KERANJANG
// ==========================================

function tampilkanKeranjang() {

    // Mengosongkan tabel
    keranjangBody.innerHTML = "";


    // Jika keranjang kosong
    if (keranjang.length === 0) {

        keranjangBody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center;">
                    Belum ada barang di keranjang.
                </td>
            </tr>
        `;

    } else {

        // For loop untuk menampilkan barang
        for (let i = 0; i < keranjang.length; i++) {

            let barang = keranjang[i];

            // Menghitung ulang subtotal
            barang.subtotal = barang.harga * barang.qty;

            keranjangBody.innerHTML += `
                <tr>
                    <td>${i + 1}</td>

                    <td>${barang.nama}</td>

                    <td>${formatRupiah(barang.harga)}</td>

                    <td>${barang.qty}</td>

                    <td>${formatRupiah(barang.subtotal)}</td>

                    <td>
                        <button
                            class="btn-hapus"
                            onclick="hapusBarang(${i})"
                        >
                            Hapus
                        </button>
                    </td>
                </tr>
            `;
        }
    }


    // Menampilkan jumlah item
    jumlahItem.textContent = keranjang.length + " Item";


    // Menghitung total
    hitungTotal();
}


// ==========================================
// HAPUS BARANG
// ==========================================

function hapusBarang(index) {

    // Menghapus barang berdasarkan index
    keranjang.splice(index, 1);


    // Menyimpan perubahan ke localStorage
    localStorage.setItem(
        "keranjangKantinCeria",
        JSON.stringify(keranjang)
    );


    // Menampilkan ulang keranjang
    tampilkanKeranjang();


    // Menghitung ulang kembalian
    hitungKembalian();
}


// ==========================================
// HITUNG TOTAL BELANJA
// ==========================================

function hitungTotal() {

    let total = 0;


    // Menghitung total semua subtotal
    for (let i = 0; i < keranjang.length; i++) {

        total += keranjang[i].harga * keranjang[i].qty;
    }


    // --------------------------------------
    // DISKON 10%
    // --------------------------------------

    let jumlahDiskon = 0;

    if (total >= 50000) {

        jumlahDiskon = total * 0.10;
    }


    // Menghitung total akhir
    let totalBayar = total - jumlahDiskon;


    // Menampilkan hasil
    totalBelanja.textContent = formatRupiah(total);

    diskon.textContent = formatRupiah(jumlahDiskon);

    totalAkhir.textContent = formatRupiah(totalBayar);
}


// ==========================================
// HITUNG KEMBALIAN
// ==========================================

function hitungKembalian() {

    let total = 0;


    // Menghitung total belanja
    for (let i = 0; i < keranjang.length; i++) {

        total += keranjang[i].harga * keranjang[i].qty;
    }


    // Menghitung diskon
    let jumlahDiskon = 0;

    if (total >= 50000) {

        jumlahDiskon = total * 0.10;
    }


    // Menghitung total akhir
    let totalBayar = total - jumlahDiskon;


    // Mengambil uang bayar
    let bayar = Number(uangBayar.value);


    // Jika belum ada uang bayar
    if (uangBayar.value.trim() === "") {

        kembalian.textContent = "Rp 0";
        kembalian.style.color = "";

        return;
    }


    // Jika uang kurang
    if (bayar < totalBayar) {

        kembalian.textContent = "Uang belum mencukupi";
        kembalian.style.color = "red";

    } else {

        // Menghitung kembalian
        let hasilKembalian = bayar - totalBayar;

        kembalian.textContent = formatRupiah(hasilKembalian);
        kembalian.style.color = "green";
    }
}


// ==========================================
// EVENT UANG BAYAR
// ==========================================

uangBayar.addEventListener("input", function() {

    hitungKembalian();

});


// ==========================================
// TRANSAKSI BARU / RESET
// ==========================================

resetButton.addEventListener("click", function() {

    // Mengosongkan keranjang
    keranjang = [];


    // Menghapus localStorage
    localStorage.removeItem("keranjangKantinCeria");


    // Reset form barang
    formBarang.reset();


    // Reset uang bayar
    uangBayar.value = "";


    // Menghapus pesan error
    errorNama.textContent = "";
    errorHarga.textContent = "";
    errorQty.textContent = "";


    // Menampilkan keranjang kosong
    tampilkanKeranjang();


    // Reset kembalian
    kembalian.textContent = "Rp 0";
    kembalian.style.color = "";
});


// ==========================================
// VALIDASI INPUT HARGA
// ==========================================

hargaBarang.addEventListener("input", function() {

    let harga = Number(hargaBarang.value);

    // Jika harga kurang dari 500
    if (harga < 500 && hargaBarang.value !== "") {

        errorHarga.textContent = "Harga minimal Rp 500.";

    } else {

        errorHarga.textContent = "";
    }
});


// ==========================================
// VALIDASI INPUT QTY
// ==========================================

qtyBarang.addEventListener("input", function() {

    let qty = Number(qtyBarang.value);


    // Jika Qty kurang dari 1
    if (qty < 1 && qtyBarang.value !== "") {

        qtyBarang.value = 1;
    }


    // Jika Qty berupa desimal
    if (!Number.isInteger(qty) && qtyBarang.value !== "") {

        qtyBarang.value = Math.floor(qty);
    }
});


// ==========================================
// LOAD DATA SAAT HALAMAN DIBUKA
// ==========================================

tampilkanKeranjang();