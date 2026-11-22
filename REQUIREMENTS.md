# Approved Requirements — AI Agent Repository

Dokumen ini merupakan sumber acuan keputusan requirement yang telah disetujui untuk repository AI Agent. Seluruh R-01 sampai R-50 telah disetujui dan diaudit konsistensinya. Hasil klarifikasi audit dimasukkan ke requirement terkait, bukan sebagai requirement baru.

Status dokumen: **Finalized baseline R-01–R-50**.

## 1. Architecture and repository boundaries

| ID | Requirement | Keputusan final |
|---|---|---|
| R-01 | Folder tersendiri per agent | Setiap agent memiliki folder sendiri di bawah `agents/`. |
| R-02 | Skill khusus masing-masing agent | Skill dimiliki secara lokal oleh agent tersebut; tidak ada shared skill. |
| R-03 | Multiple instruction files | Satu agent dapat memiliki beberapa file instruksi. |
| R-04 | Modular skill structure | Skill mendukung file utama dan resource modular pendukung. |
| R-05 | Konfigurasi individual | Setiap agent memiliki `agent.json`; central registry tidak wajib. |
| R-06 | Shared Skill Repository | Tidak digunakan. |
| R-07 | Shared schema | Schema bersama boleh berada di root repository untuk validasi, bukan dependency runtime antar-agent. |
| R-08 | Repository Dependency Boundary | Agent mandiri dalam repository utama dan tidak diwajibkan portable sebagai repository GitHub terpisah. |
| R-09 | Automatic Agent Discovery | Sistem memindai subfolder langsung `agents/`; folder dengan `agent.json` dikenali sebagai agent. |
| R-10 | Automatic Skill Discovery | Sistem memindai folder `skills/` milik agent; folder skill dengan `SKILL.md` dikenali sebagai skill. |

## 2. Agent and skill configuration

| ID | Requirement | Keputusan final |
|---|---|---|
| R-11 | Agent Configuration Structure | `agent.json` memuat identitas, versi, metadata, dan konfigurasi operasional agent. Daftar file instruksi tidak perlu didaftarkan karena discovery dilakukan otomatis berdasarkan R-21. |
| R-12 | Skill Configuration Structure | `skill.json` memuat metadata/konfigurasi dan `SKILL.md` memuat instruksi skill. `references/`, `scripts/`, dan `assets/` bersifat opsional; folder resource tambahan juga diperbolehkan berdasarkan R-40. |
| R-13 | Categorized Instruction Structure | Instruksi dikelompokkan berdasarkan kategori. Kategori default: `core/`, `behavior/`, `workflow/`, dan `response/`; tidak semuanya wajib ada. Kategori tambahan diperbolehkan. |
| R-14 | Instruction Loading Order | Urutan default kategori: `core` → `behavior` → `workflow` → `response`. Urutan dapat dioverride melalui `agent.json`; kategori yang tidak tercantum tetap dimuat setelah kategori yang diatur, mengikuti aturan R-34 dan R-35. |
| R-15 | Hybrid Configuration Validation | Critical error menolak konfigurasi/agent yang bermasalah; noncritical issue menghasilkan warning. Detail error dan warning harus tersedia. |
| R-16 | Agent Failure Isolation | Kegagalan satu agent tidak memengaruhi agent lain. Error dicatat secara individual dalam laporan validasi repository. |
| R-17 | Independent Agent Versioning | Setiap agent memiliki versi sendiri; perubahan pada agent lain tidak mengharuskan versi agent ini berubah. MAJOR.MINOR.PATCH merupakan format yang direkomendasikan, bukan aturan final yang mengikat. |
| R-18 | Flexible Agent Configuration | Hanya `id` dan `version` yang wajib dalam `agent.json`; field lain opsional dan dapat disesuaikan. |
| R-19 | Required Skill Metadata | `skill.json` wajib memiliki `id`, `name`, `description`, dan `version`. Field tambahan diperbolehkan. |
| R-20 | Skill-to-Agent Assignment | Semua skill di dalam `agents/<agent-id>/skills/` otomatis menjadi milik agent tersebut. Registrasi skill di `agent.json` tidak diperlukan. |

## 3. Instruction discovery, formats, and ordering

| ID | Requirement | Keputusan final |
|---|---|---|
| R-21 | Automatic Instruction Loading | File instruksi ditemukan otomatis tanpa registrasi satu per satu di `agent.json`. Bersama R-37, discovery berlaku untuk format `.md`, `.json`, `.yaml`, dan `.txt` di dalam struktur kategori instruksi. |
| R-22 | Hybrid Instruction Ordering | Numeric prefix pada nama file menjadi urutan default; metadata `priority` menjadi override jika tersedia. |
| R-23 | Instruction Priority Metadata Format | Metadata prioritas menggunakan YAML Frontmatter di bagian atas file Markdown. |
| R-24 | Instruction Priority Field | Nama field metadata prioritas adalah `priority`. |
| R-25 | Priority Value Type | Nilai `priority` harus bertipe Integer. Angka desimal dan string tidak diperbolehkan. |
| R-26 | Priority Ordering Direction | Nilai priority yang lebih kecil dimuat lebih dahulu. |
| R-27 | Priority and Numeric Prefix Relationship | Priority menjadi override terhadap numeric prefix jika tersedia. Numeric prefix menjadi fallback ketika priority tidak tersedia. |
| R-28 | Equal Priority Tie-breaker | File dengan nilai priority yang sama diurutkan berdasarkan numeric prefix. Jika numeric prefix juga sama atau tidak membedakan urutan, gunakan urutan alfabetis berdasarkan relative file path sebagai tie-breaker terakhir. |
| R-29 | File Without Priority | File tanpa metadata priority tetap dimuat dan menggunakan numeric prefix sebagai fallback. |
| R-30 | File Without Priority and Numeric Prefix | File yang tidak memiliki priority maupun numeric prefix tetap dimuat dan diurutkan secara alfabetis berdasarkan relative file path. |
| R-31 | Priority Value Range | Priority menggunakan integer positif mulai dari 1. |
| R-32 | Frontmatter Metadata Extensibility | YAML Frontmatter mendukung field `priority`; field metadata tambahan juga diperbolehkan. Hanya `priority` yang memiliki semantik pengurutan yang ditetapkan dalam requirement ini. |
| R-33 | Instruction Discovery Depth | Pencarian file instruksi dilakukan secara rekursif pada seluruh subfolder kategori instruksi. |
| R-34 | Unknown Instruction Categories | Kategori instruksi tambahan/tidak dikenal ditemukan dan dimuat otomatis setelah kategori default/yang diatur. Kategori tambahan diurutkan secara alfabetis. |
| R-35 | Instruction Category Ordering | Urutan kategori menggunakan pendekatan hybrid: urutan default tetap tersedia dan dapat dioverride melalui konfigurasi `agent.json`. Kategori yang tidak tercantum dalam urutan konfigurasi tidak diabaikan; kategori tersebut tetap dimuat setelah kategori yang diatur dan diurutkan secara alfabetis. |
| R-36 | Duplicate Instruction Files | File instruksi dengan nama yang sama tetap dimuat sesuai lokasinya masing-masing; nama file yang sama tidak dengan sendirinya menyebabkan salah satunya diabaikan. |
| R-37 | Instruction File Formats and Parsing | Format instruksi yang didukung adalah Markdown (`.md`), JSON (`.json`), YAML (`.yaml`), dan TXT (`.txt`). Semua format tersebut ditemukan otomatis sesuai R-21. Markdown dan TXT dibaca sebagai teks; JSON dan YAML diparsing sebagai data terstruktur sebelum digunakan. YAML Frontmatter untuk metadata `priority` tetap berlaku pada file Markdown. |

### Instruction ordering interpretation

Aturan di atas menetapkan:
1. Kategori diproses menurut urutan default atau urutan override dari `agent.json`.
2. Kategori yang tidak tercantum tetap diproses setelah kategori yang diatur, dalam urutan alfabetis.
3. Dalam satu kategori, priority yang tersedia menjadi override terhadap numeric prefix; nilai priority lebih kecil didahulukan.
4. File tanpa priority menggunakan numeric prefix sebagai fallback.
5. Jika priority sama, numeric prefix menjadi tie-breaker; jika masih sama/tidak tersedia, relative file path alfabetis menjadi tie-breaker.
6. File tanpa priority dan numeric prefix tetap dimuat dan diurutkan berdasarkan relative file path alfabetis.
7. File dengan nama sama di lokasi berbeda tetap diperlakukan sebagai file terpisah.

## 4. Skill structure, discovery, and dependencies

| ID | Requirement | Keputusan final |
|---|---|---|
| R-38 | Skill Discovery Depth | Discovery skill dilakukan pada folder langsung di dalam `agents/<agent-id>/skills/`; tidak dilakukan secara rekursif untuk mencari skill bersarang. |
| R-39 | Minimum Skill Structure | Setiap skill wajib memiliki `skill.json` dan `SKILL.md`. |
| R-40 | Skill Resources | Folder `references/`, `scripts/`, dan `assets/` bersifat opsional. Folder resource tambahan diperbolehkan. |
| R-41 | Skill Dependencies | Dependency eksternal diperbolehkan dan harus dideklarasikan dalam `skill.json`. Dependency dapat berupa package, tool, API, atau resource eksternal. Dependency eksternal tidak boleh menciptakan mekanisme ketergantungan runtime atau komunikasi antar-agent; batas independensi R-08 tetap berlaku. |
| R-42 | Skill Versioning | Setiap skill memiliki versi independen dari versi agent dan skill lain. |

## 5. Identity and extensible configuration

| ID | Requirement | Keputusan final |
|---|---|---|
| R-43 | Agent and Skill ID Format | Agent ID dan Skill ID menggunakan lowercase kebab-case. |
| R-44 | ID Uniqueness | Agent ID harus unik di seluruh repository. Skill ID harus unik di dalam agent pemiliknya; skill dari agent berbeda boleh menggunakan ID yang sama. |
| R-45 | Additional Agent Configuration Fields | Field standar agent dapat digunakan sebagai konvensi, tetapi field khusus agent juga diperbolehkan. Field wajib R-18 tetap harus tersedia. |
| R-46 | Additional Skill Configuration Fields | Field standar skill dapat digunakan sebagai konvensi, tetapi field khusus skill juga diperbolehkan. Field wajib R-19 tetap harus tersedia. |

## 6. Validation and error handling

| ID | Requirement | Keputusan final |
|---|---|---|
| R-47 | Validation Severity Levels | Validasi memiliki tiga level: Critical, Warning, dan Info. |
| R-48 | Cross-Agent Validation | Validasi dilakukan secara independen per agent dan dilengkapi validasi pada tingkat repository secara keseluruhan. |
| R-49 | Validation Report Formats | Laporan validasi tersedia dalam format JSON dan Markdown. |
| R-50 | Critical Error Behavior | Agent yang mengalami critical error ditolak/tidak diproses, sementara agent lain yang valid tetap dapat diproses. Kegagalan satu agent tidak menghentikan seluruh repository. |

## 7. Audit consistency result

Audit silang R-01 sampai R-50 telah diselesaikan dan dikonfirmasi. Tidak ditemukan konflik langsung yang mengharuskan perubahan arsitektur atau penambahan requirement baru. Klarifikasi berikut dimasukkan ke requirement yang sudah ada:

| Requirement terkait | Hasil klarifikasi audit |
|---|---|
| R-28 | Jika priority dan numeric prefix sama, relative file path alfabetis menjadi tie-breaker terakhir. |
| R-21 + R-37 | Automatic discovery berlaku untuk seluruh format instruksi yang disetujui: Markdown, JSON, YAML, dan TXT. |
| R-37 | Markdown/TXT dibaca sebagai teks; JSON/YAML diparsing sebagai data terstruktur. |
| R-34 + R-35 | Kategori yang tidak tercantum dalam urutan konfigurasi tetap dimuat setelah kategori yang diatur dan diurutkan alfabetis. |
| R-08 + R-41 | Dependency eksternal skill diperbolehkan, tetapi tidak boleh menciptakan runtime dependency atau komunikasi antar-agent. |

### Kesimpulan audit

- Seluruh R-01 sampai R-50 berstatus **disetujui**.
- Hasil klarifikasi audit merupakan penyempurnaan requirement yang sudah ada, bukan requirement baru.
- Tidak ada requirement tambahan di luar rentang R-01 sampai R-50.
- Tidak ada perubahan terhadap prinsip independent agent architecture.
- Dokumen ini menjadi baseline requirement final untuk tahap desain/implementasi berikutnya.

## 8. Implementation status and boundaries

Dokumen requirement ini tidak menyatakan bahwa seluruh runtime telah dibangun.

Baseline repository yang telah dibuat sebelumnya:
- `README.md` sebagai dokumentasi repository.
- `REQUIREMENTS.md` sebagai catatan keputusan requirement.
- `schemas/agent.schema.json` untuk validasi dasar konfigurasi agent.
- `schemas/skill.schema.json` untuk validasi dasar konfigurasi skill.
- `agents/` sebagai lokasi agent.

Automatic discovery loader, instruction parser/loader, skill loader, runtime execution, dependency resolver, dan validation engine belum dinyatakan selesai atau teruji hanya berdasarkan dokumentasi dan schema yang ada.
