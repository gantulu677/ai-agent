# AI Agent Repository

Repository ini menampung beberapa AI Agent yang dikelola sebagai unit independen. Setiap agent memiliki konfigurasi, instruksi, dan skill sendiri di dalam foldernya.

Seluruh keputusan requirement **R-01 sampai R-50 telah disetujui dan diaudit**. Rincian keputusan final dan hasil audit silang tersedia di [REQUIREMENTS.md](REQUIREMENTS.md).

## Prinsip arsitektur

- Setiap AI Agent berada di direktori tersendiri di bawah `agents/`.
- Setiap agent memiliki `agent.json` sebagai konfigurasi individual; tidak diperlukan central registry.
- Agent ditemukan otomatis melalui keberadaan `agent.json` pada direktori langsung di bawah `agents/`.
- Setiap agent memiliki instruksi dan skill sendiri; tidak ada shared skill atau runtime dependency antar-agent.
- Schema di root repository digunakan untuk validasi bersama, bukan sebagai dependency runtime antar-agent.
- Kegagalan satu agent diisolasi dari agent lain.
- Setiap agent dan setiap skill memiliki versioning independen.
- Agent tidak diwajibkan menjadi repository GitHub terpisah.

## Struktur repository

```text
ai-agent/
├── README.md
├── REQUIREMENTS.md
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

Struktur tersebut merupakan pola. Kategori instruksi tidak wajib seluruhnya ada. Direktori resource skill standar bersifat opsional dan direktori resource tambahan diperbolehkan.

## Agent discovery and configuration

Sistem memindai subdirektori langsung di dalam `agents/`. Direktori dikenali sebagai agent jika memiliki `agent.json`.

Hanya dua field yang wajib pada `agent.json`:

| Field | Ketentuan |
|---|---|
| `id` | Identitas agent; string non-kosong, format lowercase kebab-case, unik di seluruh repository |
| `version` | Versi agent; string non-kosong |

Field lain bersifat opsional. Konfigurasi dapat memuat metadata, pengaturan operasional, urutan kategori instruksi, dan field khusus agent. Field tambahan diperbolehkan tanpa menghilangkan kewajiban field `id` dan `version`.

Setiap agent mengelola versinya secara independen. Format MAJOR.MINOR.PATCH direkomendasikan, tetapi belum menjadi aturan final yang mengikat.

## Instruction discovery and loading

Instruksi disimpan dalam folder kategori di dalam `instructions/`. Discovery dilakukan otomatis secara rekursif dan tidak memerlukan pendaftaran file satu per satu di `agent.json`.

Format instruksi yang didukung:

| Format | Penanganan |
|---|---|
| Markdown (`.md`) | Dibaca sebagai teks; mendukung YAML Frontmatter untuk metadata instruksi |
| TXT (`.txt`) | Dibaca sebagai teks |
| JSON (`.json`) | Diparsing sebagai data terstruktur sebelum digunakan |
| YAML (`.yaml`) | Diparsing sebagai data terstruktur sebelum digunakan |

Kategori default dan urutan pemuatan:

| Urutan | Kategori | Cakupan |
|---:|---|---|
| 1 | `core` | Identitas dan tanggung jawab |
| 2 | `behavior` | Prinsip, perilaku, dan batasan |
| 3 | `workflow` | Prosedur dan alur kerja |
| 4 | `response` | Format dan gaya respons |

Urutan kategori default dapat dioverride melalui konfigurasi `agent.json`. Kategori yang tidak tercantum dalam urutan konfigurasi tidak diabaikan: kategori tersebut tetap dimuat setelah kategori yang diatur dan diurutkan secara alfabetis. Kategori tambahan otomatis ditemukan.

### Instruction file ordering

Pengurutan file dalam kategori menggunakan aturan berikut:

1. Metadata `priority` dalam YAML Frontmatter menjadi override terhadap numeric prefix jika tersedia.
2. Nilai priority yang lebih kecil dimuat lebih dahulu.
3. Jika priority tidak tersedia, numeric prefix pada nama file menjadi fallback.
4. Jika priority sama, numeric prefix digunakan sebagai tie-breaker.
5. Jika priority dan numeric prefix sama atau tidak membedakan urutan, relative file path diurutkan secara alfabetis.
6. File tanpa priority dan tanpa numeric prefix tetap dimuat dan diurutkan berdasarkan relative file path secara alfabetis.
7. File dengan nama sama di lokasi berbeda tetap dimuat sebagai file terpisah.

Contoh metadata priority pada file Markdown:

```yaml
---
priority: 10
---
```

Field `priority` wajib berupa Integer positif mulai dari 1. Angka desimal dan string tidak diperbolehkan. YAML Frontmatter boleh memiliki field tambahan; hanya semantik `priority` yang ditetapkan untuk pengurutan dalam requirement saat ini.

## Skill discovery and structure

Setiap agent memiliki direktori `skills/` sendiri. Folder skill ditemukan pada tingkat langsung di bawah `agents/<agent-id>/skills/`; discovery skill tidak mencari folder skill bersarang secara rekursif.

Sebuah direktori dikenali sebagai skill jika memiliki `skill.json` dan `SKILL.md`. Semua skill di direktori tersebut otomatis menjadi milik agent terkait; tidak diperlukan pendaftaran di `agent.json`.

| File/direktori | Ketentuan |
|---|---|
| `skill.json` | Metadata dan konfigurasi skill; wajib |
| `SKILL.md` | Instruksi skill; wajib |
| `references/` | Resource pendukung opsional |
| `scripts/` | Script pendukung opsional |
| `assets/` | Asset pendukung opsional |
| Folder resource tambahan | Diperbolehkan |

Field wajib dalam `skill.json`:

| Field | Ketentuan |
|---|---|
| `id` | Identitas skill; string non-kosong, lowercase kebab-case, unik dalam agent pemilik |
| `name` | Nama skill; string non-kosong |
| `description` | Deskripsi skill; string non-kosong |
| `version` | Versi skill; string non-kosong |

Field tambahan diperbolehkan. Setiap skill memiliki versi independen dari versi agent dan skill lainnya.

### Skill dependencies

Dependency eksternal diperbolehkan dan harus dideklarasikan di `skill.json`. Dependency dapat berupa package, tool, API, atau resource eksternal. Dependency eksternal tidak boleh menciptakan runtime dependency atau komunikasi antar-agent; batas independensi agent tetap berlaku.

## Validation and failure isolation

Validasi dilakukan secara independen pada setiap agent dan juga pada tingkat repository secara keseluruhan.

Level validasi:

- **Critical** — kesalahan yang menyebabkan agent terkait ditolak/tidak diproses.
- **Warning** — masalah nonkritis yang tetap dilaporkan.
- **Info** — informasi hasil pemeriksaan.

Perilaku dan pelaporan:

- Critical error pada satu agent tidak menghentikan pemrosesan agent lain.
- Agent yang valid tetap dapat diproses.
- Error dicatat per agent dan hasil validasi repository.
- Laporan validasi tersedia dalam format JSON dan Markdown.

Schema JSON di `schemas/` menetapkan validasi dasar field wajib dan tipe data konfigurasi. Aturan validasi operasional lebih lanjut mengikuti [REQUIREMENTS.md](REQUIREMENTS.md).

## Requirement and implementation status

- **Requirement:** R-01 sampai R-50 disetujui dan difinalisasi setelah audit konsistensi.
- **Audit:** tidak ditemukan konflik langsung yang mengharuskan perubahan arsitektur atau penambahan requirement. Klarifikasi audit telah dimasukkan ke R-21, R-28, R-34, R-35, R-37, R-08, dan R-41.
- **Dokumentasi:** README ini dan [REQUIREMENTS.md](REQUIREMENTS.md) mencerminkan keputusan final.
- **Schema baseline:** `schemas/agent.schema.json` dan `schemas/skill.schema.json` tersedia untuk validasi dasar.

**Batas implementasi:** dokumentasi dan schema tidak berarti runtime telah tersedia. Automatic discovery loader, instruction parser/loader, skill loader, runtime execution, dependency resolver, dan validation engine belum dinyatakan selesai atau teruji hanya berdasarkan dokumen ini.

## Python Runtime

Python Runtime Architecture v1.0 is the approved implementation baseline. The current Phase 1–6 implementation, commands, and limitations are documented in [runtime/README.md](runtime/README.md) and [docs/IMPLEMENTATION_STATUS.md](docs/IMPLEMENTATION_STATUS.md).

## Python Runtime Implementation

The approved Python Runtime Architecture v1.0 has been implemented through the six planned phases.
The implementation is in `runtime/src/agent_runtime/`; details and known limitations are documented in
[Runtime README](runtime/README.md) and [Implementation Status](docs/IMPLEMENTATION_STATUS.md).

### Available commands

Install the package and development dependencies:

    python -m pip install -e ".[dev]"

Inspect runtime capabilities and discovered agents:

    agent-runtime info
    agent-runtime discover

Validate the repository and write JSON/Markdown reports:

    agent-runtime --root . validate

Run the test suite:

    python -m pytest -q

### Implementation scope

- **Phase 1:** Python package, project configuration, internal data models, and CLI foundation.
- **Phase 2:** automatic agent/skill/instruction discovery and per-agent/repository validation.
- **Phase 3:** Markdown/TXT/JSON/YAML parsing, category and file ordering, agent loading, and on-demand skill loading.
- **Phase 4:** isolated agent contexts and sessions, async LLM provider protocol, explicit tool registry, and orchestration.
- **Phase 5:** process-local file cache, concurrent independent agent runs, and logging.
- **Phase 6:** unit test suite, GitHub Actions workflow, and implementation documentation.

**Important limitations:** no vendor-specific LLM provider, automatic skill-script execution, dependency installation, or security sandbox is included. The presence of CI configuration does not itself establish that a GitHub Actions run has passed. Requirement baseline R-01 through R-50 remains unchanged.
