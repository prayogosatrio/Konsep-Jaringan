# Tugas 2 Konsep Jaringan — Bab 2 (Level A, B, dan C)

11 Oktober 2026 · Prayogo Adhi Satrio

## Identitas

| Keterangan | Isi |
| --- | --- |
| Nama | Prayogo Adhi Satrio |
| NRP | 3125600043 |
| Program studi | S1 Teknik Informatika, PENS |
| Mata kuliah | Konsep Jaringan |
| Tugas | Tugas 2 — Latihan Bab 2 (Model Berlapis, OSI, dan TCP/IP) |

---

## Level A — Ingatan dan Pemahaman

### 1. Alasan komunikasi jaringan disusun berlapis

Komunikasi jaringan sangat kompleks: ada urusan sinyal fisik, pengalamatan, rute, keandalan, sampai format data aplikasi. Pelapisan memecah kerumitan itu menjadi bagian-bagian kecil yang masing-masing punya tugas jelas. Manfaatnya:

- **Modularitas** — tiap lapisan bisa dirancang, diuji, dan diganti sendiri. Contoh: Wi-Fi diganti Ethernet tanpa mengubah browser.
- **Abstraksi** — lapisan atas cukup memakai layanan lapisan bawah tanpa perlu tahu cara kerjanya.
- **Interoperabilitas** — vendor berbeda bisa saling terhubung asalkan mengikuti protokol yang sama di lapisan yang sama.
- **Kemudahan diagnosis** — gangguan bisa dilokalisasi per lapisan (fisik, alamat, port, aplikasi).
- **Bahasa bersama** — teknisi, dosen, dan vendor memakai istilah yang sama (perangkat L2, firewall L7).

### 2. Layanan, antarmuka, dan protokol

| Konsep | Arah hubungan | Pengertian | Contoh |
| --- | --- | --- | --- |
| Layanan (service) | Vertikal: lapisan bawah → lapisan atas | Apa yang disediakan suatu lapisan untuk lapisan di atasnya | TCP menyediakan aliran byte yang andal dan berurutan |
| Antarmuka (interface) | Vertikal: titik temu dua lapisan bersebelahan | Cara lapisan atas mengakses layanan lapisan bawah (operasi, parameter) | Socket API: `connect()`, `send()`, `recv()` |
| Protokol | Horizontal: lapisan yang sama di dua host | Aturan format pesan, urutan, dan tindakan antara entitas sejawat (peer) | Aturan three-way handshake dan format header TCP |

Intinya: layanan menjawab *apa*, antarmuka menjawab *bagaimana mengaksesnya*, protokol menjawab *bagaimana dua pihak sejawat berbicara*. Protokol boleh diganti selama layanan dan antarmukanya tetap.

### 3. Tujuh lapisan OSI (dari bawah ke atas)

| No. | Lapisan | Fungsi utama | Contoh |
| --- | --- | --- | --- |
| 1 | Physical | Mengirim bit mentah lewat media: sinyal, tegangan, konektor, modulasi | Kabel UTP, serat optik, radio 802.11 PHY |
| 2 | Data Link | Membentuk frame, alamat fisik (MAC), deteksi error per tautan, akses medium | Ethernet, Wi-Fi MAC, PPP |
| 3 | Network | Pengalamatan logis dan routing antarjaringan | IPv4, IPv6, ICMP |
| 4 | Transport | Komunikasi ujung ke ujung antarproses: port, keandalan, kontrol aliran dan kemacetan | TCP, UDP |
| 5 | Session | Membuka, mengatur, dan menutup dialog/sesi, sinkronisasi | NetBIOS session, RPC |
| 6 | Presentation | Representasi data: format, pengodean karakter, kompresi, enkripsi | ASN.1, encoding UTF-8, JPEG |
| 7 | Application | Layanan jaringan langsung bagi aplikasi pengguna | HTTP, DNS, SMTP, FTP |

### 4. Empat lapisan model TCP/IP

1. **Network Access / Link** — pengiriman frame dalam satu jaringan fisik (Ethernet, Wi-Fi).
2. **Internet** — pengalamatan IP dan routing antarjaringan (IPv4, IPv6, ICMP).
3. **Transport** — komunikasi antarproses ujung ke ujung (TCP, UDP, QUIC).
4. **Application** — protokol aplikasi, mencakup fungsi Session dan Presentation OSI (HTTP, DNS, TLS, SMTP).

### 5. Mengapa model TCP/IP kadang disajikan lima lapisan

RFC 1122 tidak mengatur detail fisik. Lapisan Network Access pada model empat lapisan menggabungkan dua hal yang sangat berbeda, yaitu **Data Link** (frame, MAC, switch) dan **Physical** (sinyal, kabel, radio). Dalam praktik dan pengajaran, keduanya perlu dibedakan, misalnya untuk menjelaskan perbedaan switch dan hub atau perbedaan masalah kabel dengan masalah VLAN. Karena itu banyak buku (mis. Kurose & Ross, Tanenbaum) memakai **model hibrida lima lapisan**: Physical, Link, Network, Transport, Application.

### 6. Frame, IP packet, TCP segment, dan UDP datagram

Semuanya adalah **PDU (Protocol Data Unit)**, yaitu satuan data pada lapisan tertentu.

| PDU | Lapisan | Header membawa | Ciri |
| --- | --- | --- | --- |
| Frame | Link (L2) | MAC tujuan & asal, EtherType; trailer FCS (CRC) | Hanya berlaku dalam satu tautan; dibuat ulang di setiap hop |
| IP packet | Internet/Network (L3) | Alamat IP asal & tujuan, TTL/Hop Limit, Protocol/Next Header | Berjalan ujung ke ujung melewati banyak router |
| TCP segment | Transport (L4) | Port asal & tujuan, nomor urut, ACK, flag, window | Bagian dari aliran byte yang andal dan berorientasi koneksi |
| UDP datagram | Transport (L4) | Port asal & tujuan, panjang, checksum (8 byte saja) | Mandiri, tanpa koneksi, tanpa jaminan sampai |

### 7. Header, trailer, dan payload

- **Header**: informasi kontrol yang ditambahkan di **depan** data oleh suatu lapisan, berisi alamat, nomor port, panjang, dan flag.
- **Trailer**: informasi kontrol yang ditambahkan di **belakang** data. Biasanya ada di lapisan Link untuk deteksi error, misalnya FCS/CRC-32 pada Ethernet.
- **Payload**: muatan atau isi yang dibawa suatu lapisan. Payload satu lapisan adalah PDU utuh lapisan di atasnya; misalnya payload paket IP adalah segmen TCP lengkap dengan header-nya.

### 8. Enkapsulasi dan dekapsulasi

**Enkapsulasi** terjadi di pengirim: data berjalan dari lapisan atas ke bawah, dan setiap lapisan membungkus PDU dari atas dengan header (dan trailer) miliknya.

```
Application  :                                   [ Data HTTP ]
Transport    :                       [ TCP hdr | Data HTTP ]                → segment
Network      :             [ IP hdr | TCP hdr | Data HTTP ]                 → packet
Link         : [ Eth hdr | IP hdr | TCP hdr | Data HTTP | FCS ]             → frame
Physical     : 0101101001110...                                             → bit
```

**Dekapsulasi** terjadi di penerima, dengan arah sebaliknya. Setiap lapisan membaca dan memeriksa header-nya, membuangnya, lalu menyerahkan payload ke lapisan di atas yang ditunjuk oleh field pengenal (EtherType, Protocol, nomor port).

### 9. Multiplexing dan demultiplexing

- **Multiplexing** (di pengirim): menggabungkan data dari banyak sumber di lapisan atas agar bisa dikirim lewat satu saluran di lapisan bawah. Contoh: browser, Spotify, dan WhatsApp memakai satu alamat IP dan satu kartu jaringan yang sama; masing-masing diberi nomor port berbeda.
- **Demultiplexing** (di penerima): memilah data yang datang dan menyerahkannya ke penerima yang tepat berdasarkan field pengenal.

Field pengenal di setiap batas lapisan:

| Batas | Field pengenal |
| --- | --- |
| Link → Network | EtherType (0x0800 = IPv4, 0x86DD = IPv6, 0x0806 = ARP) |
| Network → Transport | Protocol (IPv4) / Next Header (IPv6): 6 = TCP, 17 = UDP, 1 = ICMP |
| Transport → Application | Nomor port (53 DNS, 80 HTTP, 443 HTTPS); TCP memakai 5-tuple untuk membedakan koneksi |

### 10. Mengapa OSI tidak boleh dianggap spesifikasi implementasi

Model OSI (ISO/IEC 7498-1) adalah **model referensi konseptual**, bukan cetak biru perangkat lunak:

- OSI hanya mendefinisikan *apa* fungsi tiap lapisan, bukan format header, algoritma, atau API.
- Implementasi nyata tidak mengikuti tujuh lapisan. Internet memakai TCP/IP yang tidak punya lapisan Session dan Presentation terpisah.
- Banyak protokol tidak cocok di satu lapisan: TLS, QUIC, ARP, MPLS ("lapisan 2,5"), dan ICMP.
- Demi kinerja, implementasi sengaja melanggar batas lapisan: TCP checksum dihitung NIC (offload), kernel menggabungkan beberapa lapisan dalam satu fungsi.
- Rangkaian protokol OSI asli (CLNP, TP4, X.400) justru gagal diadopsi luas.

Jadi OSI dipakai sebagai **alat berpikir, bahasa bersama, dan kerangka troubleshooting**, bukan aturan wajib cara membangun sistem.

---

## Level B — Penerapan dan Analisis

### 11. Pemetaan protokol ke model TCP/IP

| Protokol | Lapisan TCP/IP | Perlu penjelasan? | Catatan |
| --- | --- | --- | --- |
| HTTP | Application | Tidak | HTTP/1.1 & HTTP/2 di atas TCP; HTTP/3 di atas QUIC |
| DNS | Application | **Ya** | Layanan aplikasi, tetapi menjadi infrastruktur yang dipakai hampir semua aplikasi lain. Memakai UDP/53 dan TCP/53, serta varian terenkripsi DoT (TCP/853), DoH (HTTPS/443), DoQ (QUIC) |
| TLS | Application (di antara aplikasi dan TCP) | **Ya** | Tidak cocok di satu lapisan. Menyediakan kerahasiaan dan autentikasi untuk aplikasi (fungsi mirip Presentation/Session OSI), tetapi berjalan di atas TCP dan di bawah HTTP. Pada QUIC, TLS 1.3 bahkan menyatu ke dalam transport |
| TCP | Transport | Tidak | Andal, berorientasi koneksi |
| UDP | Transport | Tidak | Tanpa koneksi, overhead kecil |
| QUIC | Transport | **Ya** | Fungsinya transport (keandalan, kontrol kemacetan, stream), tetapi dibawa di dalam UDP dan berjalan di user space; jadi secara teknis "transport di atas transport" |
| IPv6 | Internet | Tidak | Pengalamatan dan routing |
| ICMP / ICMPv6 | Internet | **Ya** | Bagian dari lapisan Internet sebagai protokol kontrol, tetapi pesannya dibawa *di dalam* paket IP (Protocol 1 / Next Header 58), seolah-olah lapisan di atas IP. ICMPv6 juga menjalankan Neighbor Discovery yang fungsinya setara ARP di L2 |
| Ethernet | Network Access (Link) | Tidak | Mencakup Physical dan Data Link OSI |
| Wi-Fi (802.11) | Network Access (Link) | **Ya** | Mencakup PHY dan MAC, tetapi juga memiliki fungsi tambahan seperti asosiasi, roaming, dan enkripsi WPA di L2 |

### 12. Enkapsulasi permintaan DNS melalui UDP, IPv4, dan Ethernet

Contoh: laptop 192.168.1.10 menanyakan `portal.pens.ac.id` ke server DNS 192.168.1.1 dalam satu LAN.

```
+-------------------------------------------------------------------------------+
| ETHERNET HEADER (14 B)                                                         |
|   Dst MAC = MAC server DNS / gateway   Src MAC = MAC laptop                    |
|   EtherType = 0x0800 (IPv4)  ---------------------------------------------+    |
+---------------------------------------------------------------------------|---+
| IPv4 HEADER (20 B)                                                     <--+    |
|   Src IP = 192.168.1.10   Dst IP = 192.168.1.1   TTL = 64                      |
|   Protocol = 17 (UDP)  ---------------------------------------------------+    |
+---------------------------------------------------------------------------|---+
| UDP HEADER (8 B)                                                       <--+    |
|   Src Port = 53001 (ephemeral)   Dst Port = 53 (DNS)  --------------------+    |
|   Length, Checksum                                                         |   |
+---------------------------------------------------------------------------|---+
| DNS MESSAGE                                                            <--+    |
|   Transaction ID = 0x3fa2   Flags: RD=1                                        |
|   Question: portal.pens.ac.id  Type A  Class IN                                |
+-------------------------------------------------------------------------------+
| ETHERNET TRAILER: FCS (CRC-32, 4 B)                                            |
+-------------------------------------------------------------------------------+
```

Pengenal pada setiap batas:

| Batas | Pengenal | Fungsi |
| --- | --- | --- |
| Ethernet → IP | EtherType 0x0800; MAC tujuan | Memberi tahu penerima bahwa payload adalah IPv4; MAC menentukan kartu jaringan tujuan di LAN |
| IP → UDP | Protocol = 17; alamat IP tujuan | Menyerahkan payload ke modul UDP di host tujuan |
| UDP → DNS | Port tujuan 53 (dan port asal 53001 untuk balasan) | Menyerahkan data ke proses server DNS; balasan kembali ke port 53001 |
| Di dalam DNS | Transaction ID | Mencocokkan jawaban dengan pertanyaan yang tepat |

Bila server DNS berada di luar subnet, MAC tujuan adalah MAC **default gateway** (didapat lewat ARP), sedangkan IP tujuan tetap IP server DNS.

### 13. Enkapsulasi HTTP/3 melalui QUIC

```
+-------------------------------------------------------------------------------+
| ETHERNET HEADER: Dst MAC = gateway, Src MAC = laptop, EtherType = 0x86DD/0x0800 |
+-------------------------------------------------------------------------------+
| IP HEADER: Src IP klien, Dst IP server, Protocol/Next Header = 17 (UDP)        |
+-------------------------------------------------------------------------------+
| UDP HEADER: Src Port = 51234, Dst Port = 443                                   |
+-------------------------------------------------------------------------------+
| QUIC PACKET HEADER (sebagian tidak terenkripsi)                                |
|   Destination Connection ID, Packet Number (dilindungi header protection)      |
+-------------------------------------------------------------------------------+
| ===== payload QUIC terenkripsi dengan kunci TLS 1.3 =====                      |
|   QUIC STREAM frame: Stream ID = 0, offset, length                             |
|     HTTP/3 frame: HEADERS (QPACK: :method GET, :path /, :authority ...)        |
|     HTTP/3 frame: DATA                                                         |
+-------------------------------------------------------------------------------+
| FCS                                                                             |
+-------------------------------------------------------------------------------+
```

Pengenal pada setiap batas: EtherType (Ethernet → IP), Protocol/Next Header 17 (IP → UDP), port UDP 443 (UDP → QUIC), **Connection ID** (mengidentifikasi koneksi QUIC, tidak bergantung pada IP/port), dan **Stream ID** (memisahkan setiap permintaan HTTP/3 di dalam satu koneksi).

Mengapa QUIC tetap dianggap transport walau berjalan di atas UDP:

- QUIC menjalankan **semua fungsi transport**: pembentukan koneksi (handshake), pengiriman andal dengan ACK dan retransmisi, kontrol aliran, kontrol kemacetan, dan multiplexing stream tanpa head-of-line blocking antar-stream.
- UDP hanya dipakai sebagai **pembungkus tipis** agar QUIC bisa melewati NAT dan firewall yang sudah ada dan bisa diimplementasikan di aplikasi (user space) tanpa menunggu pembaruan kernel atau middlebox. Protokol transport baru di atas IP langsung (Protocol number baru) hampir pasti diblokir middlebox.
- QUIC memiliki **identitas koneksinya sendiri** (Connection ID). Koneksi tetap hidup walaupun IP/port UDP berubah (connection migration), bukti bahwa UDP bukan "koneksi"-nya.
- Secara fungsi, QUIC menggantikan TCP + TLS sekaligus. Status lapisan ditentukan oleh **fungsi**, bukan oleh posisi dalam tumpukan header.

### 14. Dua host beda subnet melewati satu router (tanpa NAT)

Contoh: PC A (10.0.1.10) mengirim ke Server B (10.0.2.20) lewat router R.

| Header | Di segmen A → R | Di segmen R → B | Berubah? |
| --- | --- | --- | --- |
| Ethernet: MAC asal | MAC PC A | MAC interface keluar router | **Berubah** |
| Ethernet: MAC tujuan | MAC interface router (gateway) | MAC Server B | **Berubah** |
| Ethernet: FCS | Dihitung A | Dihitung ulang router | **Berubah** |
| IP: alamat asal & tujuan | 10.0.1.10 → 10.0.2.20 | 10.0.1.10 → 10.0.2.20 | Tetap |
| IP: TTL (IPv4) / Hop Limit (IPv6) | 64 | 63 | **Berubah** (dikurangi 1) |
| IPv4: header checksum | — | Dihitung ulang | **Berubah** (karena TTL berubah; IPv6 tidak punya checksum header) |
| IP: DSCP/ECN | — | — | Biasanya tetap; bisa diubah bila ada kebijakan QoS atau penandaan kemacetan ECN |
| TCP/UDP header (port, nomor urut, checksum) | — | — | Tetap |
| Payload aplikasi | — | — | Tetap |

Kesimpulan: **header L2 berlaku per hop** dan diganti di setiap router, sedangkan **header L3 berlaku ujung ke ujung** (kecuali TTL dan checksum), dan **L4 ke atas tidak disentuh** oleh router biasa. Pengecualian kecil: fragmentasi IPv4 bila MTU keluar lebih kecil (menambah field fragment offset dan memecah paket).

### 15. Bila router juga melakukan NAT/PAT

Analisis berubah karena router kini **mengubah informasi L3 dan L4**:

- **IP asal** berubah dari alamat privat (10.0.1.10) menjadi alamat publik router (mis. 203.0.113.5). Pada lalu lintas balasan, **IP tujuan** diterjemahkan kembali.
- **Port asal** berubah (PAT/NAT overload), mis. 51234 → 40001, agar banyak host bisa berbagi satu IP publik.
- **Checksum IP, TCP, dan UDP dihitung ulang**, karena checksum TCP/UDP mencakup *pseudo-header* yang berisi alamat IP.
- Router harus menyimpan **state** (tabel translasi 5-tuple) dan menghapusnya setelah timeout. Koneksi dari luar tidak bisa masuk tanpa *port forwarding*.
- Untuk protokol yang menulis alamat IP di dalam payload (FTP aktif, SIP), router membutuhkan **ALG** yang mengubah isi L7.

Dampak: prinsip end-to-end terganggu (alamat asli tersembunyi), IPsec AH gagal karena header yang diautentikasi berubah, aplikasi P2P/VoIP butuh teknik NAT traversal (STUN/TURN/ICE), dan log forensik harus mencatat IP **dan** port beserta waktu agar bisa melacak pengguna asli.

### 16. Checksum TCP salah pada capture, tetapi komunikasi lancar

Hipotesis: **NIC TX checksum offload**. Sistem operasi menyerahkan perhitungan checksum TCP/UDP ke kartu jaringan untuk menghemat CPU. Wireshark/tcpdump menangkap paket di kernel **sebelum** paket sampai ke NIC, sehingga field checksum masih kosong atau berisi nilai sementara. NIC baru mengisi checksum yang benar tepat sebelum mengirim, jadi paket di kabel sebenarnya valid. Wireshark biasanya menandai: *"incorrect, should be 0x…(maybe caused by TCP checksum offload?)"*.

Gejala terkait: **TSO/GSO (segmentation offload)**. Capture menampilkan segmen TCP sangat besar (mis. 64 KB, melebihi MTU 1500) karena pemecahan ke ukuran MTU juga dilakukan NIC.

Cara membuktikan:

1. Cek fitur offload: `ethtool -k eth0 | grep -i checksum` (Linux).
2. Matikan sementara: `sudo ethtool -K eth0 tx off tso off gso off`, lalu capture ulang; checksum seharusnya benar.
3. Capture dari host lain atau port mirroring (SPAN) di switch; paket di kabel akan menunjukkan checksum yang valid.
4. Paket **masuk** dengan checksum benar dan tidak ada retransmisi menunjukkan tidak ada korupsi nyata.
5. Di Wireshark, nonaktifkan validasi checksum (Preferences → Protocols → TCP) agar analisis tidak terganggu.

### 17. Portal bisa dibuka dengan IP, tetapi tidak dengan nama

Karena akses via IP berhasil, lapisan Physical, Link, Network, Transport, bahkan HTTP ke server sudah terbukti bekerja. Masalah hampir pasti ada pada **resolusi nama (DNS, lapisan Application)** atau hal yang bergantung pada nama.

| Langkah | Lapisan | Pemeriksaan | Interpretasi |
| --- | --- | --- | --- |
| 1 | L1–L4 | `ping <IP>` dan buka `https://<IP>` | Berhasil → jalur fisik, IP, dan port sehat |
| 2 | L7 (DNS) | `nslookup portal.pens.ac.id` / `dig portal.pens.ac.id` | Gagal (timeout/NXDOMAIN) → masalah DNS |
| 3 | Konfigurasi host | `ipconfig /all` atau `resolvectl status`: server DNS mana yang dipakai? | DNS salah/kosong (mis. DHCP memberi DNS publik yang tidak tahu nama internal) |
| 4 | L4 ke DNS | `dig @<server-dns-kampus> portal.pens.ac.id` | Bila server lain bisa menjawab → masalah di server DNS yang dipakai; bila timeout → UDP/TCP 53 diblokir firewall |
| 5 | Split DNS / VPN | Apakah nama itu hanya terdaftar di DNS internal? | Pengguna di luar kampus atau browser memakai DoH (mis. ke 1.1.1.1) sehingga melewati DNS internal |
| 6 | Data DNS | Bandingkan alamat hasil resolusi dengan IP yang berhasil | Record salah/kedaluwarsa, cache lama (`ipconfig /flushdns`), file `hosts` berisi entri keliru |
| 7 | IPv6 | Apakah ada record AAAA? | Nama di-resolve ke IPv6 yang tidak bisa dijangkau, sementara uji IP memakai IPv4 |
| 8 | L7 (HTTP/TLS) | Bila nama ter-resolve ke IP yang sama tetapi tetap gagal | Masalah virtual host/SNI atau sertifikat yang terikat pada nama (bukan DNS) |

### 18. Ping berhasil, HTTPS gagal — hipotesis lapisan Transport hingga Application

Ping (ICMP) yang berhasil hanya membuktikan lapisan Network ke bawah. Hipotesis di atasnya:

| No. | Lapisan | Hipotesis | Cara uji |
| --- | --- | --- | --- |
| 1 | Transport | Firewall/ACL memblokir **TCP 443** (ICMP diizinkan) | `Test-NetConnection host -Port 443` / `nc -vz host 443`; timeout → diblokir |
| 2 | Transport | **Layanan tidak mendengarkan** di port 443 (web server mati, salah bind) | Di server: `ss -tlnp \| grep 443`; RST dari klien → port tertutup |
| 3 | Transport/Network | **MTU black hole**: paket kecil (ping, SYN) lolos, tetapi paket besar berisi sertifikat TLS dibuang dan ICMP "fragmentation needed" diblokir | `ping -M do -s 1472`; handshake berhenti setelah ClientHello |
| 4 | Transport/App | **Load balancer** tidak punya backend sehat, atau rate limit/SYN flood protection menolak koneksi | Cek status backend dan log LB |
| 5 | TLS (Session/Presentation) | **Versi TLS atau cipher tidak cocok** (klien lama vs server hanya TLS 1.3) | `openssl s_client -connect host:443 -tls1_2`; alert "protocol_version"/"handshake_failure" |
| 6 | TLS | **Sertifikat bermasalah**: kedaluwarsa, nama tidak cocok, CA tidak dipercaya, rantai tidak lengkap | Detail error browser; `openssl s_client -showcerts` |
| 7 | TLS | **Jam klien salah**, sehingga sertifikat dianggap belum berlaku/kedaluwarsa | Cek tanggal sistem |
| 8 | TLS/App | **Proxy wajib** atau proxy inspeksi TLS memotong koneksi; sertifikat proxy tidak dipercaya | Cek setelan proxy/PAC; issuer sertifikat yang diterima |
| 9 | Application | Server menjawab tetapi **error HTTP** (403 dari WAF, 500/502/503) atau redirect loop/HSTS | `curl -vk https://host`; lihat kode status |
| 10 | Application/DNS | Nama di-resolve ke IP berbeda dari IP yang di-ping (mis. AAAA/IPv6) | Ping dan curl memakai alamat yang sama secara eksplisit |

### 19. Sesi aplikasi vs koneksi TCP

| Aspek | Koneksi TCP | Sesi aplikasi |
| --- | --- | --- |
| Lapisan | Transport | Application (konsep Session OSI) |
| Identitas | 5-tuple: IP asal, IP tujuan, port asal, port tujuan, protokol | Token/cookie/ID sesi, akun pengguna |
| Umur | Dari three-way handshake sampai FIN/RST atau timeout | Ditentukan logika aplikasi: menit, jam, bahkan hari |
| Status | Nomor urut, window, buffer di kernel | Data login, isi keranjang, posisi video, di server/basis data |
| Hubungan | Satu koneksi bisa membawa banyak permintaan | Satu sesi bisa memakai banyak koneksi berturut-turut atau paralel |

Contoh sesi bertahan saat koneksi berubah:

- **Login web**: setelah login di SIAKAD, browser membuka dan menutup banyak koneksi TCP (keep-alive habis, tab baru), tetapi pengguna tetap login karena **cookie sesi** dikirim di setiap koneksi.
- **Pindah jaringan Wi-Fi → 4G**: alamat IP berubah sehingga koneksi TCP lama mati. Aplikasi seperti WhatsApp atau Zoom membuat koneksi baru dan melanjutkan sesi dengan token yang sama. Pada **QUIC**, bahkan koneksinya sendiri bisa bermigrasi karena diidentifikasi dengan Connection ID, bukan IP/port.
- **TLS session resumption**: koneksi TCP baru dapat melanjutkan sesi TLS lama dengan session ticket tanpa handshake penuh.
- **Unduhan yang dilanjutkan**: HTTP Range request melanjutkan unduhan di koneksi baru setelah koneksi pertama putus.

### 20. Mengapa enkripsi tidak bisa mutlak ditempatkan di Presentation layer

Dalam OSI, enkripsi disebut sebagai fungsi Presentation. Dalam praktik, enkripsi muncul di hampir setiap lapisan karena tiap lapisan melindungi cakupan yang berbeda:

| Lapisan | Mekanisme | Melindungi |
| --- | --- | --- |
| Link (L2) | MACsec (802.1AE), WPA2/WPA3 | Satu tautan atau udara antara klien dan AP |
| Network (L3) | IPsec | Seluruh lalu lintas IP antar-host/jaringan (VPN) |
| Transport | QUIC (enkripsi menyatu dengan transport), TCP-AO | Koneksi transport, termasuk sebagian header transport |
| Antara Transport dan Application | TLS, DTLS | Satu koneksi aplikasi |
| Application | Enkripsi end-to-end (Signal Protocol), PGP, enkripsi berkas | Pesan atau data dari pengguna ke pengguna |

Alasannya:

- **TCP/IP tidak memiliki lapisan Presentation** yang terpisah; fungsinya dijalankan protokol aplikasi atau pustaka seperti TLS.
- **TLS tidak hanya mengubah representasi data**: ia juga melakukan autentikasi server, negosiasi kunci, dan menjaga integritas (mirip fungsi Session), serta berjalan sebagai pustaka di dalam proses aplikasi.
- **Tujuan keamanan menentukan lapisan**: melindungi tautan fisik dari penyadapan berbeda dengan melindungi isi chat dari penyedia layanan.
- **Header lapisan bawah harus tetap terbaca** oleh router dan switch agar paket bisa diteruskan. Karena itu enkripsi di lapisan atas tidak menyembunyikan alamat IP, sedangkan enkripsi di bawah (IPsec tunnel) menyembunyikannya tetapi butuh header luar baru.
- Banyak sistem menerapkan **enkripsi berlapis** (defense in depth), misalnya HTTPS di atas VPN IPsec di atas Wi-Fi WPA3.

---

## Level C — Evaluasi dan Sintesis

### 21. Evaluasi: "Model OSI tidak lagi relevan karena Internet menggunakan TCP/IP"

Pernyataan ini **sebagian benar tetapi keliru dalam kesimpulannya**, karena mencampuradukkan tiga hal yang berbeda: model, protokol, dan kegunaan pedagogis.

**1. Model berbeda dengan protokol.** OSI terdiri atas dua hal: (a) **model referensi** tujuh lapisan (ISO/IEC 7498-1) dan (b) **rangkaian protokol OSI** (CLNP, TP4, X.400, FTAM). Yang kalah bersaing adalah rangkaian protokolnya, bukan model referensinya. Internet memang menjalankan protokol TCP/IP, tetapi protokol itu tetap bisa dijelaskan dengan kerangka OSI.

**2. Model TCP/IP juga bukan cerminan sempurna.** Model TCP/IP lahir *setelah* protokolnya ada, sehingga ia lebih berupa deskripsi daripada model analitis. Ia tidak membedakan Physical dan Data Link, dan menggabungkan Session/Presentation ke dalam Application. Akibatnya untuk membahas switch, VLAN, atau masalah kabel, orang tetap memakai istilah OSI.

**3. OSI tetap hidup sebagai bahasa industri.** Istilah "switch Layer 2", "switch Layer 3", "load balancer L4/L7", "firewall Layer 7", dan "MPLS Layer 2,5" berasal dari penomoran OSI. Vendor, sertifikasi (CCNA, CompTIA Network+), dan dokumentasi teknis memakainya setiap hari.

**4. Kegunaan pedagogis dan diagnosis.** OSI memisahkan konsep secara bersih sehingga mahasiswa memahami pembagian tugas, enkapsulasi, dan cara melokalisasi gangguan (bottom-up atau top-down troubleshooting).

**5. Keterbatasan OSI yang harus diakui.** Lapisan Session dan Presentation jarang punya protokol mandiri; banyak protokol modern (TLS, QUIC, VXLAN) tidak masuk rapi ke satu lapisan.

**Kesimpulan:** OSI tidak relevan sebagai *rangkaian protokol*, tetapi tetap relevan sebagai *model referensi, kosakata profesional, dan alat belajar*. TCP/IP lebih tepat untuk menjelaskan *implementasi* Internet. Keduanya saling melengkapi.

### 22. Strict layering: keuntungan, kerugian, dan cross-layer information

**Strict layering** berarti setiap lapisan hanya berinteraksi dengan lapisan tepat di atas dan di bawahnya melalui antarmuka resmi, tanpa mengintip informasi lapisan lain.

| Keuntungan | Kerugian |
| --- | --- |
| Modularitas: komponen bisa diganti tanpa efek samping (Wi-Fi → 5G tanpa mengubah aplikasi) | Fungsi terduplikasi: pemeriksaan error dan retransmisi di L2, L4, dan L7 |
| Evolusi independen; inovasi di satu lapisan tidak menunggu lapisan lain | Overhead kinerja: tiap batas lapisan menambah salinan data dan header |
| Interoperabilitas antarvendor | Informasi penting tersembunyi: TCP menganggap semua kehilangan paket sebagai kemacetan, padahal di Wi-Fi bisa karena gangguan radio |
| Mudah diuji, diajarkan, dan dianalisis | Sulit mengoptimalkan untuk media khusus (nirkabel, satelit) |

**Kapan cross-layer information membantu:**

- **ECN**: router (L3) menandai paket saat mulai padat agar TCP (L4) menurunkan laju sebelum paket dibuang.
- **Path MTU Discovery**: ICMP (L3) memberi tahu TCP ukuran segmen maksimum.
- **Adaptive bitrate video**: aplikasi menyesuaikan kualitas berdasarkan estimasi throughput dari transport.
- **Wi-Fi rate adaptation dan WMM**: penandaan DSCP dari aplikasi dipetakan ke antrean prioritas di L2.
- **NIC offload (TSO, checksum offload)**: hardware L2 mengerjakan tugas L4 untuk efisiensi.

**Kapan cross-layer merusak modularitas:**

- **Ossification**: middlebox yang membaca dan mengandalkan header TCP membuat TCP sulit dikembangkan; opsi TCP baru sering dibuang. Ini salah satu alasan QUIC mengenkripsi hampir seluruh header-nya.
- **NAT dan ALG** mengubah isi L4/L7, sehingga protokol baru (IPsec, SIP) rusak.
- **Ketergantungan tersembunyi**: aplikasi yang bergantung pada detail media tertentu akan rusak ketika media diganti.
- **Kompleksitas pemeliharaan**: perubahan satu lapisan memaksa perubahan lapisan lain, dan bug lintas lapisan sulit dilacak.

Prinsip yang sehat: gunakan cross-layer sebagai **petunjuk (hint) opsional** lewat antarmuka yang terdefinisi (seperti ECN dan DSCP), bukan sebagai ketergantungan wajib.

### 23. Prosedur troubleshooting: video konferensi tersendat di Wi-Fi kampus saat jam sibuk

**Definisi masalah.** "Tersendat" diubah menjadi metrik terukur: jitter, packet loss, latensi, bitrate video, dan freeze. Pola awal: terjadi hanya di Wi-Fi dan hanya saat jam sibuk, sehingga dugaan kuat adalah kapasitas atau kualitas udara Wi-Fi.

**Langkah 1 — Uji pembanding.** Lakukan panggilan yang sama dari lokasi yang sama memakai kabel LAN; dari Wi-Fi pada jam sepi; dan dari Wi-Fi di gedung lain. Bila kabel lancar sementara Wi-Fi tidak, fokus ke L1–L2 nirkabel.

**Langkah 2 — Kumpulkan bukti per lapisan.**

| Lapisan | Bukti yang dikumpulkan | Alat | Indikasi masalah |
| --- | --- | --- | --- |
| Physical (L1) | RSSI, SNR, noise floor, utilisasi kanal, interferensi non-Wi-Fi | Controller Wi-Fi, WiFi Analyzer, spectrum analyzer | RSSI < -67 dBm, SNR < 25 dB, utilisasi kanal > 70%, kanal 2,4 GHz tumpang tindih |
| Data Link (L2) | Jumlah klien per AP, airtime, retry rate, data rate, kejadian roaming, antrean WMM | Dashboard controller, capture 802.11 | > 40–50 klien per radio, retry > 10–15%, klien lambat (802.11n/2,4 GHz) memakan airtime, roaming gagal (sticky client) |
| Network (L3) | Latensi, jitter, dan loss ke gateway lalu ke server konferensi; penandaan DSCP | `ping`, `mtr`, `iperf3 -u`, Wireshark | Jitter melonjak sejak hop pertama (gateway) → masalah Wi-Fi; mulai di hop ISP → masalah WAN; DSCP EF terhapus |
| Transport (L4) | Penggunaan UDP vs fallback ke TCP/443, statistik loss RTP | Wireshark (RTP/RTCP stream analysis) | UDP diblokir sehingga aplikasi jatuh ke TCP yang memperparah delay; loss RTP > 1–2% |
| Application (L7) | Statistik panggilan: bitrate, resolusi, jitter, packet loss, CPU | Zoom/Teams/Meet stats, log admin | Aplikasi menurunkan resolusi; log kualitas menunjukkan gangguan jaringan, bukan CPU perangkat |
| Uplink/WAN | Utilisasi uplink AP, switch akses, dan link ISP pada jam sibuk | SNMP/NetFlow, grafik controller | Uplink AP 1 Gbps penuh atau link ISP > 80% |

**Langkah 3 — Uji hipotesis.** Contoh: pindahkan klien uji ke SSID 5/6 GHz; batasi jumlah klien per AP; aktifkan band steering; naikkan minimum data rate untuk membuang klien lambat; aktifkan WMM dan petakan DSCP EF/AF41; batasi aplikasi berat (update OS, streaming) saat jam kuliah.

**Langkah 4 — Kriteria keberhasilan.** Pada jam sibuk: jitter < 30 ms, packet loss < 1%, latensi satu arah < 150 ms, video minimal 720p stabil, dan tidak ada keluhan berulang selama dua minggu.

### 24. Skenario laboratorium perekaman paket tanpa data sensitif

**Tujuan:** mahasiswa melihat Ethernet, IP, TCP/UDP, TLS, dan protokol aplikasi dalam satu capture, tanpa menyentuh data pribadi.

**Topologi lab (terisolasi):**

```
[VM Klien 10.10.10.2] ---- [Switch virtual / bridge lab] ---- [VM Server 10.10.10.1]
   Wireshark                                                    dnsmasq (DNS lab.local)
   browser, curl, dig                                           nginx (HTTP :80, HTTPS :443,
                                                                sertifikat self-signed)
```

**Aturan keamanan dan etika:**

- Jaringan lab terisolasi (host-only network/VLAN khusus), tanpa akses Internet, sehingga tidak ada lalu lintas pengguna lain yang terekam.
- Hanya memakai akun dan data **dummy** (mis. `mahasiswa01` / `Lab-Test-123`); halaman web berisi teks contoh.
- Capture filter dibatasi: `host 10.10.10.1 and host 10.10.10.2`.
- File capture hanya disimpan di VM lab dan dihapus setelah praktikum; dilarang merekam di Wi-Fi kampus atau jaringan rumah.

**Langkah praktikum:**

| No. | Aktivitas | Perintah | Display filter Wireshark | Yang diamati |
| --- | --- | --- | --- | --- |
| 1 | ARP dan ICMP | `ping 10.10.10.1` | `arp \|\| icmp` | Frame Ethernet, EtherType, alamat MAC, header IP, TTL |
| 2 | DNS di atas UDP | `dig @10.10.10.1 web.lab.local` | `dns` | Port 53, Transaction ID, Protocol = 17 di header IP |
| 3 | HTTP di atas TCP | `curl http://web.lab.local/` | `tcp.port == 80` | Three-way handshake, nomor urut, header HTTP terbaca jelas |
| 4 | HTTPS (TLS 1.3) | `curl -k https://web.lab.local/` | `tls` | ClientHello, SNI, ServerHello; isi HTTP tidak terbaca |
| 5 | Dekripsi TLS milik sendiri | Jalankan browser dengan variabel `SSLKEYLOGFILE` lalu muat file kunci di Wireshark | `http` | Bagaimana kunci sesi membuka isi HTTP; menunjukkan kenapa TLS melindungi data |
| 6 | Enkapsulasi | Pilih satu paket HTTPS, buka panel detail | — | Urutan Ethernet → IPv4 → TCP → TLS → (HTTP) |

**Laporan mahasiswa:** gambar enkapsulasi satu paket per protokol, tabel field pengenal (EtherType, Protocol, port), serta perbandingan HTTP vs HTTPS dari sisi apa yang terlihat oleh penyadap.

### 25. VXLAN di atas UDP dan IPsec tunnel: urutan header dan risiko MTU

Skenario: dua data center menghubungkan VLAN yang sama dengan VXLAN, dan lalu lintas antarsitus dilindungi IPsec tunnel mode (ESP).

```
+--------------------------------------------------------------------------------------+
| Outer Ethernet (14 B) — MAC antar-router WAN                                          |
| Outer IP (20 B) — IP gateway IPsec situs A → situs B, Protocol 50 (ESP)               |
| ESP header (8 B) + IV (8–16 B)                                                        |
| ====================== TERENKRIPSI (ESP) ==========================================  |
|   IP VTEP (20 B) — IP VTEP A → VTEP B, Protocol 17                                    |
|   UDP (8 B) — Dst Port 4789                                                           |
|   VXLAN header (8 B) — VNI (VXLAN Network Identifier)                                 |
|   Inner Ethernet (14 B) — MAC VM asal → MAC VM tujuan                                 |
|   Inner IP (20 B) — IP VM asal → IP VM tujuan                                         |
|   TCP (20 B) + data aplikasi                                                          |
|   ESP trailer: padding (0–15 B) + pad length + next header (2 B)                      |
| ===================================================================================  |
| ESP ICV (12–16 B, integritas)                                                         |
| Outer FCS (4 B)                                                                       |
+--------------------------------------------------------------------------------------+
```

**Perhitungan overhead (IPv4):**

| Lapisan tambahan | Ukuran |
| --- | --- |
| VXLAN: inner Ethernet 14 + VXLAN 8 + UDP 8 + IP VTEP 20 | 50 byte |
| IPsec ESP tunnel: outer IP 20 + ESP 8 + IV 16 + trailer 2–17 + ICV 16 | ± 62–77 byte |
| Total | ± 112–127 byte |

Dengan MTU fisik 1500 byte, paket IP milik VM hanya boleh sekitar **1.370 byte** agar tidak melebihi MTU.

**Risiko MTU:**

- **Fragmentasi**: paket 1.500 byte dari VM membengkak menjadi ± 1.625 byte. Router harus memecahnya (beban CPU, latensi naik), atau paket dibuang bila bit DF aktif.
- **PMTUD black hole**: bila ICMP "Fragmentation Needed"/"Packet Too Big" diblokir firewall, pengirim tidak tahu harus mengecilkan paket. Gejalanya khas: ping kecil dan handshake berhasil, tetapi transfer berkas, SSH dengan banyak data, atau HTTPS macet.
- **Fragmen sulit diproses**: firewall dan load balancer tidak bisa membaca port pada fragmen kedua; fragmen yang hilang membuat seluruh paket hilang.
- **Kinerja**: overhead ± 8% per paket ditambah biaya enkripsi.

**Mitigasi:** naikkan MTU underlay ke jumbo frame (mis. 9000) di jalur yang mendukung; turunkan MTU interface VM (mis. 1400); terapkan **TCP MSS clamping** di gateway; izinkan ICMP tipe 3 kode 4 (IPv4) dan ICMPv6 Packet Too Big; uji dengan `ping -M do -s <ukuran>`.

### 26. Perbandingan MACsec, IPsec, TLS, dan enkripsi end-to-end aplikasi

| Aspek | MACsec (802.1AE) | IPsec | TLS | Enkripsi end-to-end aplikasi |
| --- | --- | --- | --- | --- |
| Lapisan | Data Link (L2) | Network (L3) | Antara Transport dan Application | Application |
| Cakupan perlindungan | Satu tautan (hop-by-hop) antara dua perangkat bersebelahan | Antara dua host atau dua gateway (tunnel/VPN) | Satu koneksi antara klien dan titik terminasi TLS | Pesan/data dari pengguna asal ke pengguna tujuan |
| Titik terminasi | Setiap port switch/router; data didekripsi di setiap hop | Gateway VPN atau host ujung | Server, atau sering **load balancer, CDN, reverse proxy, proxy inspeksi** | Hanya perangkat pengirim dan penerima akhir |
| Yang terlihat oleh perantara | Di dalam perangkat: semua; di kabel: hanya header Ethernet | Header IP luar (alamat gateway) | IP, port, SNI (kecuali ECH), ukuran dan waktu paket | Metadata (siapa, kapan, ukuran), tetapi isi tidak |
| Siapa yang harus dipercaya | Semua switch/router yang dilalui | Jaringan internal di belakang gateway dan operator gateway | Pihak yang memegang kunci TLS (penyedia layanan, CDN) | Hanya perangkat dan kunci milik pengguna |
| Melindungi dari | Penyadapan kabel, perangkat jahat di tautan fisik | Penyadapan di Internet/WAN antar situs | Penyadapan dan manipulasi di jalur antara klien dan server | Penyadapan oleh penyedia layanan dan server perantara |
| Contoh | Link antar-switch data center | VPN site-to-site, VPN akses jarak jauh | HTTPS, IMAPS, SMTP STARTTLS | WhatsApp/Signal, PGP |

Prinsipnya: **semakin tinggi lapisannya, semakin sempit lingkaran kepercayaan yang dibutuhkan**, tetapi semakin sedikit lalu lintas yang dilindungi secara otomatis. Enkripsi lapisan bawah melindungi semua aplikasi sekaligus namun dibuka di setiap titik terminasi. Karena itu organisasi sering menggabungkannya.

### 27. Firewall, proxy, dan load balancer menantang anggapan "tiap perangkat hanya membaca lapisannya"

Dalam teori, router hanya membaca header L3 dan switch hanya header L2. Kenyataannya, banyak perangkat perantara membaca, bahkan mengubah, lapisan yang lebih tinggi:

| Perangkat | Lapisan yang dibaca/diubah | Contoh perilaku |
| --- | --- | --- |
| Firewall stateful | L3 + L4 | Membaca port dan flag TCP, melacak status koneksi (SYN, ESTABLISHED), sehingga router bertindak sampai lapisan Transport |
| Next-Generation Firewall / IPS | L3 sampai L7 | Deep Packet Inspection: mengenali aplikasi dari pola payload, membaca SNI TLS, bahkan mendekripsi TLS (TLS inspection) untuk memindai malware |
| Proxy (forward/reverse) | Memutus koneksi di L4 dan L7 | Menjadi ujung koneksi TCP/TLS dari klien, lalu membuat koneksi baru ke server; bisa mengubah header HTTP, menyimpan cache, dan menyaring URL |
| Load balancer L4 | L3 + L4 | Memilih backend berdasarkan IP/port, melakukan NAT tujuan |
| Load balancer L7 | Sampai L7 | Terminasi TLS, membaca Host, path, dan cookie HTTP untuk routing dan session persistence; menambahkan header `X-Forwarded-For` |
| NAT router | L3 + L4 (kadang L7 lewat ALG) | Menulis ulang IP, port, dan checksum; ALG mengubah isi pesan FTP/SIP |
| Switch L3/router ECMP | L3 + L4 | Hashing 5-tuple (termasuk port) untuk membagi lalu lintas ke beberapa jalur |

Implikasinya:

- Prinsip **end-to-end** terganggu; "ujung" koneksi bisa jadi adalah proxy, bukan server sebenarnya.
- **Ossification protokol**: perangkat yang mengharapkan header tertentu membuang paket dengan format baru, menghambat inovasi (alasan QUIC mengenkripsi header).
- **Privasi dan kepercayaan**: TLS inspection berarti perangkat perantara melihat data yang seharusnya terenkripsi.
- **Troubleshooting** harus memperhitungkan bahwa kegagalan aplikasi bisa disebabkan perangkat yang secara teori hanya "L3".

### 28. Prinsip end-to-end untuk pemeriksaan integritas berkas

**Prinsip end-to-end** (Saltzer, Reed, & Clark, 1984): suatu fungsi hanya dapat diimplementasikan secara lengkap dan benar dengan pengetahuan dan bantuan aplikasi di titik ujung komunikasi. Implementasi di lapisan bawah hanya boleh menjadi **optimasi kinerja**, bukan jaminan kebenaran.

| Penempatan | Kemampuan | Keterbatasan | Penilaian |
| --- | --- | --- | --- |
| Router / tautan (CRC Ethernet) | Mendeteksi error bit di kabel per hop | Tidak mendeteksi korupsi di memori router, bug perangkat lunak, atau kesalahan setelah paket keluar dari tautan; router tidak tahu batas "berkas" | Tidak tepat untuk integritas berkas; cukup sebagai pengaman per hop |
| Transport (checksum TCP 16-bit) | Mendeteksi sebagian besar error dan memicu retransmisi otomatis | Checksum lemah (beberapa pola error lolos); tidak melindungi data saat ditulis ke disk, saat melewati proxy yang membuka koneksi, atau dari manipulasi sengaja | Optimasi yang berguna, tetapi bukan jaminan akhir |
| Aplikasi (hash SHA-256, tanda tangan digital) | Memverifikasi berkas utuh dari sumber hingga tersimpan di tujuan, termasuk melintasi proxy, CDN, dan disk; tanda tangan juga membuktikan keaslian | Butuh komputasi di ujung dan distribusi hash yang terpercaya | **Tempat yang benar** untuk jaminan integritas berkas |

**Kesimpulan:** pemeriksaan integritas berkas harus dilakukan di **aplikasi** (mis. verifikasi SHA-256 berkas ISO, tanda tangan paket `apt`/`npm`). Pemeriksaan di transport dan link tetap dipertahankan karena mendeteksi error lebih awal dan murah untuk dikoreksi, tetapi tidak dijadikan satu-satunya jaminan. Router tidak sebaiknya memeriksa integritas berkas karena harus tetap sederhana dan tanpa state agar bisa berskala besar.

### 29. Retry storm ketika aplikasi, service mesh, dan client sama-sama mengulang

**Skenario:** client memanggil layanan A, lewat sidecar service mesh (Envoy/Istio), dan kode layanan A memanggil basis data dengan pustaka yang juga punya retry. Masing-masing dikonfigurasi "coba hingga 3 kali".

**Perhitungan amplifikasi:** bila setiap tingkat membuat hingga 3 percobaan, satu permintaan pengguna bisa berubah menjadi 3 × 3 × 3 = **27 permintaan** ke layanan terbawah. Bila retry dihitung sebagai 1 percobaan awal + 3 ulangan, jumlahnya (1+3)³ = **64 percobaan**. Ditambah lagi pengguna yang menekan tombol "refresh".

**Mekanisme badai:**

1. Layanan basis data sedikit melambat karena beban tinggi.
2. Timeout terlewati, sehingga setiap lapisan mengulang permintaan bersamaan.
3. Beban berlipat ganda tepat ketika layanan paling lemah, sehingga semakin banyak permintaan gagal dan diulang.
4. Terjadi **cascading failure** dan sistem tidak pulih walau penyebab awal sudah hilang (metastable failure).

**Mengapa lintas lapisan:**

- Setiap lapisan merancang retry secara **independen** dan tidak tahu bahwa lapisan lain juga mengulang (abstraksi menyembunyikan perilaku itu).
- Retry terjadi di berbagai tingkat sekaligus: **TCP** (retransmisi segmen), **TLS/koneksi** (reconnect), **service mesh** (L7 proxy), **pustaka aplikasi**, dan **client/pengguna**.
- **Timeout tidak selaras**: timeout luar lebih pendek dari total waktu retry di dalam, sehingga lapisan luar menyerah dan mengulang sementara lapisan dalam masih mencoba.
- Masalahnya adalah **sifat emergen sistem**, bukan bug di satu komponen; tidak bisa diperbaiki hanya di satu lapisan.

**Mitigasi:**

- Tetapkan **satu lapisan pemilik retry** (biasanya paling dekat dengan client atau di service mesh); lapisan lain tidak mengulang.
- **Retry budget**: retry maksimal mis. 10–20% dari total permintaan.
- **Exponential backoff dengan jitter** agar permintaan tidak serentak.
- **Circuit breaker** untuk berhenti mengirim ke layanan yang gagal, plus **load shedding** dan **rate limiting** di server.
- **Propagasi deadline** (mis. gRPC deadline) agar lapisan dalam tahu sisa waktu.
- Hanya mengulang operasi **idempoten**, atau memakai **idempotency key**.
- Pantau metrik rasio retry per lapisan.

### 30. Model apa yang sebaiknya dipakai untuk pemula?

**Posisi saya: gunakan model hibrida lima lapisan sebagai kerangka utama, dengan OSI tujuh lapisan sebagai peta kosakata.**

**Tujuan pembelajaran untuk pemula:**

1. Memahami bagaimana data berpindah dari aplikasi di satu komputer ke aplikasi di komputer lain (enkapsulasi dan dekapsulasi).
2. Mengenali peran perangkat (switch, router, firewall) dan protokol utama Internet.
3. Mampu melakukan troubleshooting dasar secara terstruktur.
4. Memahami istilah industri yang akan ditemui di pekerjaan dan sertifikasi.

**Perbandingan pilihan:**

| Kriteria | OSI 7 lapisan | TCP/IP 4 lapisan | Hibrida 5 lapisan |
| --- | --- | --- | --- |
| Kesesuaian dengan Internet nyata | Rendah; Session/Presentation tidak punya protokol mandiri | Tinggi | Tinggi |
| Membedakan fisik dan data link | Ya | Tidak | Ya |
| Kosakata industri (L2, L3, L7) | Paling lengkap | Kurang | Cocok untuk L1–L4, L7 dipetakan |
| Beban kognitif pemula | Tinggi; dua lapisan abstrak membingungkan | Rendah, tetapi terlalu ringkas di bawah | Sedang |
| Dukungan buku ajar | Banyak (Cisco, sertifikasi) | RFC, dokumentasi IETF | Kurose & Ross, Tanenbaum |

**Manfaat model lima lapisan:**

- Setiap lapisan punya protokol nyata yang bisa dipraktikkan dan dilihat di Wireshark (Ethernet/Wi-Fi, IP, TCP/UDP, HTTP/DNS).
- Memisahkan masalah kabel/sinyal (Physical) dari masalah frame/MAC/VLAN (Link), yang penting untuk troubleshooting.
- Penomoran L1–L4 sama dengan OSI, sehingga istilah "switch L2" atau "router L3" tetap konsisten; L7 cukup dijelaskan sebagai Application.

**Keterbatasan dan cara mengatasinya:**

- Tidak menjelaskan fungsi Session dan Presentation secara eksplisit; solusinya, ajarkan bahwa fungsi tersebut (enkripsi TLS, format data, sesi login) ada di lapisan Application.
- Protokol "di antara lapisan" (TLS, QUIC, ARP, MPLS) tetap perlu pembahasan khusus; jadikan contoh bahwa model adalah alat bantu, bukan aturan mutlak.
- Mahasiswa tetap harus mengenal OSI karena dipakai dalam sertifikasi dan industri; berikan tabel pemetaan OSI ↔ lima lapisan ↔ TCP/IP.

**Kesimpulan:** model lima lapisan memberi keseimbangan terbaik antara kesederhanaan, kesesuaian dengan protokol nyata, dan kemampuan troubleshooting. OSI diajarkan sebagai kosakata dan pembanding, TCP/IP empat lapisan sebagai pengetahuan historis dan standar RFC.

---

## Referensi

1. Kurose, J. F., & Ross, K. W. *Computer Networking: A Top-Down Approach* (edisi ke-8). Pearson.
2. Tanenbaum, A. S., Feamster, N., & Wetherall, D. *Computer Networks* (edisi ke-6). Pearson.
3. ISO/IEC 7498-1:1994. *Information technology — Open Systems Interconnection — Basic Reference Model: The Basic Model*.
4. Braden, R. (Ed.). RFC 1122: *Requirements for Internet Hosts — Communication Layers*. IETF, 1989.
5. Iyengar, J., & Thomson, M. (Eds.). RFC 9000: *QUIC: A UDP-Based Multiplexed and Secure Transport*. IETF, 2021.
6. Bishop, M. (Ed.). RFC 9114: *HTTP/3*. IETF, 2022.
7. Mahalingam, M., et al. RFC 7348: *Virtual eXtensible Local Area Network (VXLAN)*. IETF, 2014.
8. Kent, S. RFC 4303: *IP Encapsulating Security Payload (ESP)*. IETF, 2005.
9. IEEE Std 802.1AE: *Media Access Control (MAC) Security*.
10. Saltzer, J. H., Reed, D. P., & Clark, D. D. (1984). End-to-End Arguments in System Design. *ACM Transactions on Computer Systems*, 2(4), 277–288.
