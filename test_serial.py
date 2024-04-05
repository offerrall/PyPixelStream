import serial
import time

PORT = 'COM3'
BAUD_RATE = 460800

atm_frame = -1  # Comienza desde -1 para manejar correctamente el primer frame
last_frame_time = time.time()

def open_serial_port(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        return ser
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial {port}: {e}")
        return None

def check_data(data):
    global atm_frame, last_frame_time
    key, num = data.split(": ")
    num = int(num)

    if key == "Frame":
        if num != atm_frame:
            current_time = time.time()
            # Solo calcula los FPS si no es el primer frame
            if atm_frame != -1:
                fps = 1.0 / (current_time - last_frame_time)
                print(f"FPS: {fps:.2f}")
            last_frame_time = current_time
            atm_frame = num
    if key == "LEDs FPS":
        print(f"LEDs FPS: {num:.2f}")

def read_serial_data(serial_connection):
    while True:
        if serial_connection.in_waiting > 0:
            data = serial_connection.readline().decode('utf-8', 'ignore').strip()
            check_data(data)

if __name__ == "__main__":
    serial_conn = open_serial_port(PORT, BAUD_RATE)
    if serial_conn:
        print(f"Leyendo datos de {PORT} a {BAUD_RATE} baudios...")
        read_serial_data(serial_conn)
        serial_conn.close()
