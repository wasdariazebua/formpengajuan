import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Form Pengajuan Data", layout="centered")

st.title("📝 Form Data Pengajuan PT.Mencari Cinta Sejati")
st.markdown("Isi form di bawah ini. Pastikan tidak ada typo sebelum menekan tombol **Generate Text** di bagian paling bawah.")
st.divider()

# --- BAGIAN 1: DATA PENGAJU & MAJIKAN ---
st.subheader("Data Pengaju & Majikan")
col1, col2 = st.columns(2)
with col1:
    nama_pengaju = st.text_input("Nama Pengaju", placeholder="NAMA LENGKAP PENGAJU")
    hp_pengaju = st.text_input("No HP Pengaju", placeholder="+886 / +62 XXXX")
    tgl_lahir = st.text_input("Tanggal Lahir", placeholder="YYYY/MM/DD")
    daerah = st.text_input("Daerah", placeholder="NAMA KOTA / DAERAH TINGGAL")
with col2:
    nama_majikan = st.text_input("Nama Majikan", placeholder="NAMA MAJIKAN (MANDARIN / LATIN)")
    no_paspor = st.text_input("No. Paspor", placeholder="CONTOH: E9012345")
    msk_taiwan = st.text_input("Masuk Taiwan", placeholder="YYYY/MM/DD")

# --- BAGIAN 2: DETAIL PINJAMAN ---
st.subheader("Detail Pinjaman")
col3, col4 = st.columns(2)
with col3:
    pinjaman = st.text_input("Nominal Pinjaman", placeholder="CONTOH: 30 JT")
    perbulan = st.text_input("Angsuran Perbulan", placeholder="CONTOH: 8846 NT")
    mulai_setoran = st.text_input("Mulai Setoran", placeholder="YYYY/MM/DD")
    anak_angsuran = st.text_input("Anak Angsuran", placeholder="YYYY/MM/DD")
with col4:
    bayar = st.text_input("Tenor & Potongan", placeholder="CONTOH: 12 X ( POT DALAM 2 X 8846 NT)")
    keperluan = st.text_input("Keperluan", placeholder="CONTOH: TAMBAHAN RENOV RUMAH")
    pot_pt = st.text_input("Keterangan Potongan PT", placeholder="CONTOH: POT PT 2X 12790 (DIBAYAR MAJIKAN)")

# --- BAGIAN 3: REKENING TUJUAN ---
st.subheader("Rekening Tujuan")
rek_nama = st.text_input("Nama Pemilik Rekening", placeholder="NAMA SESUAI BUKU TABUNGAN")
rek_bank = st.text_input("Nama Bank & Cabang", placeholder="CONTOH: BNI CIKAMPEK KARAWANG")
col5, col6 = st.columns(2)
with col5:
    rek_no = st.text_input("Nomor Rekening", placeholder="CONTOH: 1978770639")
with col6:
    rek_hp = st.text_input("No HP Rekening Tujuan", placeholder="+62 XXXX")

# --- BAGIAN 4: DATA PENJAMIN (DINAMIS) ---
st.subheader("Data Penjamin")
st.caption("Klik 'Tambah' untuk menambah baris, atau 'Hapus' untuk mengurangi baris penjamin.")

# Inisialisasi session state untuk jumlah penjamin
if 'jumlah_penjamin' not in st.session_state:
    st.session_state.jumlah_penjamin = 1

data_penjamin = []

# Looping untuk memunculkan form input sesuai jumlah_penjamin
for i in range(st.session_state.jumlah_penjamin):
    st.markdown(f"**Penjamin {i+1}**")
    p_col1, p_col2, p_col3 = st.columns([2, 1, 2])
    
    with p_col1:
        nama = st.text_input(f"Nama", key=f"nama_{i}", placeholder="NAMA LENGKAP PENJAMIN")
    with p_col2:
        hub = st.text_input(f"Hubungan", key=f"hub_{i}", placeholder="CONTOH: ADIK")
    with p_col3:
        hp = st.text_input(f"No HP", key=f"hp_{i}", placeholder="+62 XXXX")
    
    # Masukkan ke list hanya jika nama sudah diisi
    if nama:
        data_penjamin.append({"nama": nama, "hub": hub, "hp": hp})

# Membuat dua kolom untuk tombol Tambah dan Hapus
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.session_state.jumlah_penjamin < 5:
        if st.button("➕ Tambah Penjamin", use_container_width=True):
            st.session_state.jumlah_penjamin += 1
            st.rerun()

with col_btn2:
    # Tombol hapus hanya muncul jika jumlah penjamin lebih dari 1
    if st.session_state.jumlah_penjamin > 1:
        if st.button("➖ Hapus Penjamin terakhir", use_container_width=True):
            st.session_state.jumlah_penjamin -= 1
            st.rerun()

# --- BAGIAN 5: AGENSI & DOKUMEN ---
st.subheader("Agensi & Dokumen")
col7, col8 = st.columns(2)
with col7:
    nama_agensi = st.text_input("Nama Agensi", placeholder="NAMA PERUSAHAAN AGENSI")
    kode_agensi = st.text_input("Kode Agensi", placeholder="CONTOH: 0669")
    tlp_agensi = st.text_input("No Tlp Agensi", placeholder="CONTOH: 02-23625012")
    tlp_majikan = st.text_input("No Tlp Majikan", placeholder="CONTOH: LINE / NO HP")
with col8:
    alamat_arc = st.text_input("Alamat ARC & Rumah Taiwan", placeholder="CONTOH: SAMA / BEDA")
    cap_merah = st.text_input("Cap Merah", placeholder="CONTOH: ADA / TIDAK")
    print_doc = st.text_input("Print", placeholder="CONTOH: SEVEN")
    kirim_balik = st.text_input("Kirim Balik", placeholder="CONTOH: SEVEN")

# --- BAGIAN 6: MEDIA SOSIAL & PIC ---
st.subheader("Media Sosial & Penanggung Jawab")
link_fb = st.text_input("Link Facebook", placeholder="https://www.facebook.com/...")
link_line = st.text_input("Link Line", placeholder="https://line.me/ti/p/...")
link_tiktok = st.text_input("Link Tiktok", placeholder="https://www.tiktok.com/...")
pic = st.text_input("Penanggung Jawab / Catatan Bawah", placeholder="NAMA PIC / TIKTOK")

st.divider()

# --- BAGIAN 7: GENERATE TEXT ---
# Tombol utama diletakkan di luar form karena kita menggunakan input dinamis di atas
if st.button("✨ Generate Text", type="primary"):
    
    # 1. Menyusun teks penjamin secara otomatis (Semua di-upper)
    teks_penjamin_gabung = ""
    for p in data_penjamin:
        teks_penjamin_gabung += f"{p['nama'].upper()} / {p['hub'].upper()}\n{p['hp'].upper()}\n\n"
    
    # Mencegah tulisan kosong jika user belum mengisi penjamin sama sekali
    if not teks_penjamin_gabung:
        teks_penjamin_gabung = "- \n\n"

    # 2. Memformat seluruh teks sesuai dengan template
    # CATATAN: Semua variabel diberi .upper() KECUALI bagian Link agar link tidak rusak
    hasil_teks = f"""{nama_pengaju.upper()} = {hp_pengaju.upper()}
NAMA MAJIKAN : {nama_majikan.upper()}
NO. PASPOR : {no_paspor.upper()}
TGL LAHIR : {tgl_lahir.upper()}
DAERAH : {daerah.upper()}
MSK TAIWAN : {msk_taiwan.upper()}

PINJAMAN: {pinjaman.upper()}
BAYAR: {bayar.upper()}
PERBULAN : {perbulan.upper()}
MULAI SETORAN:  {mulai_setoran.upper()}
ANAK ANGSURAN : {anak_angsuran.upper()}
KEPERLUAN :  {keperluan.upper()}

REKENING TUJUAN
{rek_nama.upper()}
{rek_bank.upper()}
{rek_no.upper()}
{rek_hp.upper()} 

PENJAMIN
{teks_penjamin_gabung}
AGENSI : {nama_agensi.upper()} = {kode_agensi.upper()}
NO TLP AGENSI :  {tlp_agensi.upper()}
NO TLP MAJIKAN: {tlp_majikan.upper()}

ALAMAT ARC & RUMAH TAIWAN :  {alamat_arc.upper()}
CAP MERAH :  {cap_merah.upper()}
PRINT : {print_doc.upper()}
KIRIM BALIK : {kirim_balik.upper()}

PINJAMAN 
{pot_pt.upper()}


LINK FACEBOOK :  {link_fb}
LINK LINE :  {link_line}
TIKTOK : {link_tiktok}

{pic.upper()}"""

    st.success("Teks berhasil dibuat! Silakan klik ikon 'Copy' di pojok kanan atas kotak di bawah ini:")
    
    # Menampilkan hasil menggunakan st.code agar muncul tombol copy otomatis
    st.code(hasil_teks, language="text")