# KONSEP JARINGAN
## Tugas 7 — Essay: Bagaimana Sebuah Paket Menemukan Jalannya

**DOSEN:**  
Dr. Ferry Astika Saputra, ST, M.Sc. (197708232001121002)

**PENYUSUN:**  
Prayogo Adhi Satrio (3125600043)

**PROGRAM STUDI SARJANA TERAPAN TEKNIK INFORMATIKA**  
**POLITEKNIK ELEKTRONIKA NEGERI SURABAYA**

---

Essay ini merujuk ke kursus **APNIC Academy — Routing Fundamentals Course** (<https://academy.apnic.net/en/course/routing-fundamentals-course>).

### 1. Routing: keputusan kecil yang diulang jutaan kali

Ketika kita membuka sebuah situs web dari laptop di kampus, paket data kita tidak tahu jalan menuju server tujuan. Yang ia bawa hanyalah **alamat IP tujuan**. Setiap router yang dilewati paket harus menjawab satu pertanyaan sederhana: *"Ke interface mana paket ini harus saya teruskan?"* Proses memilih jalan itulah yang disebut **routing**.

Routing sebenarnya terdiri dari dua pekerjaan yang berbeda. Pertama, router harus **belajar** jaringan mana saja yang ada dan lewat mana jaringan itu bisa dicapai. Hasil belajar ini disimpan di **Routing Information Base (RIB)**, yaitu routing table yang kita lihat dengan perintah `show ip route`. Kedua, router harus **meneruskan** (*forwarding*) setiap paket secepat mungkin. Untuk itu, rute terbaik dari RIB disalin ke **Forwarding Information Base (FIB)**, tabel yang dioptimalkan untuk pencarian cepat dan pada router besar diproses langsung oleh hardware. Pemisahan ini penting: RIB boleh "berpikir" lambat dan teliti, sedangkan FIB harus bekerja dalam hitungan nanodetik untuk setiap paket.

### 2. Longest prefix match: aturan yang paling spesifik menang

Sering kali alamat tujuan cocok dengan lebih dari satu entri di tabel. Router menyelesaikannya dengan aturan **longest prefix match**: entri dengan prefix terpanjang (paling spesifik) yang dipilih. Contoh routing table berikut:

| Prefix | Next hop |
| :--- | :--- |
| `10.1.0.0/16` | Router A |
| `10.1.1.0/24` | Router B |
| `0.0.0.0/0` | Router C (default route) |

| Tujuan paket | Entri yang cocok | Dipilih | Alasan |
| :--- | :--- | :--- | :--- |
| `10.1.1.20` | /16, /24, /0 | **Router B** | /24 paling panjang |
| `10.1.2.5` | /16, /0 | **Router A** | /16 lebih panjang dari /0 |
| `8.8.8.8` | /0 saja | **Router C** | Hanya default route yang cocok |

Aturan ini berhubungan langsung dengan Tugas 6 (VLSM): karena subnet bisa berukuran berbeda-beda, router harus selalu memilih prefix yang paling tepat.

### 3. Tiga sumber rute dan cara router memilih di antaranya

Router mengenal jaringan dari tiga sumber:

1. **Connected route** — jaringan yang menempel langsung pada interface yang aktif dan memiliki alamat IP. Rute ini muncul otomatis tanpa konfigurasi.
2. **Static route** — rute yang diketik manual oleh administrator. Sederhana, tidak membebani CPU, tetapi tidak bisa menyesuaikan diri bila jaringan berubah.
3. **Dynamic route** — rute yang dipelajari lewat **routing protocol** (OSPF, IS-IS, BGP, dan lainnya), di mana router saling bertukar informasi dan bereaksi sendiri saat ada link yang putus.

Bila prefix yang sama dipelajari dari dua sumber berbeda, router memakai **Administrative Distance (AD)**, yaitu ukuran "seberapa dipercaya" suatu sumber. Nilai lebih kecil lebih dipercaya. Nilai bawaan Cisco IOS (MikroTik RouterOS memakai nilai yang sama; Juniper memakai istilah *preference* dengan angka berbeda):

| Sumber rute | AD (Cisco) |
| :--- | ---: |
| Connected | 0 |
| Static | 1 |
| eBGP | 20 |
| OSPF | 110 |
| IS-IS | 115 |
| iBGP | 200 |

Perlu dibedakan: **AD** membandingkan rute dari *protokol yang berbeda*, sedangkan **metric** (misalnya *cost* pada OSPF) membandingkan beberapa jalur dari *protokol yang sama*.

### 4. Static route bukan sekadar cara "manual"

Modul 2 kursus APNIC menunjukkan bahwa static route punya beberapa pola penggunaan yang sangat berguna di jaringan nyata:

- **Default route** (`0.0.0.0/0` atau `::/0`) — "jika tidak tahu, kirim ke sini". Router kantor kecil atau jaringan kampus cukup memiliki satu default route ke ISP, tanpa perlu menyimpan seluruh tabel Internet.
- **Black hole route** — rute yang sengaja membuang paket (di Cisco diarahkan ke interface `Null0`). Gunanya mencegah *routing loop* untuk blok alamat yang belum dipakai, dan menjadi "jangkar" agar sebuah prefix agregat bisa diumumkan lewat BGP.
- **Floating static route** — static route cadangan yang diberi AD lebih tinggi daripada rute utama. Selama link utama hidup, rute ini "mengambang" dan tidak dipakai; begitu rute utama hilang, rute cadangan otomatis masuk ke tabel.
- **ECMP (Equal-Cost Multi-Path)** — beberapa rute ke tujuan yang sama dengan nilai sama, sehingga trafik dibagi ke beberapa link sekaligus untuk menambah kapasitas dan redundansi.

Contoh pada Cisco IOS (alamat memakai blok dokumentasi RFC 5737):

```
! Default route utama ke ISP-1
ip route 0.0.0.0 0.0.0.0 203.0.113.1
! Floating static: cadangan ke ISP-2, AD 200 sehingga hanya dipakai bila ISP-1 putus
ip route 0.0.0.0 0.0.0.0 198.51.100.1 200
! Black hole untuk blok agregat yang dimiliki
ip route 192.0.2.0 255.255.255.0 Null0
```

Kelemahan static route baru terasa ketika jaringan membesar. Dengan puluhan router, setiap perubahan topologi berarti mengubah konfigurasi di banyak tempat. Di sinilah routing protocol dinamis dibutuhkan.

### 5. OSPF: setiap router memegang peta yang sama

**OSPF (Open Shortest Path First)** adalah routing protocol **link-state** yang dipakai *di dalam* satu jaringan organisasi (disebut **IGP**, *Interior Gateway Protocol*). Cara kerjanya bisa dibayangkan seperti semua router memegang salinan peta yang identik:

1. **Menemukan tetangga.** Router mengirim paket *Hello* (bawaan setiap 10 detik pada link Ethernet) ke alamat multicast `224.0.0.5`. Router yang parameternya cocok menjadi *neighbor*.
2. **Membangun adjacency.** Tetangga melalui beberapa tahap (Down → Init → 2-Way → ExStart → Exchange → Loading → **Full**) sampai database mereka sinkron. Pada segmen broadcast seperti Ethernet dipilih **DR/BDR** agar tidak semua router harus bertukar data dengan semua router lain.
3. **Membanjiri informasi (flooding).** Setiap router menyebarkan **LSA (Link-State Advertisement)** yang menjelaskan link-link miliknya. Hasilnya, semua router di satu area memiliki **LSDB** (*link-state database*) yang sama.
4. **Menghitung jalur.** Setiap router menjalankan algoritma **Dijkstra (SPF)** atas LSDB tersebut dan menjadikan dirinya akar pohon jalur terpendek. Jalur dengan total **cost** terkecil masuk ke routing table. Di Cisco, cost dihitung sebagai *reference bandwidth* (bawaan 100 Mbps) dibagi bandwidth interface.

Agar tetap skalabel, OSPF membagi jaringan menjadi **area**. **Area 0 (backbone)** wajib ada dan semua area lain harus terhubung ke sana. Router di dalam satu area disebut *internal router*, router yang menghubungkan area lain ke area 0 disebut **ABR** (*Area Border Router*), dan router yang memasukkan rute dari luar OSPF disebut **ASBR**. OSPFv2 (RFC 2328) menangani IPv4, sedangkan IPv6 membutuhkan **OSPFv3** (RFC 5340) yang berjalan sebagai proses terpisah.

```
router ospf 1
 router-id 10.0.0.1
 network 10.0.0.1 0.0.0.0 area 0
 network 10.252.108.208 0.0.0.3 area 0
 passive-interface GigabitEthernet0/0
```

### 6. IS-IS: saudara OSPF yang disukai operator besar

**IS-IS (Intermediate System to Intermediate System)** juga protokol link-state yang memakai algoritma Dijkstra, sehingga hasilnya mirip OSPF. Perbedaannya terletak pada sejarah dan desainnya. IS-IS awalnya dibuat oleh ISO (ISO/IEC 10589) untuk protokol OSI, lalu diperluas untuk IP melalui RFC 1195. Konsekuensinya:

- IS-IS **berjalan langsung di atas layer 2**, bukan di atas IP. Ia lebih sulit diserang dari jarak jauh dan tidak bergantung pada pengalamatan IP untuk membentuk tetangga.
- Satu proses IS-IS bisa membawa **IPv4 dan IPv6 sekaligus** (dukungan IPv6 ditambahkan sebagai TLV baru, RFC 5308). Pada OSPF, IPv4 dan IPv6 membutuhkan dua protokol terpisah.
- Hierarkinya memakai **level**: router **Level 1** menangani routing di dalam area, router **Level 2** membentuk backbone antar-area, dan router **L1/L2** menjadi penghubung. Batas area IS-IS berada *pada link*, sedangkan pada OSPF batas area berada *di dalam router* (ABR).
- Setiap router diidentifikasi dengan alamat **NET (Network Entity Title)**, misalnya `49.0001.0100.0000.0001.00`:

| Bagian | Nilai | Arti |
| :--- | :--- | :--- |
| AFI | `49` | Alamat privat (setara dengan IP privat) |
| Area ID | `0001` | Nomor area |
| System ID | `0100.0000.0001` | 6 byte unik per router, sering diturunkan dari loopback `10.0.0.1` |
| NSEL | `00` | Selalu 00 untuk router |

Karena stabil, sederhana untuk dikembangkan, dan menangani dua keluarga alamat dalam satu proses, IS-IS banyak dipakai sebagai IGP oleh ISP besar. Catatan praktis: Cisco Packet Tracer tidak mendukung IS-IS, sehingga praktiknya memerlukan GNS3, EVE-NG, atau router MikroTik/Juniper.

### 7. BGP: protokol yang menyatukan Internet

OSPF dan IS-IS bekerja di dalam satu organisasi. Internet sendiri tersusun dari puluhan ribu jaringan independen yang masing-masing disebut **Autonomous System (AS)** dan memiliki nomor unik (ASN) yang dibagikan oleh RIR seperti APNIC. Protokol yang menghubungkan AS-AS tersebut adalah **BGP (Border Gateway Protocol)**, versi 4 (RFC 4271).

BGP bekerja sangat berbeda dari protokol link-state:

- BGP adalah protokol **path-vector**. Ia tidak menyebarkan peta lengkap, melainkan mengumumkan prefix beserta **AS_PATH**, yaitu daftar AS yang dilewati. Bila sebuah router melihat ASN miliknya sendiri di AS_PATH, rute itu ditolak, dan dengan cara ini loop antar-AS dicegah.
- BGP berjalan di atas **TCP port 179**. Tetangga (*peer*) harus dikonfigurasi secara manual, tidak ditemukan otomatis seperti pada OSPF.
- Sesi melewati status Idle → Connect → Active → OpenSent → OpenConfirm → **Established**, memakai pesan OPEN, UPDATE, KEEPALIVE, dan NOTIFICATION.
- Pemilihan rute terbaik tidak hanya soal jarak, melainkan **kebijakan (policy)** melalui atribut seperti LOCAL_PREF, AS_PATH, MED, dan NEXT_HOP. Ini memungkinkan ISP memilih jalur berdasarkan bisnis, misalnya lebih memilih link pelanggan daripada link transit yang berbayar.

BGP memiliki dua bentuk:

| | **eBGP** | **iBGP** |
| :--- | :--- | :--- |
| Antara | Router di AS yang **berbeda** | Router di AS yang **sama** |
| AD (Cisco) | 20 | 200 |
| Next hop | Diubah ke alamat router pengirim | Dibiarkan (sering perlu `next-hop-self`) |
| Aturan khusus | Tolak rute bila ASN sendiri ada di AS_PATH | Rute dari iBGP peer tidak diteruskan ke iBGP peer lain, sehingga perlu *full mesh* atau *route reflector* |

Contoh eBGP sederhana antara kampus (AS 64500) dan ISP (AS 64501), memakai ASN dokumentasi RFC 5398:

```
router bgp 64500
 bgp router-id 10.0.0.1
 neighbor 203.0.113.1 remote-as 64501
 address-family ipv4 unicast
  neighbor 203.0.113.1 activate
  network 192.0.2.0 mask 255.255.255.0
```

Perintah `network` hanya mengumumkan prefix bila prefix tersebut **benar-benar ada** di routing table. Itulah alasan black hole route `192.0.2.0/24 → Null0` di bagian 4 sering dipasangkan dengan BGP.

Skala BGP sangat besar. Menurut laporan tahunan APNIC, pada Januari 2026 tabel routing global sudah berisi sekitar **1,05 juta prefix IPv4** dan **241.800 prefix IPv6**, dengan pertumbuhan yang mulai melambat.

### 8. Peran masing-masing protokol dalam satu jaringan

Pelajaran terpenting dari kursus ini, menurut saya, adalah bahwa protokol-protokol tersebut **tidak saling bersaing, melainkan berbagi tugas**:

| Lapisan tugas | Protokol | Apa yang dibawa |
| :--- | :--- | :--- |
| Jaringan kecil / tepi | Static & default route | Jalur keluar ke ISP, rute cadangan, black hole |
| Di dalam satu AS | IGP: **OSPF atau IS-IS** | Alamat infrastruktur: loopback router dan link antar-router. Dibuat kecil agar konvergensi cepat |
| Antar-AS dan prefix pelanggan | **BGP** (iBGP di dalam, eBGP ke luar) | Prefix pelanggan dan tabel Internet. BGP mencari *next hop*-nya lewat IGP |

Pola desainnya adalah: **IGP menjawab "bagaimana mencapai router lain di jaringan saya", sedangkan BGP menjawab "jaringan mana yang ada di Internet dan lewat router mana"**. Dengan demikian, routing table IGP tetap kecil dan stabil, sementara jutaan prefix Internet ditangani oleh BGP yang memang dirancang untuk skala tersebut.

### 9. Perintah verifikasi di tiga vendor

Kursus APNIC menyajikan contoh di tiga sistem operasi router. Perintah pengecekan dasarnya:

| Tujuan | Cisco IOS | Juniper Junos OS | MikroTik RouterOS v7 |
| :--- | :--- | :--- | :--- |
| Lihat routing table | `show ip route` | `show route` | `/ip route print` |
| Tetangga OSPF | `show ip ospf neighbor` | `show ospf neighbor` | `/routing ospf neighbor print` |
| Tetangga IS-IS | `show isis neighbors` | `show isis adjacency` | `/routing isis neighbor print` |
| Sesi BGP | `show ip bgp summary` | `show bgp summary` | `/routing bgp session print` |

### 10. Penutup

Routing terlihat rumit karena banyak istilahnya, tetapi intinya tetap satu: setiap router memilih next hop terbaik berdasarkan routing table, lalu mengulang keputusan itu untuk setiap paket. Connected dan static route cukup untuk jaringan kecil. Static route dengan pola default, black hole, floating, dan ECMP sudah dapat menangani banyak kebutuhan nyata. Ketika jaringan membesar, OSPF atau IS-IS menjaga agar setiap router mengetahui topologi internal secara otomatis, dan BGP menghubungkan jaringan kita dengan puluhan ribu jaringan lain yang membentuk Internet.

Bagi saya, kursus Routing Fundamentals dari APNIC menjadi jembatan yang baik antara teori di kelas dan praktik di lapangan. Materi dari Tugas 4–6 (subnetting dan VLSM) ternyata menjadi fondasi langsung untuk memahami *longest prefix match* dan agregasi prefix di BGP. Pemahaman yang sama juga berlaku di vendor mana pun, karena konsepnya identik dan hanya sintaks perintahnya yang berbeda.

---

## Referensi

1. APNIC Academy. *Routing Fundamentals Course*. <https://academy.apnic.net/en/course/routing-fundamentals-course>
2. APNIC Academy. *Routing Basics* (webinar course). <https://academy.apnic.net/en?p=15099>
3. Huston, G. *BGP in 2025*. APNIC Blog, 8 Januari 2026. <https://blog.apnic.net/2026/01/08/bgp-in-2025/>
4. Moy, J. RFC 2328: *OSPF Version 2*. IETF, 1998.
5. Coltun, R., Ferguson, D., Moy, J., & Lindem, A. RFC 5340: *OSPF for IPv6*. IETF, 2008.
6. Callon, R. RFC 1195: *Use of OSI IS-IS for Routing in TCP/IP and Dual Environments*. IETF, 1990.
7. Hopps, C. RFC 5308: *Routing IPv6 with IS-IS*. IETF, 2008.
8. Rekhter, Y., Li, T., & Hares, S. RFC 4271: *A Border Gateway Protocol 4 (BGP-4)*. IETF, 2006.
9. Arkko, J., Cotton, M., & Vegoda, L. RFC 5737: *IPv4 Address Blocks Reserved for Documentation*. IETF, 2010.
10. Huston, G. RFC 5398: *Autonomous System (AS) Number Reservation for Documentation Use*. IETF, 2008.
