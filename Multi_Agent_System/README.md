# Multi-Agent System Sederhana dengan Python

Proyek pemula yang menunjukkan cara beberapa agen bekerja berurutan untuk menangani satu topik.

## Agen yang tersedia

1. **ResearchAgent** — menghasilkan poin awal untuk topik.
2. **AnalysisAgent** — menyusun analisis berdasarkan topik dan hasil agen pertama.
3. **SummaryAgent** — membuat ringkasan dan langkah lanjutan.

## Persyaratan

- Python 3.9 atau lebih baru
- Tidak perlu menginstal library tambahan

## Cara menjalankan

Buka terminal di folder proyek, lalu jalankan:

```bash
python main.py
```

Jika perintah `python` tidak tersedia di Windows, coba:

```bash
py main.py
```

Masukkan topik saat diminta. Jika dikosongkan, program memakai topik contoh `Otomasi industri berbasis AI`.

## Catatan

Ini adalah **demo alur multi-agent sederhana** berbasis aturan Python. Agen-agen belum memakai LLM, API, atau pencarian internet. Kamu dapat mengembangkan tiap metode `run()` agar memakai model AI atau sumber data yang sesuai.

## Struktur folder

```text
multi_agent_system_python/
├── main.py
└── README.md
```
