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
