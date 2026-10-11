# KONSEP JARINGAN
## Tugas 4 — Perhitungan Subnetting dan Simulasi pada Cisco Packet Tracer

**DOSEN:**  
Dr. Ferry Astika Saputra, ST, M.Sc. (197708232001121002)

**PENYUSUN:**  
Prayogo Adhi Satrio (3125600043)

**PROGRAM STUDI SARJANA TERAPAN TEKNIK INFORMATIKA**  
**POLITEKNIK ELEKTRONIKA NEGERI SURABAYA**

---

## Dasar Teori

**Subnetting** adalah teknik membagi satu network besar menjadi beberapa network kecil (subnet) dengan cara **meminjam bit dari bagian host** untuk dijadikan bagian network. Pada tugas ini semua subnet berukuran sama (Fixed Length Subnet Mask/FLSM).

Tujuan subnetting:

- Memecah broadcast domain sehingga lalu lintas broadcast lebih sedikit.
- Memisahkan kelompok pengguna (mis. per lantai, per divisi) agar lebih mudah dikelola dan diamankan.
- Memakai ruang alamat IP secara lebih efisien.

### Rumus dasar

| Besaran | Rumus | Keterangan |
| :--- | :--- | :--- |
| Bit yang dipinjam ($n$) | $2^n \ge$ jumlah subnet yang dibutuhkan | Ambil $n$ terkecil yang memenuhi |
| Prefix baru | prefix lama $+ n$ | Mis. /24 + 2 = /26 |
| Jumlah subnet tersedia | $2^n$ | |
| Bit host tersisa ($h$) | $32 -$ prefix baru | |
| Host valid per subnet | $2^h - 2$ | Dikurangi network address dan broadcast |
| Blok lompatan (block size) | $256 -$ nilai mask pada oktet yang berubah | Jarak antar-network address |
| Network address | Kelipatan blok lompatan | Semua bit host = 0 |
| Host pertama | Network address $+ 1$ | |
| Broadcast | Network berikutnya $- 1$ | Semua bit host = 1 |
| Host terakhir | Broadcast $- 1$ | |

Kolom **Bit pinjaman** pada setiap tabel hasil menunjukkan kombinasi bit yang dipinjam. Setiap kombinasi menghasilkan satu subnet; urutannya 00, 01, 10, 11, dan seterusnya.

### Ringkasan semua kasus

| Kasus | Network awal | Kebutuhan | $n$ | Prefix baru | Subnet mask baru | Blok | Subnet tersedia | Host per subnet |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | ---: |
| A | 192.168.1.0/24 | 4 subnet | 2 | /26 | 255.255.255.192 | 64 (oktet 4) | 4 | 62 |
| A (alternatif) | 192.168.1.0/24 | 6 subnet | 3 | /27 | 255.255.255.224 | 32 (oktet 4) | 8 | 30 |
| B | 132.10.0.0/16 | 10 subnet | 4 | /20 | 255.255.240.0 | 16 (oktet 3) | 16 | 4.094 |
| C | 17.8.0.0/16 | 4 subnet | 2 | /18 | 255.255.192.0 | 64 (oktet 3) | 4 | 16.382 |
| D | 8.32.0.0/12 | 6 subnet | 3 | /15 | 255.254.0.0 | 2 (oktet 2) | 8 | 131.070 |

### Topologi simulasi Packet Tracer

Setiap kasus disimulasikan dengan topologi **router-on-a-stick** agar jumlah subnet berapa pun cukup memakai satu router dan satu switch:

```
                 [Router 2911]
                   G0/0 (trunk, subinterface G0/0.10, G0/0.20, ...)
                     |
                 G0/1|
               [Switch 2960]
      Fa0/1    Fa0/2    Fa0/3   ...   Fa0/n
        |        |        |             |
      [PC1]    [PC2]    [PC3]   ...   [PCn]
     VLAN 10  VLAN 20  VLAN 30       VLAN n×10
```

- Setiap subnet = satu VLAN = satu subinterface router.
- IP **gateway** (subinterface router) memakai **host pertama** subnet.
- IP **PC** memakai **host terakhir** subnet, dengan default gateway = host pertama.
- Kabel: Router G0/0 ↔ Switch G0/1 (Copper Straight-Through), Switch Fa0/x ↔ PC FastEthernet0.

---

## Kasus A — 192.168.1.0/24 dijadikan 4 subnet

### Langkah perhitungan

1. **Bit yang dipinjam:** $2^n \ge 4 \Rightarrow 2^2 = 4 \ge 4$, jadi $n = 2$.
2. **Prefix baru:** $/24 + 2 = /26$.
3. **Subnet mask baru:** `255.255.255.0` menjadi **`255.255.255.192`**. Perubahan terjadi di oktet ke-4:

   | | Biner oktet ke-4 | Desimal |
   | :--- | :--- | :--- |
   | Mask lama (/24) | `0000 0000` | 0 |
   | Mask baru (/26) | `1100 0000` | 192 |

4. **Blok lompatan (block size):** $256 - 192 = 64$ pada oktet ke-4. Network berikutnya selalu bertambah 64.
5. **Jumlah subnet tersedia:** $2^2 = 4$ subnet.
6. **Host valid per subnet:** $2^{6} - 2 = 62$ host.

### Tabel hasil subnetting

| Subnet | Bit pinjaman (2 bit) | Network Address | Host Pertama | Host Terakhir | Broadcast |
| :--- | :---: | :--- | :--- | :--- | :--- |
| Subnet 1 | `00` | `192.168.1.0/26` | `192.168.1.1` | `192.168.1.62` | `192.168.1.63` |
| Subnet 2 | `01` | `192.168.1.64/26` | `192.168.1.65` | `192.168.1.126` | `192.168.1.127` |
| Subnet 3 | `10` | `192.168.1.128/26` | `192.168.1.129` | `192.168.1.190` | `192.168.1.191` |
| Subnet 4 | `11` | `192.168.1.192/26` | `192.168.1.193` | `192.168.1.254` | `192.168.1.255` |

### Pengalamatan untuk simulasi Packet Tracer

Gateway memakai host pertama, PC memakai host terakhir setiap subnet.

| VLAN | Port switch | Subinterface router | IP gateway | IP PC | Subnet mask |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | Fa0/1 | G0/0.10 | `192.168.1.1` | `192.168.1.62` | `255.255.255.192` |
| 20 | Fa0/2 | G0/0.20 | `192.168.1.65` | `192.168.1.126` | `255.255.255.192` |
| 30 | Fa0/3 | G0/0.30 | `192.168.1.129` | `192.168.1.190` | `255.255.255.192` |
| 40 | Fa0/4 | G0/0.40 | `192.168.1.193` | `192.168.1.254` | `255.255.255.192` |

Konfigurasi router (Router 2911):

```
enable
configure terminal
interface g0/0
 no shutdown
 exit
interface g0/0.10
 encapsulation dot1Q 10
 ip address 192.168.1.1 255.255.255.192
 exit
interface g0/0.20
 encapsulation dot1Q 20
 ip address 192.168.1.65 255.255.255.192
 exit
interface g0/0.30
 encapsulation dot1Q 30
 ip address 192.168.1.129 255.255.255.192
 exit
interface g0/0.40
 encapsulation dot1Q 40
 ip address 192.168.1.193 255.255.255.192
 exit
end
write memory
```

Konfigurasi switch (Switch 2960):

```
enable
configure terminal
vlan 10
interface fa0/1
 switchport mode access
 switchport access vlan 10
 exit
vlan 20
interface fa0/2
 switchport mode access
 switchport access vlan 20
 exit
vlan 30
interface fa0/3
 switchport mode access
 switchport access vlan 30
 exit
vlan 40
interface fa0/4
 switchport mode access
 switchport access vlan 40
 exit
interface g0/1
 switchport mode trunk
 exit
end
write memory
```

---

## Kasus A (Alternatif) — 192.168.1.0/24 dijadikan 6 subnet

### Langkah perhitungan

1. **Bit yang dipinjam:** $2^n \ge 6 \Rightarrow 2^3 = 8 \ge 6$, jadi $n = 3$.
2. **Prefix baru:** $/24 + 3 = /27$.
3. **Subnet mask baru:** `255.255.255.0` menjadi **`255.255.255.224`**. Perubahan terjadi di oktet ke-4:

   | | Biner oktet ke-4 | Desimal |
   | :--- | :--- | :--- |
   | Mask lama (/24) | `0000 0000` | 0 |
   | Mask baru (/27) | `1110 0000` | 224 |

4. **Blok lompatan (block size):** $256 - 224 = 32$ pada oktet ke-4. Network berikutnya selalu bertambah 32.
5. **Jumlah subnet tersedia:** $2^3 = 8$ subnet (dipakai 6, sisa 2 sebagai cadangan).
6. **Host valid per subnet:** $2^{5} - 2 = 30$ host.

### Tabel hasil subnetting

| Subnet | Bit pinjaman (3 bit) | Network Address | Host Pertama | Host Terakhir | Broadcast |
| :--- | :---: | :--- | :--- | :--- | :--- |
| Subnet 1 | `000` | `192.168.1.0/27` | `192.168.1.1` | `192.168.1.30` | `192.168.1.31` |
| Subnet 2 | `001` | `192.168.1.32/27` | `192.168.1.33` | `192.168.1.62` | `192.168.1.63` |
| Subnet 3 | `010` | `192.168.1.64/27` | `192.168.1.65` | `192.168.1.94` | `192.168.1.95` |
| Subnet 4 | `011` | `192.168.1.96/27` | `192.168.1.97` | `192.168.1.126` | `192.168.1.127` |
| Subnet 5 | `100` | `192.168.1.128/27` | `192.168.1.129` | `192.168.1.158` | `192.168.1.159` |
| Subnet 6 | `101` | `192.168.1.160/27` | `192.168.1.161` | `192.168.1.190` | `192.168.1.191` |
| Subnet 7 *(cadangan)* | `110` | `192.168.1.192/27` | `192.168.1.193` | `192.168.1.222` | `192.168.1.223` |
| Subnet 8 *(cadangan)* | `111` | `192.168.1.224/27` | `192.168.1.225` | `192.168.1.254` | `192.168.1.255` |

### Pengalamatan untuk simulasi Packet Tracer

Gateway memakai host pertama, PC memakai host terakhir setiap subnet.

| VLAN | Port switch | Subinterface router | IP gateway | IP PC | Subnet mask |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | Fa0/1 | G0/0.10 | `192.168.1.1` | `192.168.1.30` | `255.255.255.224` |
| 20 | Fa0/2 | G0/0.20 | `192.168.1.33` | `192.168.1.62` | `255.255.255.224` |
| 30 | Fa0/3 | G0/0.30 | `192.168.1.65` | `192.168.1.94` | `255.255.255.224` |
| 40 | Fa0/4 | G0/0.40 | `192.168.1.97` | `192.168.1.126` | `255.255.255.224` |
| 50 | Fa0/5 | G0/0.50 | `192.168.1.129` | `192.168.1.158` | `255.255.255.224` |
| 60 | Fa0/6 | G0/0.60 | `192.168.1.161` | `192.168.1.190` | `255.255.255.224` |

Konfigurasi router (Router 2911):

```
enable
configure terminal
interface g0/0
 no shutdown
 exit
interface g0/0.10
 encapsulation dot1Q 10
 ip address 192.168.1.1 255.255.255.224
 exit
interface g0/0.20
 encapsulation dot1Q 20
 ip address 192.168.1.33 255.255.255.224
 exit
interface g0/0.30
 encapsulation dot1Q 30
 ip address 192.168.1.65 255.255.255.224
 exit
interface g0/0.40
 encapsulation dot1Q 40
 ip address 192.168.1.97 255.255.255.224
 exit
interface g0/0.50
 encapsulation dot1Q 50
 ip address 192.168.1.129 255.255.255.224
 exit
interface g0/0.60
 encapsulation dot1Q 60
 ip address 192.168.1.161 255.255.255.224
 exit
end
write memory
```

Konfigurasi switch (Switch 2960):

```
enable
configure terminal
vlan 10
interface fa0/1
 switchport mode access
 switchport access vlan 10
 exit
vlan 20
interface fa0/2
 switchport mode access
 switchport access vlan 20
 exit
vlan 30
interface fa0/3
 switchport mode access
 switchport access vlan 30
 exit
vlan 40
interface fa0/4
 switchport mode access
 switchport access vlan 40
 exit
vlan 50
interface fa0/5
 switchport mode access
 switchport access vlan 50
 exit
vlan 60
interface fa0/6
 switchport mode access
 switchport access vlan 60
 exit
interface g0/1
 switchport mode trunk
 exit
end
write memory
```

---

## Kasus B — 132.10.0.0/16 dijadikan 10 subnet

### Langkah perhitungan

1. **Bit yang dipinjam:** $2^n \ge 10 \Rightarrow 2^4 = 16 \ge 10$, jadi $n = 4$.
2. **Prefix baru:** $/16 + 4 = /20$.
3. **Subnet mask baru:** `255.255.0.0` menjadi **`255.255.240.0`**. Perubahan terjadi di oktet ke-3:

   | | Biner oktet ke-3 | Desimal |
   | :--- | :--- | :--- |
   | Mask lama (/16) | `0000 0000` | 0 |
   | Mask baru (/20) | `1111 0000` | 240 |

4. **Blok lompatan (block size):** $256 - 240 = 16$ pada oktet ke-3. Network berikutnya selalu bertambah 16.
5. **Jumlah subnet tersedia:** $2^4 = 16$ subnet (dipakai 10, sisa 6 sebagai cadangan).
6. **Host valid per subnet:** $2^{12} - 2 = 4.094$ host.

### Tabel hasil subnetting

| Subnet | Bit pinjaman (4 bit) | Network Address | Host Pertama | Host Terakhir | Broadcast |
| :--- | :---: | :--- | :--- | :--- | :--- |
| Subnet 1 | `0000` | `132.10.0.0/20` | `132.10.0.1` | `132.10.15.254` | `132.10.15.255` |
| Subnet 2 | `0001` | `132.10.16.0/20` | `132.10.16.1` | `132.10.31.254` | `132.10.31.255` |
| Subnet 3 | `0010` | `132.10.32.0/20` | `132.10.32.1` | `132.10.47.254` | `132.10.47.255` |
| Subnet 4 | `0011` | `132.10.48.0/20` | `132.10.48.1` | `132.10.63.254` | `132.10.63.255` |
| Subnet 5 | `0100` | `132.10.64.0/20` | `132.10.64.1` | `132.10.79.254` | `132.10.79.255` |
| Subnet 6 | `0101` | `132.10.80.0/20` | `132.10.80.1` | `132.10.95.254` | `132.10.95.255` |
| Subnet 7 | `0110` | `132.10.96.0/20` | `132.10.96.1` | `132.10.111.254` | `132.10.111.255` |
| Subnet 8 | `0111` | `132.10.112.0/20` | `132.10.112.1` | `132.10.127.254` | `132.10.127.255` |
| Subnet 9 | `1000` | `132.10.128.0/20` | `132.10.128.1` | `132.10.143.254` | `132.10.143.255` |
| Subnet 10 | `1001` | `132.10.144.0/20` | `132.10.144.1` | `132.10.159.254` | `132.10.159.255` |
| Subnet 11 *(cadangan)* | `1010` | `132.10.160.0/20` | `132.10.160.1` | `132.10.175.254` | `132.10.175.255` |
| Subnet 12 *(cadangan)* | `1011` | `132.10.176.0/20` | `132.10.176.1` | `132.10.191.254` | `132.10.191.255` |
| Subnet 13 *(cadangan)* | `1100` | `132.10.192.0/20` | `132.10.192.1` | `132.10.207.254` | `132.10.207.255` |
| Subnet 14 *(cadangan)* | `1101` | `132.10.208.0/20` | `132.10.208.1` | `132.10.223.254` | `132.10.223.255` |
| Subnet 15 *(cadangan)* | `1110` | `132.10.224.0/20` | `132.10.224.1` | `132.10.239.254` | `132.10.239.255` |
| Subnet 16 *(cadangan)* | `1111` | `132.10.240.0/20` | `132.10.240.1` | `132.10.255.254` | `132.10.255.255` |

### Pengalamatan untuk simulasi Packet Tracer

Gateway memakai host pertama, PC memakai host terakhir setiap subnet.

| VLAN | Port switch | Subinterface router | IP gateway | IP PC | Subnet mask |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | Fa0/1 | G0/0.10 | `132.10.0.1` | `132.10.15.254` | `255.255.240.0` |
| 20 | Fa0/2 | G0/0.20 | `132.10.16.1` | `132.10.31.254` | `255.255.240.0` |
| 30 | Fa0/3 | G0/0.30 | `132.10.32.1` | `132.10.47.254` | `255.255.240.0` |
| 40 | Fa0/4 | G0/0.40 | `132.10.48.1` | `132.10.63.254` | `255.255.240.0` |
| 50 | Fa0/5 | G0/0.50 | `132.10.64.1` | `132.10.79.254` | `255.255.240.0` |
| 60 | Fa0/6 | G0/0.60 | `132.10.80.1` | `132.10.95.254` | `255.255.240.0` |
| 70 | Fa0/7 | G0/0.70 | `132.10.96.1` | `132.10.111.254` | `255.255.240.0` |
| 80 | Fa0/8 | G0/0.80 | `132.10.112.1` | `132.10.127.254` | `255.255.240.0` |
| 90 | Fa0/9 | G0/0.90 | `132.10.128.1` | `132.10.143.254` | `255.255.240.0` |
| 100 | Fa0/10 | G0/0.100 | `132.10.144.1` | `132.10.159.254` | `255.255.240.0` |

Konfigurasi router (Router 2911):

```
enable
configure terminal
interface g0/0
 no shutdown
 exit
interface g0/0.10
 encapsulation dot1Q 10
 ip address 132.10.0.1 255.255.240.0
 exit
interface g0/0.20
 encapsulation dot1Q 20
 ip address 132.10.16.1 255.255.240.0
 exit
interface g0/0.30
 encapsulation dot1Q 30
 ip address 132.10.32.1 255.255.240.0
 exit
interface g0/0.40
 encapsulation dot1Q 40
 ip address 132.10.48.1 255.255.240.0
 exit
interface g0/0.50
 encapsulation dot1Q 50
 ip address 132.10.64.1 255.255.240.0
 exit
interface g0/0.60
 encapsulation dot1Q 60
 ip address 132.10.80.1 255.255.240.0
 exit
interface g0/0.70
 encapsulation dot1Q 70
 ip address 132.10.96.1 255.255.240.0
 exit
interface g0/0.80
 encapsulation dot1Q 80
 ip address 132.10.112.1 255.255.240.0
 exit
interface g0/0.90
 encapsulation dot1Q 90
 ip address 132.10.128.1 255.255.240.0
 exit
interface g0/0.100
 encapsulation dot1Q 100
 ip address 132.10.144.1 255.255.240.0
 exit
end
write memory
```

Konfigurasi switch (Switch 2960):

```
enable
configure terminal
vlan 10
interface fa0/1
 switchport mode access
 switchport access vlan 10
 exit
vlan 20
interface fa0/2
 switchport mode access
 switchport access vlan 20
 exit
vlan 30
interface fa0/3
 switchport mode access
 switchport access vlan 30
 exit
vlan 40
interface fa0/4
 switchport mode access
 switchport access vlan 40
 exit
vlan 50
interface fa0/5
 switchport mode access
 switchport access vlan 50
 exit
vlan 60
interface fa0/6
 switchport mode access
 switchport access vlan 60
 exit
vlan 70
interface fa0/7
 switchport mode access
 switchport access vlan 70
 exit
vlan 80
interface fa0/8
 switchport mode access
 switchport access vlan 80
 exit
vlan 90
interface fa0/9
 switchport mode access
 switchport access vlan 90
 exit
vlan 100
interface fa0/10
 switchport mode access
 switchport access vlan 100
 exit
interface g0/1
 switchport mode trunk
 exit
end
write memory
```

---

## Kasus C — 17.8.0.0/16 dijadikan 4 subnet

### Langkah perhitungan

1. **Bit yang dipinjam:** $2^n \ge 4 \Rightarrow 2^2 = 4 \ge 4$, jadi $n = 2$.
2. **Prefix baru:** $/16 + 2 = /18$.
3. **Subnet mask baru:** `255.255.0.0` menjadi **`255.255.192.0`**. Perubahan terjadi di oktet ke-3:

   | | Biner oktet ke-3 | Desimal |
   | :--- | :--- | :--- |
   | Mask lama (/16) | `0000 0000` | 0 |
   | Mask baru (/18) | `1100 0000` | 192 |

4. **Blok lompatan (block size):** $256 - 192 = 64$ pada oktet ke-3. Network berikutnya selalu bertambah 64.
5. **Jumlah subnet tersedia:** $2^2 = 4$ subnet.
6. **Host valid per subnet:** $2^{14} - 2 = 16.382$ host.

### Tabel hasil subnetting

| Subnet | Bit pinjaman (2 bit) | Network Address | Host Pertama | Host Terakhir | Broadcast |
| :--- | :---: | :--- | :--- | :--- | :--- |
| Subnet 1 | `00` | `17.8.0.0/18` | `17.8.0.1` | `17.8.63.254` | `17.8.63.255` |
| Subnet 2 | `01` | `17.8.64.0/18` | `17.8.64.1` | `17.8.127.254` | `17.8.127.255` |
| Subnet 3 | `10` | `17.8.128.0/18` | `17.8.128.1` | `17.8.191.254` | `17.8.191.255` |
| Subnet 4 | `11` | `17.8.192.0/18` | `17.8.192.1` | `17.8.255.254` | `17.8.255.255` |

### Pengalamatan untuk simulasi Packet Tracer

Gateway memakai host pertama, PC memakai host terakhir setiap subnet.

| VLAN | Port switch | Subinterface router | IP gateway | IP PC | Subnet mask |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | Fa0/1 | G0/0.10 | `17.8.0.1` | `17.8.63.254` | `255.255.192.0` |
| 20 | Fa0/2 | G0/0.20 | `17.8.64.1` | `17.8.127.254` | `255.255.192.0` |
| 30 | Fa0/3 | G0/0.30 | `17.8.128.1` | `17.8.191.254` | `255.255.192.0` |
| 40 | Fa0/4 | G0/0.40 | `17.8.192.1` | `17.8.255.254` | `255.255.192.0` |

Konfigurasi router (Router 2911):

```
enable
configure terminal
interface g0/0
 no shutdown
 exit
interface g0/0.10
 encapsulation dot1Q 10
 ip address 17.8.0.1 255.255.192.0
 exit
interface g0/0.20
 encapsulation dot1Q 20
 ip address 17.8.64.1 255.255.192.0
 exit
interface g0/0.30
 encapsulation dot1Q 30
 ip address 17.8.128.1 255.255.192.0
 exit
interface g0/0.40
 encapsulation dot1Q 40
 ip address 17.8.192.1 255.255.192.0
 exit
end
write memory
```

Konfigurasi switch (Switch 2960):

```
enable
configure terminal
vlan 10
interface fa0/1
 switchport mode access
 switchport access vlan 10
 exit
vlan 20
interface fa0/2
 switchport mode access
 switchport access vlan 20
 exit
vlan 30
interface fa0/3
 switchport mode access
 switchport access vlan 30
 exit
vlan 40
interface fa0/4
 switchport mode access
 switchport access vlan 40
 exit
interface g0/1
 switchport mode trunk
 exit
end
write memory
```

---

## Kasus D — 8.32.0.0/12 dijadikan 6 subnet

### Langkah perhitungan

1. **Bit yang dipinjam:** $2^n \ge 6 \Rightarrow 2^3 = 8 \ge 6$, jadi $n = 3$.
2. **Prefix baru:** $/12 + 3 = /15$.
3. **Subnet mask baru:** `255.240.0.0` menjadi **`255.254.0.0`**. Perubahan terjadi di oktet ke-2:

   | | Biner oktet ke-2 | Desimal |
   | :--- | :--- | :--- |
   | Mask lama (/12) | `1111 0000` | 240 |
   | Mask baru (/15) | `1111 1110` | 254 |

4. **Blok lompatan (block size):** $256 - 254 = 2$ pada oktet ke-2. Network berikutnya selalu bertambah 2.
5. **Jumlah subnet tersedia:** $2^3 = 8$ subnet (dipakai 6, sisa 2 sebagai cadangan).
6. **Host valid per subnet:** $2^{17} - 2 = 131.070$ host.

### Tabel hasil subnetting

| Subnet | Bit pinjaman (3 bit) | Network Address | Host Pertama | Host Terakhir | Broadcast |
| :--- | :---: | :--- | :--- | :--- | :--- |
| Subnet 1 | `000` | `8.32.0.0/15` | `8.32.0.1` | `8.33.255.254` | `8.33.255.255` |
| Subnet 2 | `001` | `8.34.0.0/15` | `8.34.0.1` | `8.35.255.254` | `8.35.255.255` |
| Subnet 3 | `010` | `8.36.0.0/15` | `8.36.0.1` | `8.37.255.254` | `8.37.255.255` |
| Subnet 4 | `011` | `8.38.0.0/15` | `8.38.0.1` | `8.39.255.254` | `8.39.255.255` |
| Subnet 5 | `100` | `8.40.0.0/15` | `8.40.0.1` | `8.41.255.254` | `8.41.255.255` |
| Subnet 6 | `101` | `8.42.0.0/15` | `8.42.0.1` | `8.43.255.254` | `8.43.255.255` |
| Subnet 7 *(cadangan)* | `110` | `8.44.0.0/15` | `8.44.0.1` | `8.45.255.254` | `8.45.255.255` |
| Subnet 8 *(cadangan)* | `111` | `8.46.0.0/15` | `8.46.0.1` | `8.47.255.254` | `8.47.255.255` |

### Pengalamatan untuk simulasi Packet Tracer

Gateway memakai host pertama, PC memakai host terakhir setiap subnet.

| VLAN | Port switch | Subinterface router | IP gateway | IP PC | Subnet mask |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | Fa0/1 | G0/0.10 | `8.32.0.1` | `8.33.255.254` | `255.254.0.0` |
| 20 | Fa0/2 | G0/0.20 | `8.34.0.1` | `8.35.255.254` | `255.254.0.0` |
| 30 | Fa0/3 | G0/0.30 | `8.36.0.1` | `8.37.255.254` | `255.254.0.0` |
| 40 | Fa0/4 | G0/0.40 | `8.38.0.1` | `8.39.255.254` | `255.254.0.0` |
| 50 | Fa0/5 | G0/0.50 | `8.40.0.1` | `8.41.255.254` | `255.254.0.0` |
| 60 | Fa0/6 | G0/0.60 | `8.42.0.1` | `8.43.255.254` | `255.254.0.0` |

Konfigurasi router (Router 2911):

```
enable
configure terminal
interface g0/0
 no shutdown
 exit
interface g0/0.10
 encapsulation dot1Q 10
 ip address 8.32.0.1 255.254.0.0
 exit
interface g0/0.20
 encapsulation dot1Q 20
 ip address 8.34.0.1 255.254.0.0
 exit
interface g0/0.30
 encapsulation dot1Q 30
 ip address 8.36.0.1 255.254.0.0
 exit
interface g0/0.40
 encapsulation dot1Q 40
 ip address 8.38.0.1 255.254.0.0
 exit
interface g0/0.50
 encapsulation dot1Q 50
 ip address 8.40.0.1 255.254.0.0
 exit
interface g0/0.60
 encapsulation dot1Q 60
 ip address 8.42.0.1 255.254.0.0
 exit
end
write memory
```

Konfigurasi switch (Switch 2960):

```
enable
configure terminal
vlan 10
interface fa0/1
 switchport mode access
 switchport access vlan 10
 exit
vlan 20
interface fa0/2
 switchport mode access
 switchport access vlan 20
 exit
vlan 30
interface fa0/3
 switchport mode access
 switchport access vlan 30
 exit
vlan 40
interface fa0/4
 switchport mode access
 switchport access vlan 40
 exit
vlan 50
interface fa0/5
 switchport mode access
 switchport access vlan 50
 exit
vlan 60
interface fa0/6
 switchport mode access
 switchport access vlan 60
 exit
interface g0/1
 switchport mode trunk
 exit
end
write memory
```

---
## Langkah Simulasi dan Pengujian di Packet Tracer

1. Tempatkan **Router 2911**, **Switch 2960-24TT**, dan PC sebanyak jumlah subnet yang dibutuhkan.
2. Hubungkan kabel sesuai topologi di atas.
3. Masukkan konfigurasi switch dan router dari tabel kasus yang dikerjakan melalui tab **CLI**.
4. Pada setiap PC, buka **Desktop → IP Configuration**, pilih **Static**, lalu isi IP PC, subnet mask, dan default gateway sesuai tabel.
5. Uji koneksi dari **Command Prompt** PC:
   - `ping <IP gateway sendiri>` → harus berhasil (PC ke router).
   - `ping <IP PC di subnet lain>` → harus berhasil karena router melakukan routing antar-subnet (inter-VLAN routing).
   - `tracert <IP PC di subnet lain>` → hop pertama adalah IP gateway, membuktikan paket lewat router.
6. Di router, jalankan `show ip interface brief` dan `show ip route` untuk memastikan semua subinterface *up* dan setiap subnet muncul sebagai *directly connected* (C).

Pada percobaan pertama, ping antar-subnet bisa gagal satu kali (timeout) karena PC dan router masih menjalankan ARP; ping berikutnya akan berhasil.

---

## Kesimpulan

- Jumlah bit yang dipinjam ditentukan oleh $2^n \ge$ kebutuhan subnet. Karena $2^n$ selalu pangkat dua, kebutuhan 6 dan 10 subnet menyisakan subnet cadangan (2 dan 6 subnet).
- Semakin banyak bit yang dipinjam, semakin banyak subnet tetapi semakin sedikit host per subnet.
- Letak oktet yang berubah bergantung pada prefix awal: /24 berubah di oktet ke-4, /16 di oktet ke-3, dan /12 di oktet ke-2. Karena itu blok lompatan dihitung pada oktet tersebut.
- Hasil perhitungan manual sudah diverifikasi dengan script Python (`subnetting.py`) yang memakai modul `ipaddress`.

---

## Lampiran — Script Verifikasi (`subnetting.py`)

```python
"""
Tugas 4 Konsep Jaringan - Kalkulator Subnetting
Penyusun: Prayogo Adhi Satrio (3125600043)
Membagi sebuah network menjadi sejumlah subnet dengan ukuran sama (FLSM).
"""
import ipaddress
import math

KASUS = [
    ("A1", "192.168.1.0/24", 4),
    ("A2", "192.168.1.0/24", 6),
    ("B",  "132.10.0.0/16", 10),
    ("C",  "17.8.0.0/16", 4),
    ("D",  "8.32.0.0/12", 6),
]


def hitung(nama, network, target):
    net = ipaddress.ip_network(network)
    n = math.ceil(math.log2(target))          # bit yang dipinjam: 2^n >= target
    prefix_baru = net.prefixlen + n
    subnets = list(net.subnets(new_prefix=prefix_baru))
    host_bits = 32 - prefix_baru
    print(f"\n=== Kasus {nama}: {network} -> {target} subnet ===")
    print(f"Bit dipinjam (n)      : {n}  (2^{n} = {2**n} >= {target})")
    print(f"Prefix baru           : /{net.prefixlen} + {n} = /{prefix_baru}")
    print(f"Subnet mask baru      : {subnets[0].netmask}")
    print(f"Bit host tersisa      : {host_bits}")
    print(f"Host valid per subnet : 2^{host_bits} - 2 = {2**host_bits - 2:,}")
    print(f"Total subnet tersedia : {len(subnets)}")
    print(f"{'No':<4}{'Network':<20}{'Host Pertama':<17}{'Host Terakhir':<17}{'Broadcast':<17}")
    for i, s in enumerate(subnets, 1):
        tanda = "" if i <= target else "  (cadangan)"
        print(f"{i:<4}{str(s):<20}{str(s.network_address + 1):<17}"
              f"{str(s.broadcast_address - 1):<17}{str(s.broadcast_address):<17}{tanda}")


if __name__ == "__main__":
    for kasus in KASUS:
        hitung(*kasus)
```

Jalankan dengan `python3 subnetting.py`.

## Referensi

1. Forouzan, B. A. *Data Communications and Networking* (edisi ke-5). McGraw-Hill. Bab 19: Network-Layer Protocols — IPv4 Addressing.
2. Cisco Networking Academy. *CCNA: Introduction to Networks* — Modul 11: IPv4 Addressing (Subnetting).
3. Python Software Foundation. *ipaddress — IPv4/IPv6 manipulation library*. https://docs.python.org/3/library/ipaddress.html
