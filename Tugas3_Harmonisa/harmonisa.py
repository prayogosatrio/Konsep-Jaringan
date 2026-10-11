"""
Tugas 3 Konsep Jaringan
Visualisasi penjumlahan sinyal harmonisa ganjil (1, 3, 5, ...)
menuju gelombang kotak (square wave), beserta proses sampling-nya.

Penyusun : Prayogo Adhi Satrio (3125600043)
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# 1. Parameter
# ---------------------------------------------------------------
f0 = 1                           # frekuensi dasar (Hz)
durasi = 2                       # lama pengamatan (detik) = 2 periode
t = np.linspace(0, durasi, 2000) # waktu "kontinu" (resolusi tinggi)
harmonisa = [1, 3, 5, 7, 9]      # hanya harmonisa GANJIL
fs = 25                          # frekuensi sampling (Hz)
t_s = np.arange(0, durasi, 1 / fs)

# Warna yang tetap mudah dibedakan (ramah buta warna)
WARNA = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9"]


def komponen(n, waktu):
    """Satu komponen deret Fourier gelombang kotak: (4/pi) * sin(2*pi*n*f0*t) / n"""
    return (4 / np.pi) * np.sin(2 * np.pi * n * f0 * waktu) / n


def jumlah_harmonisa(daftar_n, waktu):
    """Menjumlahkan komponen-komponen harmonisa pada daftar_n."""
    total = np.zeros_like(waktu)
    for n in daftar_n:
        total += komponen(n, waktu)
    return total


# Gelombang kotak ideal sebagai pembanding
kotak_ideal = np.sign(np.sin(2 * np.pi * f0 * t))

# ---------------------------------------------------------------
# Gambar 1 - Komponen harmonisa satu per satu
# ---------------------------------------------------------------
plt.figure(figsize=(10, 4.5))
for i, n in enumerate(harmonisa):
    plt.plot(t, komponen(n, t), color=WARNA[i], linewidth=1.6,
             label=f"Harmonisa ke-{n}  ({n * f0} Hz, amplitudo {4 / (np.pi * n):.3f})")
plt.title("Gambar 1. Komponen harmonisa ganjil")
plt.xlabel("Waktu (s)")
plt.ylabel("Amplitudo")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=8, loc="upper right")
plt.tight_layout()
plt.savefig("gambar1_komponen_harmonisa.png", dpi=150)

# ---------------------------------------------------------------
# Gambar 2 - Penjumlahan bertahap 1, 1+3, 1+3+5, ...
# ---------------------------------------------------------------
fig, axes = plt.subplots(len(harmonisa), 1, figsize=(10, 11), sharex=True)
for i, ax in enumerate(axes):
    dipakai = harmonisa[: i + 1]
    ax.plot(t, kotak_ideal, color="gray", linestyle="--", linewidth=1,
            label="Gelombang kotak ideal")
    ax.plot(t, jumlah_harmonisa(dipakai, t), color=WARNA[0], linewidth=1.8,
            label="Hasil penjumlahan")
    judul = " + ".join(str(n) for n in dipakai)
    ax.set_title(f"Harmonisa {judul}", fontsize=10, loc="left")
    ax.set_ylim(-1.5, 1.5)
    ax.set_ylabel("Amplitudo")
    ax.grid(True, linestyle="--", alpha=0.5)
axes[0].legend(fontsize=8, loc="upper right")
axes[-1].set_xlabel("Waktu (s)")
fig.suptitle("Gambar 2. Penjumlahan bertahap harmonisa ganjil", fontsize=12)
fig.tight_layout()
fig.savefig("gambar2_penjumlahan_bertahap.png", dpi=150)

# ---------------------------------------------------------------
# Gambar 3 - Sinyal hasil penjumlahan dan hasil sampling
# ---------------------------------------------------------------
s_kontinu = jumlah_harmonisa(harmonisa, t)
s_diskrit = jumlah_harmonisa(harmonisa, t_s)

plt.figure(figsize=(10, 5))
plt.plot(t, s_kontinu, color=WARNA[0], linewidth=1.8, label="Sinyal kontinu (harmonisa 1-9)")
titik, garis, dasar = plt.stem(t_s, s_diskrit, label=f"Hasil sampling (fs = {fs} Hz)")
plt.setp(garis, color=WARNA[1], linewidth=1.2)
plt.setp(titik, color=WARNA[1], markersize=5)
plt.setp(dasar, color="black", linewidth=1)
plt.title("Gambar 3. Sinyal hasil penjumlahan harmonisa dan proses sampling")
plt.xlabel("Waktu (s)")
plt.ylabel("Amplitudo")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig("gambar3_sampling.png", dpi=150)

# ---------------------------------------------------------------
# Gambar 4 - Spektrum frekuensi (domain frekuensi)
# ---------------------------------------------------------------
n_spektrum = np.arange(1, 16)
amplitudo = np.where(n_spektrum % 2 == 1, 4 / (np.pi * n_spektrum), 0)

plt.figure(figsize=(10, 4))
titik, garis, dasar = plt.stem(n_spektrum * f0, amplitudo)
plt.setp(garis, color=WARNA[0], linewidth=2)
plt.setp(titik, color=WARNA[0], markersize=6)
plt.setp(dasar, color="black", linewidth=1)
for n, a in zip(n_spektrum, amplitudo):
    if a > 0:
        plt.text(n * f0, a + 0.04, f"{a:.2f}", ha="center", fontsize=8)
plt.title("Gambar 4. Spektrum amplitudo gelombang kotak (hanya frekuensi ganjil)")
plt.xlabel("Frekuensi (Hz)")
plt.ylabel("Amplitudo")
plt.xticks(n_spektrum * f0)
plt.ylim(0, 1.45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("gambar4_spektrum.png", dpi=150)

# Ringkasan angka di terminal
print(f"Frekuensi sampling        : {fs} Hz")
print(f"Frekuensi tertinggi       : {max(harmonisa) * f0} Hz")
print(f"Syarat Nyquist (2 x fmax) : {2 * max(harmonisa) * f0} Hz -> "
      f"{'terpenuhi' if fs > 2 * max(harmonisa) * f0 else 'TIDAK terpenuhi'}")
print(f"Nilai puncak sinyal       : {s_kontinu.max():.3f}")

plt.show()
