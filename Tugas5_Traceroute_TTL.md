# KONSEP JARINGAN
## Tugas 5 — Analisis Cara Kerja Traceroute dan Mekanisme TTL

**DOSEN:**  
Dr. Ferry Astika Saputra, ST, M.Sc. (197708232001121002)

**PENYUSUN:**  
Prayogo Adhi Satrio (3125600043)

**PROGRAM STUDI SARJANA TERAPAN TEKNIK INFORMATIKA**  
**POLITEKNIK ELEKTRONIKA NEGERI SURABAYA**

---

## 1. Mekanisme Time To Live (TTL)

### 1.1 Pengertian

**Time To Live (TTL)** adalah field 8 bit pada header IPv4 yang membatasi berapa lama sebuah paket boleh "hidup" di jaringan. Pada IPv6, field yang sama bernama **Hop Limit**. Karena panjangnya 8 bit, nilai TTL berkisar 0–255.

Posisi TTL di header IPv4 (byte ke-9):

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-------+-------+---------------+-------------------------------+
|Version|  IHL  |      DSCP/ECN |          Total Length         |
+-------+-------+---------------+-----+-------------------------+
|         Identification        |Flags|     Fragment Offset     |
+---------------+---------------+-----+-------------------------+
|  >> TTL <<    |   Protocol    |        Header Checksum        |
+---------------+---------------+-------------------------------+
|                       Source IP Address                       |
+---------------------------------------------------------------+
|                    Destination IP Address                     |
+---------------------------------------------------------------+
```

Dalam RFC 791 TTL awalnya dimaksudkan dalam satuan detik. Dalam praktiknya, setiap router menguranginya 1 per hop, sehingga TTL sekarang berarti **jumlah maksimum router (hop) yang boleh dilewati**.

### 1.2 Tujuan TTL

- **Mencegah paket berputar tanpa akhir (routing loop).** Bila tabel routing salah sehingga dua router saling melempar paket, paket akan mati setelah TTL habis, alih-alih memenuhi jaringan selamanya.
- **Membatasi jangkauan paket.** Misalnya paket multicast dengan TTL kecil hanya beredar di jaringan lokal.
- **Menjadi dasar alat diagnosis** seperti traceroute.

### 1.3 Cara kerja TTL

1. **Inisialisasi** — sistem operasi pengirim mengisi nilai TTL awal.
2. **Dekremen** — setiap router yang meneruskan paket mengurangi TTL sebesar 1, lalu menghitung ulang header checksum (karena isi header berubah).
3. **Paket mati** — bila TTL menjadi 0, router **membuang** paket dan mengirim pesan **ICMP Time Exceeded (Type 11, Code 0)** ke alamat IP pengirim. Pesan ini berisi salinan header IP asli ditambah 8 byte pertama payload-nya, sehingga pengirim tahu paket mana yang mati.

Nilai TTL awal bawaan beberapa sistem operasi:

| Sistem operasi / perangkat | TTL awal |
| :--- | :---: |
| Linux, Android, macOS, iOS | 64 |
| Windows | 128 |
| Router Cisco, sebagian perangkat jaringan | 255 |

### 1.4 Menebak jumlah hop dari TTL balasan

Nilai TTL pada paket balasan bisa dipakai untuk memperkirakan jarak dan jenis OS lawan bicara. Contoh: `ping` ke sebuah server menampilkan `TTL=117`. Nilai awal terdekat di atas 117 adalah 128 (Windows), sehingga paket balasan sudah melewati:

$$
128 - 117 = 11 \text{ hop}
$$

Bila balasan menunjukkan `TTL=54`, kemungkinan nilai awalnya 64 (Linux), sehingga jaraknya $64 - 54 = 10$ hop. Perkiraan ini tidak selalu tepat karena TTL awal bisa diubah administrator dan jalur pergi-pulang bisa berbeda.

---

## 2. Cara Kerja Traceroute

### 2.1 Ide dasar

Traceroute (ditulis Van Jacobson, 1987) **sengaja mengirim paket dengan TTL kecil** agar paket "mati" di setiap router secara berurutan. Setiap router yang membuang paket akan membalas ICMP Time Exceeded, sehingga alamat IP router tersebut terungkap. Dengan menaikkan TTL satu per satu, seluruh jalur dari pengirim ke tujuan dapat dipetakan.

### 2.2 Langkah demi langkah

Misal jalur: **PC → R1 → R2 → R3 → Server**.

```
 PC                R1               R2               R3             Server
  |  TTL=1          |                |                |                |
  |---------------->| TTL 1→0, buang |                |                |
  |<----------------| ICMP 11 (Time Exceeded) dari R1  |                |
  |                 |                |                |                |
  |  TTL=2          |  TTL=1         |                |                |
  |---------------->|--------------->| TTL 1→0, buang |                |
  |<---------------------------------| ICMP 11 dari R2                 |
  |                 |                |                |                |
  |  TTL=3          |  TTL=2         |  TTL=1         |                |
  |---------------->|--------------->|--------------->| TTL 1→0, buang |
  |<--------------------------------------------------| ICMP 11 dari R3|
  |                 |                |                |                |
  |  TTL=4          |  TTL=3         |  TTL=2         |  TTL=1         |
  |---------------->|--------------->|--------------->|--------------->| sampai tujuan
  |<-------------------------------------------------------------------| ICMP 3/3 atau
  |                 |                |                |                | ICMP 0 (Echo Reply)
```

| Putaran | TTL probe | Router yang membuang | Balasan yang diterima | Yang dicatat traceroute |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 1 | R1 | ICMP Time Exceeded (11/0) | Hop 1 = IP R1 + RTT |
| 2 | 2 | R2 | ICMP Time Exceeded (11/0) | Hop 2 = IP R2 + RTT |
| 3 | 3 | R3 | ICMP Time Exceeded (11/0) | Hop 3 = IP R3 + RTT |
| 4 | 4 | — (sampai server) | ICMP Port Unreachable (3/3) atau Echo Reply (0/0) | Hop 4 = server tujuan, **traceroute berhenti** |

Detail tambahan:

- Setiap hop diuji **3 kali** (3 probe), sehingga muncul tiga nilai waktu per baris.
- **RTT (Round Trip Time)** = selisih waktu antara probe dikirim dan balasan ICMP diterima.
- Traceroute berhenti bila menerima balasan dari tujuan atau mencapai batas maksimum hop (umumnya 30; macOS 64).
- Traceroute mencocokkan balasan dengan probe-nya menggunakan header asli yang disalin di dalam pesan ICMP (port UDP atau ID/sequence ICMP).

### 2.3 Jenis probe pada tiap sistem operasi

| Perintah | Jenis probe default | Balasan dari tujuan akhir | Catatan |
| :--- | :--- | :--- | :--- |
| `tracert` (Windows) | ICMP Echo Request | ICMP Echo Reply (Type 0) | Opsi `-d` mematikan pencarian nama (DNS) agar lebih cepat |
| `traceroute` (Linux, macOS) | UDP ke port tinggi, mulai 33434 dan bertambah tiap probe | ICMP Port Unreachable (Type 3, Code 3) karena port itu tidak dipakai layanan apa pun | Opsi `-I` memakai ICMP, `-T` (Linux) memakai TCP SYN |
| `tcptraceroute` / `traceroute -T -p 443` | TCP SYN ke port layanan (80/443) | TCP SYN-ACK atau RST | Berguna bila firewall memblokir UDP/ICMP tetapi membuka port web |
| `mtr` / `pathping` (Windows) | ICMP (bisa diganti) | Echo Reply | Menggabungkan traceroute dan ping berulang; menampilkan persentase loss per hop |

### 2.4 Pesan ICMP yang terlibat

| Type / Code | Nama | Dikirim oleh | Arti bagi traceroute |
| :--- | :--- | :--- | :--- |
| 11 / 0 | Time Exceeded — TTL exceeded in transit | Router perantara | Hop ditemukan; lanjut ke TTL berikutnya |
| 3 / 3 | Destination Unreachable — Port Unreachable | Host tujuan (probe UDP) | Tujuan tercapai, selesai |
| 0 / 0 | Echo Reply | Host tujuan (probe ICMP) | Tujuan tercapai, selesai |
| 3 / 0, 3 / 1 | Network / Host Unreachable | Router | Ditampilkan `!N` / `!H`; tidak ada rute ke tujuan |
| 3 / 13 | Communication Administratively Prohibited | Router/firewall | Ditampilkan `!X`; diblokir oleh kebijakan (ACL) |

Pada IPv6, mekanismenya sama memakai field **Hop Limit** dan **ICMPv6 Time Exceeded (Type 3)**.

---

## 3. Analisis Output Traceroute

### 3.1 Contoh output (ilustrasi)

> Output berikut adalah **contoh ilustrasi** untuk menjelaskan cara membaca hasil traceroute. Alamat IP router perantara memakai rentang privat dan rentang dokumentasi (RFC 5737), bukan hasil pengukuran nyata.

```
$ traceroute -n 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 64 hops max, 52 byte packets
 1  192.168.1.1     2.104 ms   1.873 ms   1.902 ms
 2  10.20.0.1       8.512 ms   7.940 ms   9.021 ms
 3  198.51.100.9   12.330 ms  11.876 ms  12.004 ms
 4  * * *
 5  198.51.100.77  15.442 ms  45.910 ms  14.998 ms
 6  203.0.113.21   24.105 ms  23.880 ms  24.317 ms
 7  203.0.113.65   23.902 ms  24.511 ms  23.770 ms
 8  8.8.8.8        24.016 ms  23.954 ms  24.233 ms
```

### 3.2 Pembacaan per hop

| Hop | Alamat | Analisis |
| :---: | :--- | :--- |
| 1 | 192.168.1.1 | Router Wi-Fi/rumah (default gateway). RTT ± 2 ms wajar untuk jaringan lokal. |
| 2 | 10.20.0.1 | Alamat privat milik jaringan ISP (mis. perangkat akses atau CGNAT). Kenaikan ke ± 8 ms adalah latensi jaringan akses ISP. |
| 3 | 198.51.100.9 | Router di jaringan inti ISP. |
| 4 | `* * *` | Router tidak membalas ICMP Time Exceeded (dibatasi/diblokir). Jalur **tidak putus**, karena hop 5 dan seterusnya tetap membalas. |
| 5 | 198.51.100.77 | Satu probe bernilai 45,9 ms, sementara dua lainnya ± 15 ms. Ini lonjakan sesaat (antrean atau rate-limiting ICMP di router), bukan masalah jalur. |
| 6–7 | 203.0.113.x | Router di jaringan penyedia konten/backbone. RTT naik ke ± 24 ms karena jarak fisik (keluar dari jaringan ISP). |
| 8 | 8.8.8.8 | Tujuan tercapai; RTT ± 24 ms sama dengan hop 6–7, artinya tidak ada tambahan delay berarti di ujung jalur. |

Total jalur: **8 hop**, latensi akhir ± 24 ms.

### 3.3 Panduan interpretasi

| Gejala pada output | Arti yang benar | Kesalahan tafsir yang umum |
| :--- | :--- | :--- |
| `* * *` di satu hop, hop berikutnya normal | Router itu tidak mau membalas ICMP (kebijakan keamanan atau rate-limit) | "Jaringan putus di hop itu" — salah, karena paket tetap diteruskan |
| `* * *` terus sampai batas hop | Paket benar-benar tidak sampai, atau tujuan/firewall memblokir probe | — |
| RTT hop tengah tinggi, tetapi hop sesudahnya rendah | Router memprioritaskan meneruskan paket; membuat balasan ICMP diproses belakangan oleh CPU router (control plane) | "Router itu lambat dan menghambat" — salah bila hop sesudahnya normal |
| RTT naik dan **tetap** tinggi di semua hop sesudahnya | Latensi nyata bertambah di titik itu: jarak jauh (mis. kabel bawah laut) atau kemacetan | — |
| Satu hop menampilkan dua atau tiga IP berbeda | Load balancing (ECMP): tiap probe bisa lewat jalur paralel berbeda | "Rute berubah-ubah/rusak" |
| Alamat privat (10.x, 172.16–31.x, 192.168.x, 100.64.x) di hop awal | Jaringan internal rumah/kampus atau CGNAT milik ISP | — |
| Hop terakhir sama dengan tujuan tetapi muncul `!X` atau `!H` | Ada ACL/firewall atau host tidak terjangkau | — |

Keterbatasan traceroute yang perlu diingat:

- Traceroute hanya menampilkan **jalur pergi**. Jalur pulang (balasan ICMP) bisa melewati router berbeda (asymmetric routing), padahal RTT dihitung pergi-pulang.
- Router dalam **tunnel MPLS** bisa tersembunyi sehingga beberapa router terlihat seperti satu hop.
- Alamat yang tampil adalah **interface masuk** router yang mengirim balasan, bukan identitas router secara keseluruhan.

---

## 4. Langkah Praktikum

| Sistem | Perintah |
| :--- | :--- |
| Windows (Command Prompt) | `tracert -d 8.8.8.8` dan `tracert www.pens.ac.id` |
| macOS (Terminal) | `traceroute -n 8.8.8.8` (UDP) dan `traceroute -I -n 8.8.8.8` (ICMP) |
| Linux | `traceroute -n 8.8.8.8`, `traceroute -I 8.8.8.8`, `sudo traceroute -T -p 443 8.8.8.8` |
| Melihat TTL lewat ping | `ping -c 4 8.8.8.8` (Linux/macOS) atau `ping 8.8.8.8` (Windows), lalu baca nilai `ttl=` |

Mengamati mekanisme TTL dengan **Wireshark** saat traceroute berjalan:

1. Mulai capture pada interface Wi-Fi/Ethernet.
2. Jalankan traceroute.
3. Gunakan display filter `icmp.type == 11 || icmp.type == 3 || icmp.type == 0`.
4. Klik probe yang dikirim: pada **Internet Protocol → Time to Live**, nilai TTL terlihat naik 1, 2, 3, ...
5. Klik balasan ICMP Time Exceeded: di dalamnya terdapat salinan header IP probe asli dengan TTL bernilai 1 saat tiba di router itu.

Pembanding perintah `ping` dengan TTL tertentu (membuktikan cara kerja traceroute secara manual):

```
ping -c 1 -m 1 8.8.8.8      # macOS: -m = TTL. Balasan "Time to live exceeded" dari hop 1
ping -c 1 -t 1 8.8.8.8      # Linux: -t = TTL
ping -n 1 -i 1 8.8.8.8      # Windows: -i = TTL
```

Dengan menaikkan nilai TTL satu per satu pada perintah di atas, kita melakukan traceroute "secara manual".

---

## 5. Kesimpulan

- TTL adalah penghitung mundur jumlah hop di header IP. Setiap router menguranginya 1; ketika mencapai 0, paket dibuang dan router mengirim ICMP Time Exceeded ke pengirim. Mekanisme ini melindungi jaringan dari routing loop.
- Traceroute memanfaatkan perilaku tersebut dengan mengirim probe ber-TTL 1, 2, 3, ... sehingga setiap router di jalur "terpaksa" memperkenalkan dirinya lewat pesan ICMP.
- Akhir jalur dikenali dari jenis balasan yang berbeda: ICMP Port Unreachable (probe UDP) atau ICMP Echo Reply (probe ICMP).
- Output traceroute harus ditafsirkan dengan hati-hati: tanda `*` atau RTT tinggi pada satu hop belum tentu berarti ada gangguan, selama hop-hop sesudahnya normal.

## Referensi

1. Postel, J. RFC 791: *Internet Protocol*. IETF, 1981.
2. Postel, J. RFC 792: *Internet Control Message Protocol*. IETF, 1981.
3. Deering, S., & Hinden, R. RFC 8200: *Internet Protocol, Version 6 (IPv6) Specification*. IETF, 2017.
4. Arkko, J., Cotton, M., & Vegoda, L. RFC 5737: *IPv4 Address Blocks Reserved for Documentation*. IETF, 2010.
5. Kurose, J. F., & Ross, K. W. *Computer Networking: A Top-Down Approach* (edisi ke-8). Pearson. Subbab 1.4 (Traceroute) dan 5.6 (ICMP).
