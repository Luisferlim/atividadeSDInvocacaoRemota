import serial
import serial.tools.list_ports
import re

#padrao definido por nos
pattern = re.compile(r"T1:\s*([0-9\.\-]+)\s*C\s*\|\s*T2:\s*([0-9\.\-]+)\s*C")

#definimos o boudrate para 115200 (padrao para dispositivos uart)
def find_correct_port(baudrate=115200):
    ports = serial.tools.list_ports.comports()

    print("Procurando porta correta...")

    for port in ports:
        name = port.device.lower()

        # Ignorar automaticamente portas bluetooth
        if "bluetooth" in port.description.lower():
            print(f"⏭ Ignorando porta Bluetooth: {port.device}")
            continue
        if "bth" in name or "bluetooth" in name:
            print(f"⏭ Ignorando porta Bluetooth: {port.device}")
            continue

        try:
            print(f"Testando porta: {port.device}")

            # timeout curto para acelerar
            with serial.Serial(port.device, baudrate=baudrate, timeout=0.1) as ser:

                #lemos duas linhas
                for _ in range(2):
                    line = ser.readline().decode(errors="ignore").strip()
                    if line and pattern.search(line):
                        print("✔ Porta correta encontrada:", port.device)
                        return port.device

        except Exception:
            pass  # ignora erros e segue para próxima

    raise Exception("Nenhuma porta válida encontrada!")

def read_temperatures(port, baudrate=115200):
    with serial.Serial(port, baudrate=baudrate, timeout=1) as ser:
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            match = pattern.search(line)
            if match:
                t1 = float(match.group(1))
                t2 = float(match.group(2))
                print(f"T1 = {t1} °C | T2 = {t2} °C")
                return t1, t2


# -------- PROGRAMA PRINCIPAL --------
porta = find_correct_port()
read_temperatures(porta)
