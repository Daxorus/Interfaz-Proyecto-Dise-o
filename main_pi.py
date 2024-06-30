from machine import Pin, ADC
import sys
import time



adc = ADC(Pin(26))        # create ADC object on ADC pin
factor = 3.3/65535




while True:
    
    data = adc.read_u16() * factor 
  
    sys.stdout.write(str(data))
    sys.stdout.write(str(","))
    sys.stdout.write(str(0.0))
    sys.stdout.write(str("\n"))
    time.sleep_ms(1000)

    