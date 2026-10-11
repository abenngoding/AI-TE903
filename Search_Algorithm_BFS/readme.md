# Search Algorithm: Breadth-First Search (BFS)

## 1. Introduction

Program Python ini mencari **jalur terpendek pada graf tidak berbobot**
menggunakan algoritma **Breadth-First Search (BFS)**. BFS menelusuri simpul
secara bertingkat menggunakan antrean FIFO (*First In, First Out*).

Program menerima simpul awal dan simpul tujuan, kemudian menampilkan jalur
yang ditemukan serta jumlah sisinya. Jalur terpendek berarti jalur dengan
jumlah sisi paling sedikit, bukan biaya atau jarak berbobot.

Contoh pencarian dari simpul G menuju D menghasilkan:

```text
G -> C -> A -> B -> D
```

Jumlah sisi yang dilalui adalah **4**. Jika terdapat beberapa jalur sama pendek,
hasil mengikuti urutan tetangga yang diperiksa pada graf.

Kode inti berasal dari **TheAlgorithms/Python**, sedangkan `main.py` dan
README berbahasa Indonesia ini ditambahkan untuk memudahkan penggunaannya.

| File | Fungsi |
| --- | --- |
| `main.py` | Menjalankan demo dan menerima pilihan simpul |
| `breadth_first_search_shortest_path_2.py` | Implementasi BFS asli beserta graf contoh |
| `requirements.txt` | Keterangan dependensi program |
| `readme.md` | Penjelasan dan cara penggunaan |
| `LICENSE.md` | Lisensi MIT dari repository sumber |
| `source_manifest.json` | URL, commit, dan checksum berkas sumber |
| `verification.txt` | Hasil verifikasi program |

## 2. Requirements

- **Python 3.10 atau lebih baru**.
- Library pihak ketiga: **tidak ada**; tidak perlu menjalankan `pip install`.
- Modul bawaan Python yang digunakan:
  - `collections`: menyediakan `deque` untuk antrean BFS.
  - `argparse`: membaca simpul awal dan tujuan dari argumen terminal.
  - `doctest`: menjalankan pengujian contoh pada source code, jika diperlukan.
- Terminal Windows, macOS, atau Linux. VS Code bersifat opsional.

Cek instalasi Python:

```bash
python --version
```

## 3. How to Use

1. Ekstrak `Search_Algorithm_BFS.zip`.
2. Buka terminal di folder `Search_Algorithm_BFS` yang berisi `main.py`.
3. Jalankan program:

   ```bash
   python main.py
   ```

   Secara default, program mencari jalur dari G ke D. Hasilnya:

   ```text
   Search Algorithm: Breadth-First Search (BFS)
   Pencarian: G -> D
   Jalur terpendek: G -> C -> A -> B -> D
   Jumlah sisi: 4
   ```

4. Untuk mengganti simpul awal dan tujuan:

   ```bash
   python main.py --start A --goal F
   ```

   Hasilnya:

   ```text
   Search Algorithm: Breadth-First Search (BFS)
   Pencarian: A -> F
   Jalur terpendek: A -> C -> F
   Jumlah sisi: 2
   ```

Pilihan simpul pada contoh adalah **A, B, C, D, E, F, G**, dengan huruf kapital.
Program menolak pilihan di luar daftar tersebut. Jika simpul awal dan tujuan
sama, jumlah sisi adalah 0.

Untuk menampilkan bantuan:

```bash
python main.py --help
```

Untuk menjalankan file source asli secara langsung:

```bash
python breadth_first_search_shortest_path_2.py
```

Untuk menjalankan enam pengujian contoh bawaan source:

```bash
python -m doctest -v breadth_first_search_shortest_path_2.py
```

Jika `python` tidak dikenali, coba `py` di Windows atau `python3` di macOS/Linux.
Pastikan terminal berada di folder yang benar dan kedua file Python tetap
berada dalam satu folder.

Graf dapat diubah melalui variabel `demo_graph` pada file source. Setiap
simpul yang menjadi tetangga harus memiliki entri sendiri. Daftar tetangga
menentukan arah perjalanan; graf asli tidak sepenuhnya simetris. Contohnya,
E dapat menuju D, tetapi daftar tetangga D hanya berisi B.

Fungsi `bfs_shortest_path` menghasilkan daftar simpul pada jalur, atau `[]`
jika tidak ditemukan. Fungsi `bfs_shortest_path_distance` menghasilkan jumlah
sisi, atau `-1` jika tidak ada jalur. Saat memakai fungsi secara langsung,
pastikan simpul awal valid; peluncur `main.py` sudah memvalidasi pilihan simpul.

## 4. Source / Referensi

- **Repository:** [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python).
- **File source:** [breadth_first_search_shortest_path_2.py](https://github.com/TheAlgorithms/Python/blob/b0be30443393b019c469684554a3c8748ffeacbe/graphs/breadth_first_search_shortest_path_2.py).
- **Commit:** `b0be30443393b019c469684554a3c8748ffeacbe`.
- **Lisensi:** MIT, disertakan pada file `LICENSE.md`.
- **Atribusi sumber:** TheAlgorithms and contributors.

Implementasi BFS dan lisensi asli disertakan tanpa perubahan. Peluncur
`main.py` serta dokumentasi pendamping dibuat untuk paket pembelajaran ini.
Cantumkan repository sumber saat menggunakan kode dalam tugas.
