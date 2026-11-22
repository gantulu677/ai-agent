# Approved Requirements — AI Agent Repository

Dokumen ini mencatat keputusan requirement yang telah disetujui sampai R-23. Keputusan yang belum ditetapkan secara eksplisit ditandai sebagai belum ditentukan dan tidak boleh dianggap sebagai requirement final.

## Architecture and repository boundaries

| ID | Requirement | Approved decision |
|---|---|---|
| R-01 | Folder tersendiri per agent | Setiap agent memiliki folder sendiri di bawah `agents/`. |
| R-02 | Skill khusus masing-masing agent | Skill dimiliki secara lokal oleh agent; tidak ada shared skill. |
| R-03 | Multiple instruction files | Satu agent dapat memiliki beberapa file instruksi. |
| R-04 | Modular skill structure | Skill mendukung file utama dan resource modular pendukung. |
| R-05 | Konfigurasi individual | Setiap agent memiliki `agent.json`; central registry tidak wajib. |
| R-06 | Shared Skill Repository | Dihapus/tidak digunakan. |
| R-07 | Shared schema | Schema bersama boleh berada di root repository untuk validasi, bukan dependency runtime antar-agent. |
| R-08 | Repository Dependency Boundary | Agent mandiri dalam repository utama; tidak diwajibkan portable sebagai repository GitHub terpisah. |
| R-09 | Automatic Agent Discovery | Sistem memindai subfolder langsung `agents/`; folder dengan `agent.json` dikenali sebagai agent. |
| R-10 | Automatic Skill Discovery | Sistem memindai folder `skills/` milik agent; folder skill dengan `SKILL.md` dikenali sebagai skill. |
| R-11 | Agent Configuration Structure | `agent.json` memuat identitas, versi, dan dapat memuat metadata serta konfigurasi operasional tambahan. |
| R-12 | Skill Configuration Structure | Skill menggunakan `skill.json` untuk metadata/konfigurasi dan `SKILL.md` untuk instruksi; `references/`, `scripts/`, dan `assets/` bersifat opsional. |
| R-13 | Categorized Instruction Structure | Instruksi dikelompokkan berdasarkan kategori. Kategori default yang direkomendasikan: `core/`, `behavior/`, `workflow/`, dan `response/`; tidak semuanya wajib ada. |
| R-14 | Instruction Loading Order | Urutan kategori default: `core` → `behavior` → `workflow` → `response`; dapat disesuaikan melalui `agent.json`. |
| R-15 | Hybrid Configuration Validation | Critical error menolak konfigurasi bermasalah; noncritical issue menghasilkan warning; detail error/warning dapat diketahui. |
| R-16 | Agent Failure Isolation | Kegagalan satu agent tidak memengaruhi agent lain; error dicatat secara individual dalam laporan validasi repository. |
| R-17 | Independent Agent Versioning | Setiap agent memiliki versi sendiri; perubahan agent lain tidak mengharuskan versi agent ini berubah. MAJOR.MINOR.PATCH masih berupa rekomendasi awal. |

## Configuration and discovery rules

| ID | Requirement | Approved decision |
|---|---|---|
| R-18 | Flexible Agent Configuration | Hanya `id` dan `version` yang wajib di `agent.json`; field lain opsional dan dapat disesuaikan. |
| R-19 | Required Skill Metadata | `skill.json` wajib memiliki `id`, `name`, `description`, dan `version`; field tambahan diperbolehkan. |
| R-20 | Skill-to-Agent Assignment | Semua skill di dalam `agents/<agent-id>/skills/` otomatis menjadi milik agent tersebut. Tidak diperlukan registrasi skill di `agent.json`. |
| R-21 | Instruction Discovery and Loading | Semua file Markdown (`.md`) dalam folder kategori instruksi otomatis ditemukan dan dimuat; tidak perlu didaftarkan satu per satu di `agent.json`. |
| R-22 | Instruction File Ordering | Pengurutan file dalam kategori menggunakan pendekatan hybrid: numeric prefix sebagai default dan metadata prioritas sebagai override. |
| R-23 | Instruction Priority Metadata Format | Metadata prioritas instruksi menggunakan YAML frontmatter di bagian atas file Markdown. |

## Implemented baseline

- `README.md` menjelaskan arsitektur, discovery, loading, validasi, dan struktur.
- `schemas/agent.schema.json` mewajibkan `id` dan `version`, serta mengizinkan properti tambahan.
- `schemas/skill.schema.json` mewajibkan `id`, `name`, `description`, dan `version`, serta mengizinkan properti tambahan.

## Details still open

Keputusan berikut belum ditetapkan dan perlu dibahas sebelum dianggap final atau diimplementasikan sebagai aturan operasional:

- Nama field, tipe, rentang/nilai, dan semantik pengurutan metadata prioritas YAML frontmatter.
- Aturan rinci ketika numeric prefix dan metadata prioritas sama-sama tersedia.
- Perilaku untuk file instruksi tanpa numeric prefix.
- Format lengkap field konfigurasi opsional di `agent.json` dan `skill.json`.
- Klasifikasi critical error vs warning, format laporan validasi, serta perilaku validator.
- Aturan versioning MAJOR/MINOR/PATCH yang mengikat.
- Runtime, eksekusi skill, dan mekanisme pengujian.

Dokumen ini adalah catatan keputusan requirement, bukan klaim bahwa runtime/discovery loader/validator telah dibangun atau diuji.
