// #define FASTLED_ESP32_I2S

#include <Arduino.h>
#include <Ethernet.h>
#include <FastLED.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

// ESP32 Settings
const unsigned int SERIAL_SPEED = 460800;

// Ethernet Settings
const unsigned int W5500_CS = 5;
const unsigned int localPort = 8888;
EthernetUDP Udp;
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 0, 177);

// Led Settings
const unsigned int NUM_LEDS_PER_MATRIX = 256;
const unsigned int NUM_LEDS = NUM_LEDS_PER_MATRIX * 6;
const unsigned int BUFFER_SIZE = NUM_LEDS * 3;
const unsigned int CHUNK_BUFFER_SIZE = BUFFER_SIZE / 4;
byte frameBuffer[BUFFER_SIZE];

CRGB leds[NUM_LEDS];

void setupEthernet() {
    Ethernet.init(W5500_CS);
    if (Ethernet.begin(mac) == 0) {
        Serial.println("Error al configurar Ethernet usando DHCP");
        Ethernet.begin(mac, ip);
    }
    delay(1000);
    Serial.println("Configuración Ethernet completada");
    Serial.print("Dirección IP: ");
    Serial.println(Ethernet.localIP());
}

void updateLeds() {
    for (int i = 0; i < NUM_LEDS; ++i) {
        int offset = i * 3;
        leds[i] = CRGB(frameBuffer[offset], frameBuffer[offset + 1], frameBuffer[offset + 2]);
    }
    FastLED.show();
    // Serial.println(FastLED.getFPS());
}

void ledUpdateTask(void *pvParameters) {
    while (true) {
        updateLeds();
        vTaskDelay(1);
    }
}

void udpReceiveTask(void *pvParameters) {
    while (true) {
        int packetSize = Udp.parsePacket();
        if (packetSize) {
            byte chunkNumber = Udp.read();

            if (chunkNumber < 4) {
                int offset = chunkNumber * CHUNK_BUFFER_SIZE;
                Udp.read(frameBuffer + offset, CHUNK_BUFFER_SIZE);
            }
        }
        vTaskDelay(1);
    }
}

void setup_leds(){
    FastLED.addLeds<WS2812B, 26, GRB>(leds, 0, NUM_LEDS_PER_MATRIX);                        // 0,1 - Pin 26
    FastLED.addLeds<WS2812B, 27, GRB>(leds, NUM_LEDS_PER_MATRIX, NUM_LEDS_PER_MATRIX);      // 0,2 - Pin 27
    FastLED.addLeds<WS2812B, 25, GRB>(leds, NUM_LEDS_PER_MATRIX * 2, NUM_LEDS_PER_MATRIX);  // 0,3 - Pin 25
    FastLED.addLeds<WS2812B, 14, GRB>(leds, NUM_LEDS_PER_MATRIX * 3, NUM_LEDS_PER_MATRIX);  // 1,0 - Pin 14
    FastLED.addLeds<WS2812B, 12, GRB>(leds, NUM_LEDS_PER_MATRIX * 4, NUM_LEDS_PER_MATRIX);  // 1,1 - Pin 12
    FastLED.addLeds<WS2812B, 13, GRB>(leds, NUM_LEDS_PER_MATRIX * 5, NUM_LEDS_PER_MATRIX);  // 1,2 - Pin 13
    FastLED.setBrightness(50);
    FastLED.clear();
}

void setup() {
    Serial.begin(SERIAL_SPEED);
    Serial.println("Iniciando...");
    setupEthernet();
    Udp.begin(localPort);
    Serial.println("Configuración completada.");
    setup_leds();
    xTaskCreatePinnedToCore(ledUpdateTask, "LedUpdateTask", 10000, NULL, 1, NULL, 0);
    xTaskCreatePinnedToCore(udpReceiveTask, "UdpReceiveTask", 10000, NULL, 1, NULL, 1);
}

void loop() {
    vTaskDelay(portMAX_DELAY);
}
