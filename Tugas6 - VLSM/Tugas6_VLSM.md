# KONSEP JARINGAN
## Tugas 6 — Perancangan Pengalamatan IP dengan VLSM

**DOSEN:**  
Dr. Ferry Astika Saputra, ST, M.Sc. (197708232001121002)

**PENYUSUN:**  
Prayogo Adhi Satrio (3125600043)

**PROGRAM STUDI SARJANA TERAPAN TEKNIK INFORMATIKA**  
**POLITEKNIK ELEKTRONIKA NEGERI SURABAYA**

---

## Soal

Network **10.252.108.0/24** dibagi untuk empat segmen dengan kebutuhan host berbeda:

| Segmen | Kebutuhan host |
| :--- | ---: |
| Lab A | 90 |
| Lab B | 60 |
| Administrasi | 14 |
| End-point | 2 |
| **Total** | **166** |

## Hasil Akhir (Ringkasan)

| Segmen | Butuh | Prefix | Subnet Mask | Network | Host Pertama | Host Terakhir | Broadcast | Usable |
| :--- | ---: | :---: | :--- | :--- | :--- | :--- | :--- | ---: |
| **Lab A** | 90 | /25 | 255.255.255.128 | `10.252.108.0` | `10.252.108.1` | `10.252.108.126` | `10.252.108.127` | 126 |
| **Lab B** | 60 | /26 | 255.255.255.192 | `10.252.108.128` | `10.252.108.129` | `10.252.108.190` | `10.252.108.191` | 62 |
| **Administrasi** | 14 | /28 | 255.255.255.240 | `10.252.108.192` | `10.252.108.193` | `10.252.108.206` | `10.252.108.207` | 14 |
| **End-point** | 2 | /30 | 255.255.255.252 | `10.252.108.208` | `10.252.108.209` | `10.252.108.210` | `10.252.108.211` | 2 |
| *Belum dialokasikan* | — | — | — | `10.252.108.212` | — | — | `10.252.108.255` | 44 alamat |

---

## 1. Dasar Teori

**VLSM (Variable Length Subnet Mask)** adalah teknik subnetting yang memberi **ukuran subnet berbeda-beda** sesuai kebutuhan host setiap segmen. Berbeda dengan subnetting biasa (FLSM) yang membagi network menjadi potongan berukuran sama, VLSM menghindari pemborosan alamat pada segmen kecil.

### Mengapa soal ini harus memakai VLSM?

Dengan FLSM, 4 segmen membutuhkan $2^2 = 4$ subnet, sehingga /24 dipecah menjadi empat **/26** yang masing-masing hanya punya **62 host**. Lab A butuh 90 host, jadi FLSM **tidak bisa** memenuhi kebutuhan. Sebaliknya, bila semua subnet dibuat /25 (126 host) agar Lab A muat, hanya tersedia 2 subnet. Satu-satunya cara memenuhi keempat segmen dalam satu /24 adalah VLSM.

### Rumus

| Besaran | Rumus |
| :--- | :--- |
| Bit host ($h$) | $h$ terkecil yang memenuhi $2^h - 2 \ge$ kebutuhan host |
| Prefix | $32 - h$ |
| Jumlah alamat dalam subnet (block size) | $2^h$ |
| Host usable | $2^h - 2$ |
| Network berikutnya | Broadcast subnet sebelumnya $+ 1$ |

### Langkah VLSM

1. Urutkan segmen dari kebutuhan host **terbesar ke terkecil**.
2. Untuk setiap segmen, cari prefix terkecil yang cukup.
3. Alokasikan mulai dari alamat paling awal yang masih kosong.
4. Network segmen berikutnya dimulai tepat setelah broadcast segmen sebelumnya.

Urutan besar ke kecil penting agar setiap subnet selalu dimulai di **batas (boundary) yang sah**. Contohnya, subnet /25 harus berawal di kelipatan 128 (.0 atau .128); bila subnet kecil dialokasikan lebih dulu, batas itu bisa terlewati dan alamat terbuang.

---

## 2. Perhitungan per Segmen

### 2.1 Lab A — 90 host

- $2^6 - 2 = 62 < 90$ (tidak cukup), $2^7 - 2 = 126 \ge 90$ → $h = 7$.
- Prefix: $32 - 7 = $ **/25**, mask **255.255.255.128** (oktet ke-4: `1000 0000`).
- Block size: $2^7 = 128$ alamat.
- Dimulai dari alamat pertama: **10.252.108.0**.

| Network | Host Pertama | Host Terakhir | Broadcast |
| :--- | :--- | :--- | :--- |
| `10.252.108.0/25` | `10.252.108.1` | `10.252.108.126` | `10.252.108.127` |

Sisa host cadangan: $126 - 90 = 36$.

### 2.2 Lab B — 60 host

- $2^5 - 2 = 30 < 60$, $2^6 - 2 = 62 \ge 60$ → $h = 6$.
- Prefix: $32 - 6 = $ **/26**, mask **255.255.255.192** (`1100 0000`).
- Block size: $2^6 = 64$ alamat.
- Network: broadcast Lab A + 1 = $127 + 1$ = **10.252.108.128**.

| Network | Host Pertama | Host Terakhir | Broadcast |
| :--- | :--- | :--- | :--- |
| `10.252.108.128/26` | `10.252.108.129` | `10.252.108.190` | `10.252.108.191` |

Sisa host cadangan: $62 - 60 = 2$.

### 2.3 Administrasi — 14 host

- $2^3 - 2 = 6 < 14$, $2^4 - 2 = 14 \ge 14$ → $h = 4$.
- Prefix: $32 - 4 = $ **/28**, mask **255.255.255.240** (`1111 0000`).
- Block size: $2^4 = 16$ alamat.
- Network: $191 + 1$ = **10.252.108.192**.

| Network | Host Pertama | Host Terakhir | Broadcast |
| :--- | :--- | :--- | :--- |
| `10.252.108.192/28` | `10.252.108.193` | `10.252.108.206` | `10.252.108.207` |

Sisa host cadangan: $14 - 14 = 0$ (pas, tanpa ruang tambahan).

### 2.4 End-point — 2 host

- $2^1 - 2 = 0 < 2$, $2^2 - 2 = 2 \ge 2$ → $h = 2$.
- Prefix: $32 - 2 = $ **/30**, mask **255.255.255.252** (`1111 1100`).
- Block size: $2^2 = 4$ alamat.
- Network: $207 + 1$ = **10.252.108.208**.

| Network | Host Pertama | Host Terakhir | Broadcast |
| :--- | :--- | :--- | :--- |
| `10.252.108.208/30` | `10.252.108.209` | `10.252.108.210` | `10.252.108.211` |

Subnet /30 dengan 2 host adalah ukuran standar untuk **link point-to-point**, misalnya sambungan antar-router.

### 2.5 Sisa alamat

Alamat **10.252.108.212 – 10.252.108.255** (44 alamat) belum dialokasikan. Agar tetap bisa dipakai sebagai subnet yang sah, sisa ini dapat dipecah menjadi blok:

| Blok sisa | Jumlah alamat | Host usable | Contoh pemakaian nanti |
| :--- | ---: | ---: | :--- |
| `10.252.108.212/30` | 4 | 2 | Link antar-router tambahan |
| `10.252.108.216/29` | 8 | 6 | Segmen kecil (mis. server/printer) |
| `10.252.108.224/27` | 32 | 30 | Segmen baru (mis. Wi-Fi tamu) |

---

## 3. Analisis Efisiensi

| Ukuran | Nilai |
| :--- | ---: |
| Total kebutuhan host | 166 |
| Alamat yang dialokasikan (termasuk network & broadcast) | 212 dari 256 |
| Host usable yang dialokasikan | 204 |
| Utilisasi host usable | $\frac{166}{204} \times 100\% \approx 81{,}4\%$ |
| Sisa alamat untuk pengembangan | 44 |

Perbandingan dengan FLSM:

| Metode | Ukuran subnet | Bisa memenuhi semua segmen? | Keterangan |
| :--- | :--- | :---: | :--- |
| FLSM 4 × /26 | 62 host per subnet | Tidak | Lab A (90 host) tidak muat |
| FLSM 2 × /25 | 126 host per subnet | Tidak | Hanya 2 subnet, padahal butuh 4 |
| **VLSM** | /25, /26, /28, /30 | **Ya** | Masih tersisa 44 alamat |

Catatan perancangan:

- **Administrasi tidak punya ruang tumbuh** (14 dari 14 host). Bila nanti bertambah 1 perangkat saja, segmen ini harus dipindah ke blok /27 dari sisa alamat (`10.252.108.224/27`).
- **Lab B hanya menyisakan 2 host.** Bila kebutuhan bertambah, ia juga perlu diperbesar atau dibantu blok sisa.
- Jumlah host di atas sebaiknya sudah termasuk alamat untuk gateway router di setiap segmen.

---

## 4. Implementasi pada Cisco Packet Tracer

### 4.1 Topologi

End-point (/30) dipakai sebagai link antara dua router; Lab A dan Lab B berada di belakang R1, Administrasi di belakang R2.

```
 [Lab A]                                                    [Administrasi]
 PC/Switch                                                    PC/Switch
     |                                                            |
 G0/0 .1                                                      G0/0 .193
   [ R1 ]---------- G0/2 .209 ====/30==== .210 G0/1 ----------[ R2 ]
 G0/1 .129                     End-point link
     |
 [Lab B]
 PC/Switch
```

### 4.2 Tabel pengalamatan

| Perangkat | Interface | IP Address | Subnet Mask | Default Gateway |
| :--- | :--- | :--- | :--- | :--- |
| R1 | G0/0 | 10.252.108.1 | 255.255.255.128 | — |
| R1 | G0/1 | 10.252.108.129 | 255.255.255.192 | — |
| R1 | G0/2 | 10.252.108.209 | 255.255.255.252 | — |
| R2 | G0/1 | 10.252.108.210 | 255.255.255.252 | — |
| R2 | G0/0 | 10.252.108.193 | 255.255.255.240 | — |
| PC Lab A | NIC | 10.252.108.126 | 255.255.255.128 | 10.252.108.1 |
| PC Lab B | NIC | 10.252.108.190 | 255.255.255.192 | 10.252.108.129 |
| PC Administrasi | NIC | 10.252.108.206 | 255.255.255.240 | 10.252.108.193 |

### 4.3 Konfigurasi router

R1 (Router 2911):

```
enable
configure terminal
hostname R1
interface g0/0
 description LAB-A
 ip address 10.252.108.1 255.255.255.128
 no shutdown
interface g0/1
 description LAB-B
 ip address 10.252.108.129 255.255.255.192
 no shutdown
interface g0/2
 description END-POINT-KE-R2
 ip address 10.252.108.209 255.255.255.252
 no shutdown
 exit
ip route 10.252.108.192 255.255.255.240 10.252.108.210
end
write memory
```

R2 (Router 2911):

```
enable
configure terminal
hostname R2
interface g0/0
 description ADMINISTRASI
 ip address 10.252.108.193 255.255.255.240
 no shutdown
interface g0/1
 description END-POINT-KE-R1
 ip address 10.252.108.210 255.255.255.252
 no shutdown
 exit
ip route 10.252.108.0 255.255.255.128 10.252.108.209
ip route 10.252.108.128 255.255.255.192 10.252.108.209
end
write memory
```

### 4.4 Pengujian

1. `ping 10.252.108.210` dari R1 → membuktikan link End-point /30 aktif.
2. Dari PC Lab A: `ping 10.252.108.190` (Lab B) dan `ping 10.252.108.206` (Administrasi) → harus berhasil.
3. Dari PC Administrasi: `tracert 10.252.108.126` → melewati `10.252.108.193` lalu `10.252.108.209`.
4. Di router: `show ip route` → subnet /25, /26, /28, dan /30 tampil dengan prefix berbeda, membuktikan VLSM bekerja.

---

## 5. Kesimpulan

- Network 10.252.108.0/24 berhasil dibagi menjadi Lab A **/25**, Lab B **/26**, Administrasi **/28**, dan End-point **/30** dengan metode VLSM.
- FLSM tidak dapat memenuhi soal ini karena Lab A membutuhkan subnet yang lebih besar daripada pembagian rata empat subnet.
- Pengalokasian dari kebutuhan terbesar ke terkecil membuat setiap subnet berada di batas yang sah dan menyisakan blok alamat berurutan (44 alamat) untuk pengembangan.
- Hasil perhitungan diverifikasi dengan script Python `vlsm.py`.

---

## Lampiran — Script Verifikasi (`vlsm.py`)

```python
"""
Tugas 6 Konsep Jaringan - Kalkulator VLSM
Penyusun: Prayogo Adhi Satrio (3125600043)
Network 10.252.108.0/24 dibagi sesuai kebutuhan host tiap segmen.
"""
import ipaddress
import math

NETWORK = ipaddress.ip_network("10.252.108.0/24")
KEBUTUHAN = {
    "Lab A": 90,
    "Lab B": 60,
    "Administrasi": 14,
    "End-point": 2,
}


def prefix_untuk(host):
    """Prefix terkecil yang menampung `host` alamat usable: 2^h - 2 >= host."""
    h = math.ceil(math.log2(host + 2))
    return 32 - h


def vlsm(network, kebutuhan):
    # 1. Urutkan dari kebutuhan host terbesar ke terkecil
    urut = sorted(kebutuhan.items(), key=lambda x: x[1], reverse=True)
    alamat = network.network_address
    hasil = []
    for nama, host in urut:
        prefix = prefix_untuk(host)
        subnet = ipaddress.ip_network(f"{alamat}/{prefix}")
        hasil.append((nama, host, subnet))
        alamat = subnet.broadcast_address + 1   # subnet berikutnya mulai setelah broadcast
    return hasil, alamat


if __name__ == "__main__":
    hasil, sisa_mulai = vlsm(NETWORK, KEBUTUHAN)
    print(f"Network induk: {NETWORK} ({NETWORK.num_addresses} alamat)\n")
    print(f"{'Segmen':<14}{'Butuh':>6}{'Prefix':>8}  {'Mask':<17}{'Network':<16}"
          f"{'Host Pertama':<16}{'Host Terakhir':<16}{'Broadcast':<16}{'Usable':>7}{'Sisa':>6}")
    terpakai = 0
    for nama, host, s in hasil:
        usable = s.num_addresses - 2
        terpakai += s.num_addresses
        print(f"{nama:<14}{host:>6}{'/' + str(s.prefixlen):>8}  {str(s.netmask):<17}"
              f"{str(s.network_address):<16}{str(s.network_address + 1):<16}"
              f"{str(s.broadcast_address - 1):<16}{str(s.broadcast_address):<16}"
              f"{usable:>7}{usable - host:>6}")
    print(f"\nAlamat terpakai : {terpakai} dari {NETWORK.num_addresses}")
    print(f"Sisa (belum dialokasikan): {sisa_mulai} - {NETWORK.broadcast_address} "
          f"({NETWORK.num_addresses - terpakai} alamat)")
    print("Blok sisa yang rapi:",
          ", ".join(str(n) for n in ipaddress.summarize_address_range(sisa_mulai, NETWORK.broadcast_address)))
```

Output:

```
Network induk: 10.252.108.0/24 (256 alamat)

Segmen         Butuh  Prefix  Mask             Network         Host Pertama    Host Terakhir   Broadcast        Usable  Sisa
Lab A             90     /25  255.255.255.128  10.252.108.0    10.252.108.1    10.252.108.126  10.252.108.127      126    36
Lab B             60     /26  255.255.255.192  10.252.108.128  10.252.108.129  10.252.108.190  10.252.108.191       62     2
Administrasi      14     /28  255.255.255.240  10.252.108.192  10.252.108.193  10.252.108.206  10.252.108.207       14     0
End-point          2     /30  255.255.255.252  10.252.108.208  10.252.108.209  10.252.108.210  10.252.108.211        2     0

Alamat terpakai : 212 dari 256
Sisa (belum dialokasikan): 10.252.108.212 - 10.252.108.255 (44 alamat)
Blok sisa yang rapi: 10.252.108.212/30, 10.252.108.216/29, 10.252.108.224/27
```

## Referensi

1. Fuller, V., & Li, T. RFC 4632: *Classless Inter-domain Routing (CIDR): The Internet Address Assignment and Aggregation Plan*. IETF, 2006.
2. Cisco Networking Academy. *CCNA: Introduction to Networks* — Modul 11.9: VLSM.
3. Forouzan, B. A. *Data Communications and Networking* (edisi ke-5). McGraw-Hill. Bab 19: IPv4 Addressing.
