#include "Arduino.h"
#include "Vrekrer_scpi_parser.h"
#include <max6675.h>

int CSK1=10;
int CS1=9;
int SO1=8;

int CSK2=6;
int CS2=5;
int SO2=4;

//Registro de temperaturas
float temperaturas[2] = {0, 0};

//Contador de tiempo
unsigned long tiempo_de_medida = 0;

MAX6675 termopar1(CSK1,CS1,SO1);
MAX6675 termopar2(CSK2,CS2,SO2);

SCPI_Parser instrument;
const int salidaPWM = 11;

void setup() {
  instrument.RegisterCommand(F("*IDN?"), &Identify);
  instrument.RegisterCommand(F("OUTPut:VOLTage"), &SetVoltage);
  instrument.RegisterCommand(F("MEASure:TEMPerature#?"), &GetTemperature);

  Serial.begin(9600);
  pinMode(salidaPWM,OUTPUT);
  analogWrite(salidaPWM,0);
}

void loop() {
  if ( tiempo_de_medida > millis() ) {
    //Mide cada 250 ms (tiempo minimo soportado por el hardware)
    tiempo_de_medida += 250;
    temperaturas[0] = termopar1.readCelsius();
    temperaturas[1] = termopar2.readCelsius();
  }
  
  instrument.ProcessInput(Serial, "\n");
  delay(1);
}

void Identify(SCPI_C commands, SCPI_P parameters, Stream& interface){  
  interface.println(F("FC-UNI, Thermal Diffusivity Instrument, SN001, v1.0"));
}

void SetVoltage(SCPI_C commands, SCPI_P parameters, Stream& interface){
  if(parameters.Size() > 0){
    float voltage = constrain(String(parameters[0]).toFloat(), 0, 10);
    float pwm = voltage/10.0*255;
    analogWrite(salidaPWM, static_cast<int>(pwm));
  }
}

void GetTemperature(SCPI_C commands, SCPI_P parameters, Stream& interface){
  String header = String(commands.Last());
  header.toUpperCase();
  int suffix = -1;
  sscanf(header.c_str(),"%*[TEMPRAU]%u", &suffix);

  if ( (suffix >= 1) && (suffix <= 2) ) {
    interface.println(temperaturas[suffix-1]);
  }
}
