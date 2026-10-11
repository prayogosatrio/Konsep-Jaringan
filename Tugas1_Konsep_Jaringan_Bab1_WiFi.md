# Tugas 1 Konsep Jaringan — Bab 1 & Standar Protokol Wi-Fi

11 Oktober 2026 · Prayogo Adhi Satrio

## Identitas

| Keterangan | Isi |
| --- | --- |
| Nama | Prayogo Adhi Satrio |
| NRP | 3125600043 |
| Program studi | S1 Teknik Informatika, PENS |
| Mata kuliah | Konsep Jaringan |
| Tugas | Tugas 1 — Latihan Bab 1 + Standar Protokol Teknologi Wi-Fi |

## Level A — Ingatan dan Pemahaman

### 1. Pengertian jaringan komputer dan empat unsur pokoknya

Jaringan komputer adalah kumpulan perangkat otonom yang saling terhubung melalui media transmisi dan bertukar data menurut aturan yang disepakati. Empat unsur pokoknya:

1. **Perangkat (node/host)** — komputer, ponsel, server, printer yang mengirim dan menerima data.
2. **Media transmisi (link)** — kabel tembaga, serat optik, atau gelombang radio yang membawa sinyal.
3. **Protokol** — aturan format, urutan, dan tindakan saat bertukar pesan (mis. TCP/IP, Ethernet, 802.11).
4. **Perangkat antara dan layanan** — switch, router, access point yang meneruskan data, beserta aplikasi/layanan yang memanfaatkan jaringan.

### 2. Perangkat otonom

Perangkat otonom adalah perangkat yang mampu bekerja dan mengambil keputusan sendiri tanpa dikendalikan perangkat lain. Ia punya prosesor, memori, dan sistem operasi sendiri, sehingga tetap berfungsi bila jaringan putus. Contoh: laptop adalah perangkat otonom, sedangkan terminal "bodoh" (dumb terminal) yang sepenuhnya dikendalikan mainframe bukan perangkat otonom. Karena itu, mainframe dengan terminal-terminalnya tidak dianggap jaringan komputer dalam arti sempit.

### 3. Data, sinyal, dan paket

| Istilah | Pengertian | Contoh |
| --- | --- | --- |
| Data | Informasi dalam bentuk digital (bit) yang punya makna bagi aplikasi | Isi file, teks pesan WhatsApp |
| Sinyal | Representasi fisik data yang merambat di media (listrik, cahaya, gelombang radio) | Tegangan pada kabel UTP, gelombang 2,4 GHz pada Wi-Fi |
| Paket | Potongan data yang diberi header (alamat, nomor urut, kontrol) agar bisa dikirim dan diteruskan di jaringan | Paket IP berisi segmen TCP |

Ringkasnya: data adalah *isi*, paket adalah *kemasan* data untuk dikirim, dan sinyal adalah *wujud fisik* saat kemasan itu berpindah di media.

### 4. PAN, LAN, MAN, WAN (tanpa hanya ukuran jarak)

| Jenis | Kepemilikan & pengelolaan | Teknologi khas | Tujuan utama |
| --- | --- | --- | --- |
| PAN | Satu orang | Bluetooth, USB, NFC | Menghubungkan perangkat pribadi (ponsel–earbuds–jam pintar) |
| LAN | Satu organisasi/rumah, dikelola sendiri | Ethernet, Wi-Fi | Berbagi sumber daya dalam satu gedung/kampus dengan kecepatan tinggi dan latensi rendah |
| MAN | Pemerintah kota atau operator, kadang konsorsium | Metro Ethernet, serat optik kota | Menghubungkan beberapa LAN dalam satu kota (mis. antarkampus dalam satu kota) |
| WAN | Umumnya operator telekomunikasi; organisasi menyewa layanan | MPLS, serat optik jarak jauh, satelit | Menghubungkan lokasi antarkota/negara; biaya per bandwidth lebih mahal dan latensi lebih tinggi |

### 5. Intranet, ekstranet, dan Internet publik

- **Intranet**: jaringan privat berbasis teknologi Internet (TCP/IP, web) yang hanya dapat diakses anggota organisasi. Contoh: portal akademik internal kampus.
- **Ekstranet**: bagian intranet yang dibuka secara terkendali untuk pihak luar tertentu, seperti mitra, pemasok, atau pelanggan, biasanya lewat login atau VPN.
- **Internet publik**: jaringan global yang terbuka bagi siapa pun, tersusun dari ribuan jaringan milik banyak pihak tanpa satu pemilik.

Perbedaan utamanya terletak pada **siapa yang boleh mengakses** dan **siapa yang mengendalikan**.

### 6. Mengapa Wi-Fi tidak sama dengan Internet

Wi-Fi hanyalah teknologi akses lokal nirkabel (standar IEEE 802.11) yang menghubungkan perangkat ke access point. Internet adalah jaringan global antarjaringan yang berjalan di atas protokol IP. Seseorang bisa tersambung ke Wi-Fi tetapi tidak mendapat Internet, misalnya bila router tidak punya koneksi ke ISP. Sebaliknya, Internet bisa diakses tanpa Wi-Fi, misalnya lewat kabel LAN atau data seluler 4G/5G.

### 7. Client, server, dan peer

- **Client**: pihak yang meminta layanan, biasanya aktif memulai komunikasi (mis. browser).
- **Server**: pihak yang menyediakan layanan, selalu aktif menunggu permintaan, biasanya beralamat tetap (mis. web server).
- **Peer**: perangkat dalam model P2P yang berperan sekaligus sebagai client dan server, saling berbagi sumber daya secara setara (mis. BitTorrent).

### 8. Bandwidth, throughput, dan goodput

| Istilah | Arti | Contoh |
| --- | --- | --- |
| Bandwidth | Kapasitas maksimum teoretis suatu tautan | Paket ISP 100 Mbps |
| Throughput | Laju data yang benar-benar berhasil lewat pada suatu waktu, termasuk header dan pengiriman ulang | Hasil speed test 70 Mbps |
| Goodput | Laju data **berguna** yang diterima aplikasi, tanpa header, overhead protokol, dan data duplikat | File terunduh efektif 62 Mbps |

Selalu berlaku: goodput ≤ throughput ≤ bandwidth.

### 9. Empat komponen nodal delay

1. **Processing delay** — waktu memeriksa header, cek error, dan menentukan jalur keluar.
2. **Queuing delay** — waktu menunggu di antrean buffer router; bergantung pada kepadatan lalu lintas.
3. **Transmission delay** — waktu mendorong seluruh bit paket ke tautan: L/R (ukuran paket / laju tautan).
4. **Propagation delay** — waktu sinyal merambat dari ujung ke ujung tautan: d/s (jarak / kecepatan rambat).

$$
d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}
$$

### 10. Mengapa Web tidak sama dengan Internet

Internet adalah **infrastruktur** jaringan global (router, tautan, protokol IP). World Wide Web hanyalah salah satu **aplikasi** yang berjalan di atas Internet, menggunakan HTTP/HTTPS, HTML, dan URL. Aplikasi lain di Internet yang bukan Web misalnya email (SMTP/IMAP), DNS, SSH, game online, VoIP, dan transfer file. Analoginya: Internet adalah jalan raya, Web adalah salah satu jenis kendaraan yang lewat.

## Level B — Penerapan dan Analisis

### 11. Transmission delay paket 1.000 byte pada tautan 10 Mbps

Transmission delay ideal = **0,8 ms**.

$$
d_{trans} = \frac{L}{R} = \frac{1000 \times 8 \text{ bit}}{10 \times 10^{6} \text{ bit/s}} = \frac{8000}{10^{7}} \text{ s} = 0{,}0008 \text{ s} = 0{,}8 \text{ ms}
$$

Komponen yang belum tercakup:

- **Propagation delay** — bergantung jarak; misalnya 2.000 km serat optik (≈ 2×10⁸ m/s) menambah ± 10 ms.
- **Queuing delay** — bisa nol saat sepi atau puluhan ms saat buffer router penuh.
- **Processing delay** — pemeriksaan header dan routing di setiap router (mikrodetik).
- Delay ini juga terjadi di **setiap hop**, sehingga dikalikan jumlah router yang dilalui.
- Di luar nodal delay: overhead header/framing (paket aktual > 1.000 byte), retransmisi bila ada error, dan waktu pemrosesan di host pengirim/penerima.

### 12. Kampus 2 Gbps, tetapi satu lantai lambat — hipotesis selain ISP

Karena lantai lain normal, sumber masalah kemungkinan besar ada di jaringan lokal lantai tersebut:

1. **Uplink switch lantai jenuh atau lambat** — switch akses terhubung ke core hanya 100 Mbps/1 Gbps, atau port uplink auto-negotiation turun ke 100 Mbps/half-duplex.
2. **Kabel atau port rusak** — kabel UTP kategori rendah, konektor longgar, sehingga banyak CRC error dan retransmisi.
3. **Access point Wi-Fi kelebihan beban atau interferensi** — terlalu banyak klien per AP, kanal 2,4 GHz bertabrakan dengan AP tetangga, atau AP masih standar lama (802.11n).
4. **Broadcast storm / loop** — ada switch kecil yang dipasang pengguna dan membentuk loop karena STP tidak aktif.
5. **Satu atau beberapa perangkat memonopoli bandwidth** — backup besar, torrent, CCTV yang streaming, atau perangkat terinfeksi malware.
6. **Konfigurasi QoS / rate limit salah** — VLAN lantai itu terkena kebijakan pembatasan atau prioritas rendah.
7. **DHCP/DNS bermasalah** — server DNS yang dipakai VLAN itu lambat, sehingga situs terasa lambat padahal throughput normal.

### 13. Transfer berkas cadangan vs panggilan video

| Metrik | Transfer berkas cadangan | Panggilan video |
| --- | --- | --- |
| Throughput | **Paling penting** — menentukan berapa lama backup selesai | Cukup stabil ± 1–4 Mbps sudah memadai |
| Latency | Tidak kritis; menit atau jam masih bisa diterima | **Sangat penting**; idealnya < 150 ms satu arah |
| Jitter | Tidak berpengaruh | **Penting**; jitter tinggi membuat suara/gambar patah-patah |
| Packet loss | Tidak boleh ada data hilang, tetapi bisa diatasi retransmisi TCP | Loss kecil (< 1%) masih ditoleransi; retransmisi justru tidak berguna |
| Protokol khas | TCP (andal) | UDP/RTP atau QUIC (real-time) |

Kesimpulan: backup mengejar **volume dan keandalan**, video call mengejar **ketepatan waktu**.

### 14. Dua ISP lewat tiang dan ducting yang sama

Redundansinya **lemah** karena hanya redundan secara logis, bukan fisik. Jalur yang sama menjadi *single point of failure*. Satu kejadian, seperti tiang tertabrak, galian proyek yang memutus ducting, kebakaran, atau banjir, akan memutus kedua koneksi sekaligus.

Rekomendasi perbaikan:

- Minta **diversitas jalur (path diversity)** dan titik masuk gedung yang berbeda, mis. satu dari sisi utara, satu dari selatan.
- Pastikan kedua operator tidak berbagi **upstream** atau POP/sentral yang sama.
- Tambahkan media berbeda sebagai cadangan, seperti 4G/5G atau satelit.
- Uji failover secara berkala dan pastikan perangkat router/firewall di sisi kampus juga redundan.

### 15. Mengapa menambah bandwidth tidak selalu mempercepat akses ke server jauh

Waktu akses ditentukan oleh **latensi**, bukan hanya bandwidth. Latensi ke server jauh didominasi propagation delay, yang dibatasi kecepatan cahaya dan tidak bisa diperbaiki dengan membeli bandwidth.

Contoh: server di Amerika berjarak ± 15.000 km dari Surabaya. Propagasi di serat optik ± 75 ms satu arah, sehingga RTT ≥ 150 ms. Membuka halaman web butuh beberapa RTT: DNS, TCP handshake, TLS handshake, lalu permintaan HTTP. Lima RTT saja sudah ≥ 750 ms.

Sementara itu, mengirim objek 100 KB pada 10 Mbps butuh 80 ms dan pada 100 Mbps hanya 8 ms. Bandwidth 10× lipat cuma menghemat 72 ms dari total ± 800 ms. Faktor lain: TCP slow start, ukuran window TCP (bandwidth-delay product), dan antrean di jalur. Solusi yang lebih efektif adalah CDN/cache dekat pengguna, HTTP/2–3 (QUIC), dan mengurangi jumlah round trip.

### 16. Ketersediaan 99,9% vs 99,99%

$$
\text{Downtime}_{99{,}9\%} = (1 - 0{,}999) \times 8760 \text{ jam} = 8{,}76 \text{ jam} \approx 8 \text{ jam } 45 \text{ menit}
$$

$$
\text{Downtime}_{99{,}99\%} = (1 - 0{,}9999) \times 525.600 \text{ menit} = 52{,}56 \text{ menit}
$$

| Target | Downtime maksimum per tahun | Per bulan (± 30 hari) |
| --- | --- | --- |
| 99,9% ("three nines") | ± 8 jam 45 menit | ± 43 menit |
| 99,99% ("four nines") | ± 52,6 menit | ± 4,3 menit |

Menambah satu angka 9 memangkas downtime 10 kali lipat. Target 99,99% praktis menuntut redundansi penuh, failover otomatis, dan pemeliharaan tanpa mematikan layanan, sehingga biayanya jauh lebih tinggi.

### 17. Client–server vs P2P untuk distribusi berkas besar ke ribuan pengguna

| Aspek | Client–server | P2P |
| --- | --- | --- |
| Skalabilitas | Waktu distribusi naik linear dengan jumlah pengguna (server harus mengirim N salinan) | Kapasitas bertambah seiring jumlah peer karena tiap peer ikut mengunggah |
| Beban server/biaya | Tinggi; butuh bandwidth uplink besar atau CDN berbayar | Rendah; beban dibagi ke peer |
| Kendali & keamanan | Mudah dikontrol, autentikasi dan integritas terpusat | Sulit dikontrol; risiko berkas palsu/malware, perlu verifikasi hash |
| Keandalan | Server down = layanan berhenti | Tahan gangguan selama masih ada peer yang memiliki potongan berkas |
| Kinerja awal | Stabil dan dapat diprediksi | Lambat saat peer masih sedikit (perlu seeder awal) |
| Kendala jaringan | Sederhana | Terhambat NAT/firewall dan kebijakan kampus/ISP; memakai uplink pengguna |

Waktu distribusi minimum secara teori (F = ukuran berkas, N = jumlah pengguna, u = kecepatan unggah, d = kecepatan unduh):

$$
D_{cs} \ge \max\left\{ \frac{N F}{u_s}, \frac{F}{d_{min}} \right\} \qquad D_{P2P} \ge \max\left\{ \frac{F}{u_s}, \frac{F}{d_{min}}, \frac{N F}{u_s + \sum u_i} \right\}
$$

Kesimpulan: untuk ribuan pengguna, P2P jauh lebih efisien. Contohnya pembaruan game atau distro Linux via BitTorrent. Client–server tetap dipilih bila kendali, keamanan, dan konsistensi lebih penting, biasanya dibantu CDN.

### 18. Topologi fisik dan logis yang berbeda di kampus

- **Fisik star, logis bus**: semua PC lab terhubung ke satu switch/hub (fisik star). Bila memakai hub, semua frame disebarkan ke semua port sehingga secara logis berperilaku seperti bus satu domain tabrakan.
- **Fisik star, logis terpisah (VLAN)**: PC mahasiswa dan PC staf dicolok ke switch yang sama di satu lantai. Secara logis keduanya berada di VLAN dan subnet berbeda, sehingga tidak bisa saling berkomunikasi tanpa melewati router/firewall.
- **Fisik ring, logis star/point-to-point**: kabel serat antar-gedung dipasang melingkar (ring) untuk redundansi, tetapi STP memblokir satu jalur sehingga lalu lintas mengalir seperti pohon (tree).
- **Wi-Fi**: secara fisik tidak ada kabel ke klien, tetapi secara logis semua klien di SSID yang sama menjadi bagian dari satu LAN/VLAN yang sama.

## Level C — Evaluasi dan Sintesis

### 19. Klasifikasi dan segmentasi jaringan kampus

Setiap kelompok pengguna ditempatkan di VLAN/subnet sendiri dan dipisahkan firewall. Alasannya: membatasi penyebaran serangan (blast radius), memudahkan QoS, dan menerapkan kebijakan akses sesuai kebutuhan.

| Segmen | Kebutuhan utama | Boleh mengakses | Dilarang / dibatasi |
| --- | --- | --- | --- |
| Mahasiswa | Internet, e-learning, Wi-Fi luas, kapasitas besar | Internet, portal akademik, server e-learning | Jaringan staf, CCTV, server riset; bandwidth per pengguna dibatasi |
| Staf administrasi | Keandalan tinggi, data sensitif (keuangan, nilai) | Server SIAKAD/keuangan, Internet, printer staf | Akses masuk dari segmen mahasiswa dan tamu |
| Tamu | Internet saja, mudah didaftarkan (captive portal) | Internet saja | Semua sumber daya internal; isolasi antarklien (client isolation) |
| Kamera pengawas (CCTV) | Bandwidth stabil ke NVR, keamanan perangkat IoT | Hanya NVR/server rekaman | Internet dan segmen lain; hanya admin keamanan yang boleh melihat |
| Laboratorium riset | Throughput tinggi, kebebasan eksperimen, kadang IP publik | Internet, server riset, HPC | Tidak boleh masuk ke jaringan staf; eksperimen diisolasi dalam sandbox |

Aturan umum: *default deny* antarsegmen, hanya lalu lintas yang dibutuhkan yang diizinkan, autentikasi 802.1X/WPA-Enterprise untuk mahasiswa dan staf, serta log terpusat.

### 20. "Jaringan internal tidak memerlukan enkripsi karena sudah dilindungi firewall"

Pernyataan ini **keliru**. Firewall hanya menjaga perbatasan, sedangkan banyak ancaman berasal dari dalam atau berhasil masuk.

- **Kerahasiaan (confidentiality)**: tanpa enkripsi, siapa pun di jaringan internal — karyawan iseng, laptop terinfeksi, penyusup yang menembus firewall — bisa menyadap kata sandi dan data sensitif dengan sniffing atau ARP spoofing. Wi-Fi internal juga bisa ditangkap dari luar gedung.
- **Integritas (integrity)**: tanpa enkripsi dan autentikasi pesan, penyerang bisa melakukan *man-in-the-middle* dan mengubah data di tengah jalan, misalnya mengubah nilai atau nominal transfer, tanpa terdeteksi.
- **Ketersediaan (availability)**: penyerang di dalam dapat membajak sesi atau menyusupkan malware yang menyebar lateral, lalu mematikan layanan (mis. ransomware). Firewall perimeter tidak melihat lalu lintas antarhost di segmen yang sama.

Kesimpulan: terapkan prinsip **zero trust** dan *defense in depth* — HTTPS/TLS untuk aplikasi internal, SSH bukan Telnet, WPA3 untuk Wi-Fi, segmentasi, dan pemantauan internal.

### 21. Mengapa Internet bisa berkembang tanpa otoritas teknis pusat

Internet adalah "jaringan dari jaringan". Setiap operator (Autonomous System) mengelola jaringannya sendiri dan saling terhubung secara sukarela lewat perjanjian peering/transit dan protokol terbuka seperti BGP. Standar disusun secara terbuka oleh IETF (RFC) berdasarkan *rough consensus and running code*. Koordinasi yang ada hanya untuk sumber daya unik: ICANN/IANA dan RIR (APNIC, RIPE, ARIN, dll.) membagikan alamat IP, nomor AS, dan zona root DNS. Prinsip *end-to-end* membuat inovasi bisa dilakukan di tepi jaringan tanpa izin siapa pun.

| Manfaat | Risiko |
| --- | --- |
| Skalabilitas tinggi; jaringan baru tinggal bergabung | Tidak ada pihak yang wajib menjamin keamanan; misalnya BGP hijacking dan route leak |
| Tahan gangguan; tidak ada satu titik kegagalan pusat | Migrasi teknologi lambat karena butuh kesepakatan semua pihak (contoh: IPv6, RPKI, DNSSEC) |
| Inovasi cepat tanpa izin (permissionless innovation) | Kualitas layanan tidak seragam antarwilayah/operator |
| Netral terhadap vendor dan negara | Penegakan hukum lintas negara sulit; fragmentasi bila negara membuat aturan sendiri |

### 22. Circuit switching vs packet switching untuk suara

| Aspek | Circuit switching (PSTN) | Packet switching (VoIP) |
| --- | --- | --- |
| Sumber daya | Jalur khusus dicadangkan sepanjang panggilan (mis. 64 kbps) | Dibagi bersama; dipakai hanya saat ada data |
| Kualitas | Delay konstan, tanpa jitter, kualitas terjamin | Delay bervariasi; bisa terkena jitter dan packet loss |
| Efisiensi | Boros; kapasitas tetap terpakai saat diam | Efisien; jeda bicara tidak memakai bandwidth |
| Biaya & fleksibilitas | Mahal, hanya suara | Murah, bisa digabung video, chat, data |

Suara modern tetap berjalan baik di jaringan paket karena:

- **Codec efisien dan tahan loss** (Opus, AMR-WB) dengan *packet loss concealment*.
- **Jitter buffer** di penerima menyamakan waktu kedatangan paket.
- **Transport real-time** (RTP di atas UDP) tanpa retransmisi yang menambah delay.
- **QoS/DiffServ** (penandaan DSCP EF) memprioritaskan paket suara di router; di seluler, VoLTE/VoNR mendapat bearer khusus.
- **Bandwidth melimpah dan latensi rendah** pada jaringan modern, sehingga antrean jarang terjadi.

### 23. Prosedur menangani keluhan "Internet lambat"

Contoh keluhan: "Wi-Fi di Lab B lantai 3 lambat setiap siang."

1. **Perjelas keluhan** — siapa, di mana, kapan, aplikasi apa, sejak kapan, apakah semua pengguna terdampak. Ubah "lambat" menjadi gejala terukur (halaman lama terbuka? video buffering? upload gagal?).
2. **Kumpulkan bukti baseline**
   - Speed test ke server lokal dan luar negeri (throughput unduh/unggah).
   - `ping` dan `traceroute`/`mtr` ke gateway, DNS, dan situs tujuan (latensi, loss, hop bermasalah).
   - Waktu resolusi DNS (`nslookup`/`dig`).
   - Data perangkat: utilisasi uplink switch/AP dan link ISP (SNMP/grafik), jumlah klien per AP, RSSI/SNR, error interface.
   - Bandingkan dengan lokasi lain dan jam lain.
3. **Susun hipotesis** — AP penuh/interferensi, uplink jenuh, DNS lambat, satu pengguna memonopoli bandwidth, ISP padat.
4. **Uji hipotesis satu per satu** — tes kabel vs Wi-Fi (bila kabel cepat → masalah Wi-Fi); tes di jam sepi vs ramai (bila hanya jam ramai → kapasitas); ganti DNS; lihat top talkers via NetFlow; tes langsung di router tepi (bila tetap lambat → ISP).
5. **Terapkan perbaikan** satu perubahan pada satu waktu, catat di log perubahan.
6. **Kriteria keberhasilan** (ditetapkan sebelum perbaikan), misalnya:
   - Throughput per pengguna ≥ 20 Mbps pada jam sibuk.
   - Latensi ke gateway < 10 ms dan ke server nasional < 50 ms; packet loss < 1%.
   - Utilisasi uplink puncak < 70%.
   - Tidak ada keluhan berulang selama 2 minggu, dan pengguna mengonfirmasi perbaikan.

### 24. Statistik IPv6 Indonesia: Google vs APNIC

Data APNIC Labs dicatat pada 11 Oktober 2026 (pembaruan terakhir 8 Oktober 2026). Nilai Google ditampilkan di peta interaktif per negara dan perlu dicatat langsung dari halamannya.

| Keterangan | APNIC Labs | Google IPv6 Statistics |
| --- | --- | --- |
| Tanggal data | 8 Oktober 2026 (rata-rata 30 hari) | *(isi tanggal saat mengunjungi)* |
| Definisi metrik | **IPv6 capable**: persentase pengguna yang berhasil mengambil objek uji lewat IPv6. **IPv6 preferred**: persentase yang memilih IPv6 ketika IPv4 dan IPv6 sama-sama tersedia (dual-stack). | Persentase pengguna yang **mengakses layanan Google melalui IPv6** |
| Populasi yang diukur | Pengguna yang menampilkan iklan online berisi skrip uji APNIC (sampel ± 1,4 juta tes per hari untuk Indonesia), lalu diboboti menurut estimasi pengguna Internet per jaringan (ASN) | Pengguna yang mengakses Google (Search, YouTube, dll.) dari Indonesia |
| Nilai Indonesia | **IPv6 capable 28,7%**, **IPv6 preferred 27,9%** | *(isi dari peta Per-Country)* |

Mengapa angka kedua sumber bisa berbeda:

- **Definisi metrik berbeda** — APNIC mengukur *kemampuan* IPv6, Google mengukur *penggunaan nyata* ke layanannya.
- **Populasi sampel berbeda** — penonton iklan vs pengguna Google; komposisi seluler vs fixed broadband bisa tidak sama.
- **Metode pembobotan** — APNIC membobot per ASN berdasarkan estimasi jumlah pengguna; Google memakai jumlah koneksi aktual.
- **Periode dan smoothing** — APNIC memakai rata-rata 30 hari; Google rata-rata harian/mingguan.
- **Perilaku klien** — aplikasi dan sistem operasi (Happy Eyeballs) bisa memilih IPv4 walau IPv6 tersedia; aplikasi Google di Android juga bisa berbeda dari browser.

### 25. Satelit orbit rendah (LEO) untuk kampus terpencil

Argumen: LEO (mis. Starlink) **layak sebagai koneksi utama** bila tidak ada serat optik/microwave terestrial, tetapi **ideal sebagai cadangan** atau dipadukan dengan koneksi lain bila tersedia.

| Kriteria | Penilaian |
| --- | --- |
| Kinerja | Latensi ± 25–60 ms (jauh lebih baik dari satelit GEO ± 600 ms); unduh ± 50–250 Mbps per terminal. Kapasitas dibagi dengan pengguna lain di sel yang sama, sehingga tidak dijamin untuk ratusan mahasiswa sekaligus. |
| Biaya | Investasi terminal murah dan cepat dipasang (hari, bukan bulan). Biaya bulanan per Mbps lebih tinggi dari serat; perlu beberapa terminal untuk kapasitas kampus. |
| Ketergantungan cuaca | Hujan lebat (rain fade pada Ku/Ka-band) menurunkan kecepatan atau memutus sementara — penting di Indonesia yang curah hujannya tinggi. Butuh pandangan langit terbuka tanpa halangan. |
| Pengelolaan | Sederhana, plug-and-play. Kendala: CGNAT (tanpa IP publik), kendali terbatas atas routing/QoS, dan bergantung pada satu operator asing. |
| Keamanan | Lalu lintas melewati infrastruktur dan gateway pihak ketiga, sering di luar negeri; ada isu kedaulatan data dan regulasi. Wajib memakai VPN terenkripsi ke kampus induk dan firewall lokal. |

Rekomendasi: pakai LEO dengan **SD-WAN/failover** ke koneksi lain (radio microwave, 4G/5G, atau GEO), cache lokal untuk konten e-learning, dan SLA yang jelas.

### 26. Otomatisasi jaringan: konsistensi vs dampak kesalahan

**Meningkatkan konsistensi**: konfigurasi dibuat dari template dan *source of truth* yang sama (Ansible, Terraform, NETCONF), sehingga ratusan switch memiliki konfigurasi seragam, bebas typo manual, dapat diaudit, dan cepat diterapkan.

**Memperbesar dampak kesalahan**: satu bug di template atau variabel yang salah langsung tersebar ke semua perangkat dalam hitungan detik. Contoh: satu ACL salah dapat memutus seluruh kampus sekaligus, bukan hanya satu switch.

Kontrol untuk mengurangi risiko:

| Jenis | Kontrol |
| --- | --- |
| Teknis | Version control (Git) untuk semua konfigurasi; validasi otomatis dan linting; uji di lab/emulator (GNS3, Containerlab) atau *digital twin*; dry-run dan diff sebelum deploy; *staged/canary rollout* (1 perangkat → 1 gedung → semua); rollback otomatis atau *commit confirmed*; akses out-of-band; pemantauan pasca-perubahan |
| Proses | Peer review/pull request sebelum merge; prosedur change management dan jadwal maintenance window; prinsip *least privilege* untuk akun otomasi; runbook dan rencana rollback; dokumentasi serta post-incident review tanpa menyalahkan (blameless) |

## Standar Protokol pada Teknologi Wi-Fi

Wi-Fi adalah nama dagang dari Wi-Fi Alliance untuk produk yang lulus sertifikasi standar **IEEE 802.11**. Standar ini hanya mengatur dua lapisan terbawah model OSI: **Physical layer (PHY)** — frekuensi, modulasi, lebar kanal — dan **Data Link layer bagian MAC** — cara perangkat berbagi medium radio. Lapisan di atasnya (IP, TCP/UDP, HTTP) sama persis seperti pada jaringan kabel.

### Generasi standar IEEE 802.11

| Standar | Nama Wi-Fi Alliance | Tahun | Frekuensi | Kecepatan maks. teoretis | Teknologi kunci |
| --- | --- | --- | --- | --- | --- |
| 802.11bn | Wi-Fi 8 | Dalam pengembangan (target ± 2028) | 2,4 / 5 / 6 GHz | Fokus keandalan, bukan kecepatan | Ultra High Reliability (UHR): latensi lebih rendah dan stabil, koordinasi antar-AP |
| 802.11be | Wi-Fi 7 | 2024 | 2,4 / 5 / 6 GHz | ± 46 Gbps | Kanal 320 MHz, 4096-QAM, Multi-Link Operation (MLO) |
| 802.11ax | Wi-Fi 6 / 6E | 2019–2021 (6E: +6 GHz) | 2,4 / 5 (/ 6) GHz | ± 9,6 Gbps | OFDMA, MU-MIMO dua arah, 1024-QAM, Target Wake Time, BSS coloring |
| 802.11ac | Wi-Fi 5 | 2013 | 5 GHz | ± 6,9 Gbps | Kanal 80/160 MHz, 256-QAM, MU-MIMO downlink, beamforming |
| 802.11n | Wi-Fi 4 | 2009 | 2,4 / 5 GHz | 600 Mbps | MIMO hingga 4×4, kanal 40 MHz, frame aggregation |
| 802.11g | (Wi-Fi 3, tidak resmi) | 2003 | 2,4 GHz | 54 Mbps | OFDM di 2,4 GHz, kompatibel dengan 802.11b |
| 802.11a | (Wi-Fi 2, tidak resmi) | 1999 | 5 GHz | 54 Mbps | OFDM |
| 802.11b | (Wi-Fi 1, tidak resmi) | 1999 | 2,4 GHz | 11 Mbps | DSSS/CCK |
| 802.11 (asli) | — | 1997 | 2,4 GHz | 2 Mbps | FHSS/DSSS, inframerah |

Tren antargenerasi: kanal makin lebar, modulasi makin rapat (QAM lebih tinggi), lebih banyak antena (MIMO), dan sejak Wi-Fi 6 fokus bergeser ke **efisiensi saat banyak pengguna** (OFDMA) serta keandalan (Wi-Fi 7 dan 8).

### Protokol akses medium (MAC): CSMA/CA

Radio tidak dapat mendeteksi tabrakan sambil mengirim, sehingga Wi-Fi memakai **CSMA/CA** (*Carrier Sense Multiple Access with Collision Avoidance*), bukan CSMA/CD seperti Ethernet lama:

1. Stasiun mendengarkan kanal; bila sibuk, ia menunggu.
2. Setelah kanal kosong selama DIFS, stasiun menunggu lagi *random backoff* untuk menghindari tabrakan.
3. Frame dikirim; penerima membalas **ACK**. Tanpa ACK, frame dikirim ulang dengan backoff lebih panjang.
4. Opsional **RTS/CTS** untuk mengatasi masalah *hidden terminal* (dua stasiun yang tidak saling dengar tetapi sama-sama dekat ke AP).

Jenis frame 802.11: **management** (beacon, probe, authentication, association), **control** (RTS, CTS, ACK), dan **data**.

### Standar keamanan Wi-Fi

| Standar | Tahun | Enkripsi / autentikasi | Status |
| --- | --- | --- | --- |
| WPA3 | 2018 | SAE (Dragonfly) menggantikan PSK, wajib Protected Management Frames, mode Enterprise 192-bit, Enhanced Open (OWE) untuk Wi-Fi publik | Direkomendasikan; wajib untuk Wi-Fi 6E/7 |
| WPA2 (802.11i) | 2004 | AES-CCMP; Personal (PSK) atau Enterprise (802.1X/EAP + RADIUS) | Masih umum; rentan serangan KRACK dan tebak kata sandi offline |
| WPA | 2003 | TKIP (masih berbasis RC4) | Usang, tidak aman |
| WEP | 1997 | RC4 kunci statis 40/104-bit | Rusak total, dapat dibobol dalam menit |

Untuk kampus, praktik terbaik adalah **WPA2/WPA3-Enterprise dengan 802.1X** (contoh: eduroam), sehingga setiap pengguna login dengan akun masing-masing, bukan satu kata sandi bersama.

### Amandemen pendukung 802.11

| Amandemen | Fungsi |
| --- | --- |
| 802.11e | QoS untuk suara/video (di sertifikasi Wi-Fi disebut WMM) |
| 802.11k / 802.11v / 802.11r | Roaming cepat dan cerdas antar-AP (informasi AP tetangga, manajemen jaringan, fast BSS transition) |
| 802.11w | Proteksi management frame terhadap serangan deauthentication |
| 802.11u | Interworking dengan jaringan luar; dasar Hotspot 2.0/Passpoint |
| 802.11s | Jaringan mesh antar-AP |
| 802.11ah (Wi-Fi HaLow) | Frekuensi di bawah 1 GHz, jangkauan jauh dan hemat daya untuk IoT |
| 802.11ad / 802.11ay (WiGig) | Pita 60 GHz, multi-gigabit untuk jarak sangat pendek |
| 802.11p | Komunikasi antarkendaraan (V2X/DSRC) |

## Referensi

1. Kurose, J. F., & Ross, K. W. *Computer Networking: A Top-Down Approach* (edisi ke-8). Pearson. — konsep delay, packet/circuit switching, client–server vs P2P.
2. APNIC Labs. [IPv6 Capability Metrics — Indonesia (ID)](https://stats.labs.apnic.net/ipv6/ID), diakses 11 Oktober 2026; data mentah: [ID.json](https://data1.labs.apnic.net/v6stats/v6economy/ID.json).
3. Google. [IPv6 Statistics](https://www.google.com/intl/en/ipv6/statistics.html), diakses 11 Oktober 2026.
4. APNIC Blog. [NIR updates at APRICOT 2026: IPv6 progress, RPKI plans, and strengthening coordination](https://blog.apnic.net/2026/03/06/nir-updates-at-apricot-2026-ipv6-progress-rpki-plans-and-strengthening-coordination/), 6 Maret 2026.
5. IEEE. IEEE Std 802.11 — Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications, beserta amandemen 802.11n/ac/ax/be.
6. Wi-Fi Alliance. Dokumentasi Wi-Fi CERTIFIED (Wi-Fi 6, Wi-Fi 6E, Wi-Fi 7, WPA3).
