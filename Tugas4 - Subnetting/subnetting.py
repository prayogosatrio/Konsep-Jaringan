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
