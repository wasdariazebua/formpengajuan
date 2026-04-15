import streamlit as st
import urllib.parse # Tambahan library untuk API WhatsApp

# --- FUNGSI TAMBAHAN ---
def format_tanggal(teks):
    teks_bersih = teks.replace(" ", "").replace("/", "")
    if len(teks_bersih) == 8 and teks_bersih.isdigit():
        return f"{teks_bersih[:4]}/{teks_bersih[4:6]}/{teks_bersih[6:]}"
    return teks
# -----------------------

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
    tgl_lahir = st.text_input("Tanggal Lahir", placeholder="Ketik angka saja: 20030228")
    daerah = st.text_input("Daerah", placeholder="NAMA KOTA / DAERAH TINGGAL")
with col2:
    nama_majikan = st.text_input("Nama Majikan", placeholder="NAMA MAJIKAN (MANDARIN / LATIN)")
    no_paspor = st.text_input("No. Paspor", placeholder="CONTOH: E9012345")
    msk_taiwan = st.text_input("Masuk Taiwan", placeholder="Ketik angka saja: 20251103")

# --- BAGIAN 2: DETAIL PINJAMAN (DIPERBARUI) ---
st.subheader("Detail Pinjaman")

# Inisialisasi session state untuk jumlah potongan PT jika belum ada
if 'jumlah_potongan' not in st.session_state:
    st.session_state.jumlah_potongan = 1

col3, col4 = st.columns(2)
with col3:
    pinjaman = st.text_input("Nominal Pinjaman Utama", placeholder="CONTOH: 30 JT")
    perbulan = st.text_input("Angsuran Perbulan", placeholder="CONTOH: 8846 NT")
    mulai_setoran = st.text_input("Mulai Setoran", placeholder="Ketik angka saja: 20260514")
    anak_angsuran = st.text_input("Anak Angsuran", placeholder="Ketik angka saja: 20260714")
with col4:
    bayar = st.text_input("Tenor & Potongan", placeholder="CONTOH: 12 X ( POT DALAM 2 X 8846 NT)")
    keperluan = st.text_input("Keperluan", placeholder="CONTOH: TAMBAHAN RENOV RUMAH")

    # Bagian dinamis untuk banyak potongan/pinjaman
    list_pot_pt = []
    for i in range(st.session_state.jumlah_potongan):
        val_pot = st.text_input(f"Keterangan Pinjaman/Potongan {i+1}", key=f"pot_{i}", placeholder="CONTOH: POT PT 2X 12790")
        if val_pot:
            list_pot_pt.append(val_pot)
    
    # Tombol tambah/hapus khusus untuk bagian potongan
    col_pot1, col_pot2 = st.columns(2)
    with col_pot1:
        if st.session_state.jumlah_potongan < 5:
            if st.button("➕ Tambah Baris Pinjaman", key="add_p"):
                st.session_state.jumlah_potongan += 1
                st.rerun()
    with col_pot2:
        if st.session_state.jumlah_potongan > 1:
            if st.button("➖ Hapus Baris Pinjaman", key="del_p"):
                st.session_state.jumlah_potongan -= 1
                st.rerun()

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
    
    # --- FITUR DINAMIS LINK MAPS ---
    if 'jumlah_maps' not in st.session_state:
        st.session_state.jumlah_maps = 1
        
    list_maps = []
    for j in range(st.session_state.jumlah_maps):
        m = st.text_input(f"Link Maps {j+1}", key=f"map_{j}", placeholder="http://maps.google.com/...")
        if m:
            list_maps.append(m)
            
    c_map1, c_map2 = st.columns(2)
    with c_map1:
        if st.session_state.jumlah_maps < 3: # Batas maksimal 3 link maps
            if st.button("➕ Tambah Lokasi", key="add_m", use_container_width=True):
                st.session_state.jumlah_maps += 1
                st.rerun()
    with c_map2:
        if st.session_state.jumlah_maps > 1:
            if st.button("➖ Hapus Lokasi", key="del_m", use_container_width=True):
                st.session_state.jumlah_maps -= 1
                st.rerun()
    # -------------------------------

    cap_merah = st.text_input("Cap Merah", placeholder="CONTOH: ADA / TIDAK")
    print_doc = st.text_input("Print", placeholder="CONTOH: SEVEN")
    kirim_balik = st.text_input("Kirim Balik", placeholder="CONTOH: SEVEN")

# --- BAGIAN 6: MEDIA SOSIAL & PIC ---
st.subheader("Media Sosial & Penanggung Jawab")
link_fb = st.text_input("Link Facebook", placeholder="https://www.facebook.com/...")
link_line = st.text_input("Link Line", placeholder="https://line.me/ti/p/...")
link_tiktok = st.text_input("Link Tiktok", placeholder="https://www.tiktok.com/...")
pic = st.text_input("Penanggung Jawab / Catatan Bawah", placeholder="NAMA PIC / TIKTOK")

# --- BAGIAN 7: TOMBOL GENERATE & KIRIM WA ---
st.divider()

# Inputan nomor WA tujuan di bawah sudah dihapus agar tidak kerja dua kali

btn_generate = st.button("✨ Generate Text & Buat Link WA", type="primary", use_container_width=True)

if btn_generate:
    # 1. Format ulang semua isian tanggal secara otomatis
    tgl_lahir_auto = format_tanggal(tgl_lahir)
    msk_taiwan_auto = format_tanggal(msk_taiwan)
    mulai_setoran_auto = format_tanggal(mulai_setoran)
    anak_angsuran_auto = format_tanggal(anak_angsuran)
    
    # 2. Menyusun teks penjamin
    teks_penjamin_gabung = ""
    for p in data_penjamin:
        teks_penjamin_gabung += f"{p['nama'].upper()} / {p['hub'].upper()}\n{p['hp'].upper()}\n\n"
    
    if not teks_penjamin_gabung:
        teks_penjamin_gabung = "- \n\n"

    # 3. Menyusun list potongan PT
    teks_potongan_gabung = "\n".join([p.upper() for p in list_pot_pt])
    if not teks_potongan_gabung:
        teks_potongan_gabung = "-"

    # 4. Menyusun Link Maps secara otomatis
    # Jika ada lebih dari 1, akan muncul LINK MAPS 1, LINK MAPS 2, dst.
    if len(list_maps) > 1:
        teks_maps_gabung = "\n".join([f"LINK MAPS {idx+1} : {m}" for idx, m in enumerate(list_maps)])
    elif len(list_maps) == 1:
        teks_maps_gabung = f"LINK MAPS : {list_maps[0]}"
    else:
        teks_maps_gabung = "LINK MAPS : -"

    # 5. Memformat seluruh teks
    hasil_teks = f"""{nama_pengaju.upper()} = {hp_pengaju.upper()}
NAMA MAJIKAN : {nama_majikan.upper()}
NO. PASPOR : {no_paspor.upper()}
TGL LAHIR : {tgl_lahir_auto.upper()}
DAERAH : {daerah.upper()}
MSK TAIWAN : {msk_taiwan_auto.upper()}

PINJAMAN: {pinjaman.upper()}
BAYAR: {bayar.upper()}
PERBULAN : {perbulan.upper()}
MULAI SETORAN:  {mulai_setoran_auto.upper()}
ANAK ANGSURAN : {anak_angsuran_auto.upper()}
KEPERLUAN :  {keperluan.upper()}

REKENING TUJUAN
{rek_nama.upper()}
{rek_bank.upper()}
{rek_no.upper()}
{rek_hp.upper()} 

PENJAMIN
{teks_penjamin_gabung}AGENSI : {nama_agensi.upper()} = {kode_agensi.upper()}
NO TLP AGENSI :  {tlp_agensi.upper()}
NO TLP MAJIKAN: {tlp_majikan.upper()}

ALAMAT ARC & RUMAH TAIWAN :  {alamat_arc.upper()}
CAP MERAH :  {cap_merah.upper()}
PRINT : {print_doc.upper()}
KIRIM BALIK : {kirim_balik.upper()}

PINJAMAN 
{teks_potongan_gabung}


LINK FACEBOOK :  {link_fb}
LINK LINE :  {link_line}
{teks_maps_gabung}
LINK TIKTOK : {link_tiktok}

{pic.upper()}"""

    st.success("Teks berhasil dibuat!")
    st.code(hasil_teks, language="text")

    # 5. Logika untuk tombol API WhatsApp mengambil langsung dari hp_pengaju
    if hp_pengaju:
        # Bersihkan spasi, strip, atau tanda plus dari input nomor HP Pengaju di bagian 1
        no_wa_bersih = hp_pengaju.replace("+", "").replace("-", "").replace(" ", "")
        
        # Mengubah teks form menjadi format yang terbaca oleh URL
        teks_encode = urllib.parse.quote(hasil_teks)
        
        # Membuat link API WhatsApp
        link_wa = f"https://wa.me/{no_wa_bersih}?text={teks_encode}"
        
        st.success(f"Link WhatsApp siap dikirim ke {hp_pengaju}!")
        # Memunculkan tombol khusus
        teks_tombol = f"📲 Buka WA & Kirim ke {nama_pengaju.upper() if nama_pengaju else 'Pengaju'}"
        st.link_button(teks_tombol, url=link_wa, type="primary", use_container_width=True)
    else:
        st.warning("💡 Peringatan: Kolom 'No HP Pengaju' di bagian atas masih kosong. Isi nomornya agar tombol kirim otomatis muncul di sini.")
