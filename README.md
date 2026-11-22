# AI Agent Repository

Repository ini menampung beberapa AI Agent yang dikelola sebagai unit independen. Setiap agent memiliki konfigurasi, instruksi, dan skill sendiri di dalam foldernya.

## Prinsip utama

- Setiap AI Agent berada di direktori tersendiri di bawah `agents/`.
- Setiap agent memiliki `agent.json` sebagai konfigurasi individual.
- Agent ditemukan otomatis melalui keberadaan `agent.json` pada folder agent.
- Instruksi agent disimpan sebagai file Markdown yang dikelompokkan berdasarkan kategori.
- `agent.json` mencantumkan file instruksi yang dimuat serta strategi/prioritas pemuatannya.
- Skill hanya dimiliki oleh agent di dalam folder agent tersebut; tidak ada shared-skill repository.
- Skill ditemukan otomatis melalui keberadaan `SKILL.md` di direktori skill.
- Setiap skill menggunakan `skill.json` untuk metadata/konfigurasi dan `SKILL.md` untuk instruksi.
- Folder pendukung skill seperti `references/`, `scripts/`, dan `assets/` bersifat opsional.
- Schema bersama berada di `schemas/` untuk validasi; schema bukan dependency runtime antar-agent.
- Kegagalan satu agent diisolasi dari agent lain, tetapi tetap dapat dicatat dalam laporan validasi repository.
- Setiap agent memiliki versioning independen.

## Struktur repository

```text
ai-agent/
├── README.md
├── agents/
│   └── <agent-id>/
│       ├── agent.json
│       ├── instructions/
│       │   ├── core/
│       │   ├── behavior/
│       │   ├── workflow/
│       │   └── response/
│       └── skills/
│           └── <skill-id>/
│               ├── skill.json
│               ├── SKILL.md
│               ├── references/   # optional
│               ├── scripts/      # optional
│               └── assets/       # optional
└── schemas/
    ├── agent.schema.json
    └── skill.schema.json
```

Direktori dan kategori di atas menunjukkan pola yang direkomendasikan. Tidak semua kategori instruksi atau direktori pendukung skill wajib ada pada setiap agent.

## Agent discovery

Sistem discovery memindai subdirektori langsung di dalam `agents/`. Sebuah direktori dikenali sebagai agent jika memiliki file `agent.json`.

Contoh:

- `agents/research-agent/agent.json` → kandidat agent yang ditemukan.
- Direktori tanpa `agent.json` → bukan agent terdaftar.

Setiap `agent.json` menyimpan metadata, konfigurasi operasional, versi agent, serta daftar file instruksi yang perlu dimuat.

## Instruction organization

Instruksi dikelompokkan berdasarkan tanggung jawab. Kategori default:

| Urutan default | Kategori | Cakupan |
|---:|---|---|
| 1 | `core` | Identitas dan tanggung jawab |
| 2 | `behavior` | Prinsip, perilaku, dan batasan |
| 3 | `workflow` | Prosedur dan alur kerja |
| 4 | `response` | Format dan gaya respons |

Urutan default dapat disesuaikan melalui konfigurasi agent. File instruksi yang dimuat harus tercantum dalam `agent.json`. Detail format konfigurasi dan aturan konflik instruksi masih menunggu spesifikasi lanjutan.

## Skill discovery and structure

Sistem discovery memindai subdirektori di dalam folder `skills/` milik masing-masing agent. Direktori skill dikenali melalui keberadaan `SKILL.md`.

Setiap skill memiliki:

- `skill.json`: metadata dan konfigurasi skill.
- `SKILL.md`: instruksi penggunaan/pelaksanaan skill.
- `references/`, `scripts/`, dan `assets/`: sumber daya modular opsional.

Tidak ada registry skill pusat dan tidak ada pemakaian skill lintas-agent yang ditetapkan dalam arsitektur ini.

## Shared schemas and validation

Direktori `schemas/` menampung schema bersama untuk memvalidasi konfigurasi agent dan skill. Schema berfungsi sebagai standar validasi repository, bukan sebagai hubungan atau dependency runtime antar-agent.

Strategi validasi yang disepakati bersifat hybrid:

- Kesalahan kritis menolak konfigurasi terkait.
- Masalah nonkritis menghasilkan warning.
- Hasil validasi dan error tiap agent dicatat secara individual; kegagalan satu agent tidak menghentikan agent lain.

Daftar field wajib, klasifikasi error/warning, dan schema JSON final belum ditetapkan.

## Versioning

Setiap agent mengelola versinya sendiri melalui `agent.json`. Perubahan pada satu agent tidak mengharuskan perubahan versi agent lain. Format versi dan aturan kenaikan MAJOR/MINOR/PATCH masih menunggu spesifikasi.

## Status spesifikasi

Repository ini sedang dibangun berdasarkan Requirement Draft v1.1. Struktur dan prinsip yang sudah disetujui diterapkan terlebih dahulu. Detail schema, runtime, eksekusi skill, aturan discovery lanjutan, dan mekanisme pengujian akan ditetapkan melalui pengumpulan requirement berikutnya.
