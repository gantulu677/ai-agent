# AI Agent Repository

Repository ini menampung beberapa AI Agent yang dikelola sebagai unit independen. Setiap agent memiliki konfigurasi, instruksi, dan skill sendiri di dalam foldernya.

Daftar keputusan requirement yang telah disetujui tersedia di [REQUIREMENTS.md](REQUIREMENTS.md).

## Prinsip arsitektur

- Setiap AI Agent berada di direktori tersendiri di bawah `agents/`.
- Setiap agent memiliki `agent.json` sebagai konfigurasi individual.
- Agent ditemukan otomatis melalui keberadaan `agent.json` pada direktori langsung di bawah `agents/`.
- Setiap agent memiliki instruksi dan skill sendiri; tidak ada shared skill, dependency runtime, atau komunikasi antar-agent yang diwajibkan.
- Schema di root repository digunakan untuk validasi bersama, bukan sebagai dependency runtime antar-agent.
- Kegagalan satu agent diisolasi dari agent lain.
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

Struktur di atas merupakan pola. Kategori instruksi dan direktori pendukung skill tidak wajib seluruhnya ada pada setiap agent.

## Agent discovery and configuration

Sistem memindai subdirektori langsung di dalam `agents/`. Direktori dikenali sebagai agent jika memiliki `agent.json`.

Hanya dua field yang wajib pada `agent.json`:

| Field | Ketentuan |
|---|---|
| `id` | Identitas agent; string non-kosong |
| `version` | Versi agent; string non-kosong |

Field lain bersifat opsional dan dapat disesuaikan. Konfigurasi dapat memuat pengaturan operasional dan urutan kategori instruksi. Field tambahan tidak boleh menyebabkan konfigurasi ditolak hanya karena belum dikenal oleh schema.

Setiap agent mengelola versinya secara independen. Perubahan pada agent A tidak mengharuskan perubahan versi agent B. Format versi MAJOR.MINOR.PATCH merupakan rekomendasi awal, bukan aturan final yang telah ditetapkan.

## Instruction discovery and loading

Instruksi disimpan sebagai file Markdown (`.md`) di dalam folder kategori pada `instructions/`. Semua file Markdown dalam folder kategori instruksi ditemukan dan dimuat otomatis; file tidak perlu didaftarkan satu per satu di `agent.json`.

Kategori default dan urutan pemuatan:

| Urutan | Kategori | Cakupan |
|---:|---|---|
| 1 | `core` | Identitas dan tanggung jawab |
| 2 | `behavior` | Prinsip, perilaku, dan batasan |
| 3 | `workflow` | Prosedur dan alur kerja |
| 4 | `response` | Format dan gaya respons |

Urutan kategori default dapat disesuaikan melalui konfigurasi agent.

Di dalam kategori yang sama, urutan file menggunakan pendekatan hybrid:
1. Numeric prefix pada nama file menjadi mekanisme urutan default, misalnya `01-identity.md`, `02-purpose.md`, dan `03-constraints.md`.
2. Metadata prioritas dalam YAML frontmatter dapat menjadi override terhadap urutan default tersebut.

Contoh bentuk frontmatter (ilustratif):

```yaml
---
# metadata prioritas instruksi
---
```

Nama field metadata, tipe/nilai prioritas, aturan pengurutan, dan perilaku untuk file tanpa numeric prefix masih memerlukan spesifikasi lanjutan. File non-Markdown tidak dimuat sebagai instruksi.

## Skill discovery and structure

Setiap agent memiliki direktori `skills/` sendiri. Semua subdirektori skill di dalamnya menjadi milik agent tersebut secara otomatis; tidak diperlukan pendaftaran skill di `agent.json`.

Sebuah direktori dikenali sebagai skill jika memiliki `SKILL.md`. Skill tidak dibagikan lintas-agent.

Setiap skill memiliki:

| File/direktori | Ketentuan |
|---|---|
| `skill.json` | Metadata dan konfigurasi skill |
| `SKILL.md` | Instruksi skill; wajib untuk discovery |
| `references/` | Resource pendukung opsional |
| `scripts/` | Script pendukung opsional |
| `assets/` | Asset pendukung opsional |

Empat field yang wajib dalam `skill.json`:

| Field | Ketentuan |
|---|---|
| `id` | Identitas skill; string non-kosong |
| `name` | Nama skill; string non-kosong |
| `description` | Deskripsi skill; string non-kosong |
| `version` | Versi skill; string non-kosong |

Field tambahan diperbolehkan. Skill memiliki metadata versi sendiri; aturan versioning skill yang lebih rinci belum ditetapkan.

## Validation and failure isolation

Validasi menggunakan pendekatan hybrid:

- Kesalahan kritis menolak konfigurasi yang bermasalah.
- Masalah nonkritis menghasilkan warning.
- Detail error dan warning harus dapat diketahui.
- Hasil validasi dicatat per agent dalam laporan validasi repository.
- Kegagalan satu agent tidak menghentikan atau memengaruhi agent lain.

Schema JSON yang tersedia di `schemas/` menetapkan field wajib dan tipe dasarnya. Kebijakan klasifikasi critical/noncritical, format laporan, dan aturan validasi lanjutan masih memerlukan spesifikasi.

## Requirement status

README ini merangkum keputusan yang telah disetujui sampai **R-23**. Hal-hal yang belum diputuskan tidak dianggap sebagai requirement final. Pengumpulan requirement berikutnya akan memperjelas detail metadata prioritas frontmatter, aturan validasi, runtime, dan mekanisme pengujian.
