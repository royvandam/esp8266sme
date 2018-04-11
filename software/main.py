import uasyncio as asyncio
import board

HTTP_200_OK = b"""\
HTTP/1.0 200 OK

"""

HTTP_404_NOT_FOUND = b"""\
HTTP/1.0 404 Not Found

Error 404 - Page not found
"""

BOSH_BME280_METRICS = b"""\
# Bosch BME280 Environment Sensor
bme280_temperature_celcius %2.2f
bme280_pressure_hpa %2.2f
bme280_humidity_percent %2.2f
"""

async def monitor_wlan():
    was_connected = False
    while True:
        if board.wlan.isconnected():
            if not was_connected:
                board.led.green.on()
                await asyncio.sleep_ms(1000)
                board.led.green.off()
                was_connected = True
        else:
            board.led.red.on()
            await asyncio.sleep_ms(100)
            board.led.red.off()
            was_connected = False

        await asyncio.sleep_ms(900)

def http_page_metrics(request, writer):
    yield from writer.awrite(HTTP_200_OK)

    # Fetch sensor readings from BME280 sensor
    if hasattr(board, 'bme280'):
        bme280_values =  board.bme280.read_values()
        yield from writer.awrite(BOSH_BME280_METRICS % bme280_values)

@asyncio.coroutine
def http_serve(reader, writer):
    try:
        board.led.blue.on()

        request = (yield from reader.readline())
        print("Request:", request)

        # Read request headers
        while True:
            header = (yield from reader.readline())
            if header == b"" or header == b"\r\n":
                break
            #print(header)

        if request.startswith('GET /metrics'):
            yield from http_page_metrics(request, writer)
        else:
            yield from writer.awrite(HTTP_404_NOT_FOUND)

        yield from writer.aclose()
    finally:
        board.led.blue.off()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_wlan())
    loop.call_soon(asyncio.start_server(http_serve, "0.0.0.0", 8080))
    loop.run_forever()
    loop.close()
