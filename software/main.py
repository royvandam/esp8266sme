import usocket as socket
import board
import time

CONTENT = b"""\
HTTP/1.0 200 OK

# Environment
bme280_temperature_celcius %d
bme280_pressure_hpa %d.%02d
bme280_humidity_percent %d.%02d
"""

NOT_FOUND = b"""\
HTTP/1.0 404 Not Found

Error 404 - Page not found
"""

if __name__ == '__main__':
    while True:
        while not board.wlan.isconnected():
            time.sleep(0.9)
            board.led.red.on()
            time.sleep(0.1)
            board.led.red.off()

        board.led.green.on()

        ai = socket.getaddrinfo("0.0.0.0", 8080)

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(ai[0][-1])
        s.listen(5)

        while True:
            client = s.accept()

            client_stream = client[0]
            client_addr = client[1]

            print("Connection from:", client_addr)
            request = client_stream.readline()
            print("Request:", request)
            while True:
                header = client_stream.readline()
                if header == b"" or header == b"\r\n":
                    break
                #print(header)

            if not request.startswith('GET /metrics'):
                client_stream.write(NOT_FOUND)
                client_stream.close()
                continue

            t, p, h =  board.bme.read_compensated_data()

            t = t / 100
            p = p // 256
            pi = p // 100
            pd = p - pi * 100

            hi = h // 1024
            hd = h * 100 // 1025 - hi * 100

            client_stream.write(CONTENT % (t, pi, pd, hi, hd))
            client_stream.close()
