import socket
import json
import time
import random

HOST  = "127.0.0.1"
PORT  = 7001

BUS_ID = "M-01"   # <-- her terminalde farklı: M-01, M-02, M-03

sock = socket.socket()
sock.connect((HOST, PORT))
print(f"[{BUS_ID}] Merkeze bağlandı.")

def bildir(durum, durak=None):
    veri = {"id": BUS_ID, "durum": durum}
    if durak:
        veri["durak"] = durak
    sock.sendall((json.dumps(veri) + "\n").encode())

# Merkeze "hazırım" de
bildir("HAZIR")
print(f"[{BUS_ID}] Hazır, görev bekleniyor...")

buffer = ""
while True:
    veri = sock.recv(1024).decode()
    if not veri:
        break
    buffer += veri
    while "\n" in buffer:
        satir, buffer = buffer.split("\n", 1)
        if satir.strip():
            komut = json.loads(satir)
            if komut["komut"] == "GIT":
                durak  = komut["durak"]
                seviye = komut["seviye"]
                sure   = random.randint(5, 10)
                print(f"\n[{BUS_ID}] GÖREV: '{durak}' → Kalabalık: %{seviye}")
                print(f"[{BUS_ID}] Yolda.. ({sure} saniye)")
                time.sleep(sure)
                print(f"[{BUS_ID}] '{durak}' durağına ULAŞILDI!")
                bildir("TESLIM", durak)
                print(f"[{BUS_ID}] Tekrar hazır, yeni görev bekleniyor..\n")
                bildir("HAZIR")