#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_GC9A01A.h>
#include <Encoder.h>

#define TFT_DC   9
#define TFT_CS   10
#define TFT_RST  8

#define ENCODER_BTN 4
Encoder myEnc(3, 2);  
unsigned long lastEvent = 0;

Adafruit_GC9A01A tft(TFT_CS, TFT_DC, TFT_RST);

int volume = 0;
int lastVolume = -1;
long oldPos = 0;

bool mute = false;
unsigned long buttonDownTime = 0;
bool inMenu = false;
int displayMode = 0;
bool backlightOn = true;

int16_t centerX, centerY;

void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

  Serial.begin(9600);
  pinMode(ENCODER_BTN, INPUT_PULLUP); 

  tft.begin();
  tft.fillScreen(GC9A01A_BLACK);

  centerX = tft.width() / 2;
  centerY = tft.height() / 2;

  DrawVolume(volume);

  Serial.println("NAME:Change_Volume1");
}

void loop() {
  HandleEncoder();
  HandleButton();
  HandleSerial();
}

void DrawVolume(int vol){
  char buf[10];
  sprintf(buf, "%d%%", vol);
  DrawText(buf);
}

void DrawText(const char* txt) {
  tft.fillRect(centerX - 50, centerY - 20, 100, 40, GC9A01A_BLACK);

  tft.setTextColor(GC9A01A_WHITE);
  tft.setTextSize(4);

  int16_t x1, y1;
  uint16_t w, h;
  tft.getTextBounds(txt, 0, 0, &x1, &y1, &w, &h);

  tft.setCursor(centerX - w / 2, centerY - h / 2);
  tft.print(txt);
}

// === Обработка вращения энкодера ===
void HandleEncoder() {
  long newPos = myEnc.read() / 4;

  if (newPos != oldPos) {// && !inMenu)
    if (millis() - lastEvent > 30) {
      if (newPos > oldPos) Serial.println("UP");
      else Serial.println("DOWN");
      oldPos = newPos;
      lastEvent = millis();
    }
    else {
      myEnc.write(oldPos * 4); // сбрасываем в предыдущее положение
    }
  }
}

// === Обработка кнопки энкодера ===
void HandleButton() {
  static bool wasPressed = false;
  bool pressed = digitalRead(ENCODER_BTN) == LOW;

  if(pressed && !wasPressed){
    buttonDownTime = millis();
  }

  if(!pressed && wasPressed){
    unsigned long pressDuration = millis() - buttonDownTime;
    if (pressDuration > 50 && pressDuration < 800) {
      Serial.println("MUTE");
      if (!mute) DrawVolume(volume);
    }
    else if (pressDuration > 800) {
      // длинное → меню
      Serial.println("MENU");
      // inMenu = !inMenu;
      // if (inMenu) showMenu();
      // else redrawVolume();
    }
  }

  wasPressed = pressed;
}

// === Приём данных от Python (проценты громкости) ===
void HandleSerial() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    if(line == "MUTE") {
      DrawText("MUTE");
      mute = true;
      lastVolume = 0;
    }
    else {
      mute = false;
      volume = line.toInt();
      if (!mute && volume != lastVolume && !inMenu) {
        DrawVolume(volume);
        lastVolume = volume;
      }
    }
  }
}