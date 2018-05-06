import smbus  
from time import sleep 
  
# General i2c device class so that other devices can be added easily  
class i2c_device:  
    def __init__(self, addr, port):  
        self.addr = addr  
        self.bus = smbus.SMBus(port)  

    def write(self, byte, backlight=0x08):  
        self.bus.write_byte(self.addr, byte | backlight)
        sleep(0.0001)

    def read(self):  
        return self.bus.read_byte(self.addr)  
  
class lcd:  
 #initializes objects and lcd  
    def __init__(self, addr, port):  
        self.lcd_device = i2c_device(addr, port)  
        self.lcd_device.write((0x03<<4))
        sleep(0.01)
        self.lcd_device.write((0x03<<4))
        sleep(0.01)
        self.lcd_device.write((0x03<<4))
        sleep(0.01)
        self.lcd_device.write((0x02<<4))
        sleep(0.0001)
        
        self.lcd_write(0x28)  # 2 lines and 5x8 dot matrix
        sleep(0.002)
        self.lcd_write(0x08)  # display off, cursor off, blink off
        sleep(0.002)
        self.lcd_write(0x01)  # clear screen
        sleep(0.005)
        self.lcd_write(0x06)  # increment right and do not shift screen
        sleep(0.002)
        self.lcd_write(0x0C)  # display on,
        sleep(0.002)
        self.lcd_write(0x0F)  # display on, cursor on, blink on
        sleep(2)
        
    # clocks EN to latch command  
    def lcd_strobe(self):
        cur = self.lcd_device.read()
        self.lcd_device.write((cur | 0x04))  
        self.lcd_device.write((cur & 0xFB))  

    # write a command to lcd  
    def lcd_write(self, cmd):
        self.lcd_device.write(((cmd >> 4)<<4))  # most significant nibble
        self.lcd_strobe()  
        self.lcd_device.write(((cmd & 0x0F)<<4))  # least significant nibble       
        self.lcd_strobe()
        sleep(0.0001)
      #  self.lcd_device.write(0x0| 0x08)  # clear data

    # write a character to lcd (or character rom)  
    def lcd_write_char(self, charvalue):  
        self.lcd_device.write((0x01 | ((charvalue >> 4)<<4)))
        self.lcd_strobe()  
        self.lcd_device.write((0x01 | ((charvalue & 0x0F))<<4))  
        self.lcd_strobe()
        sleep(0.0001)
        #self.lcd_device.write(0x0| 0x08)
        
    def lcd_backlight_off(self):
        self.lcd_device.write(0x00, backlight= 0x00)

    # put string function  
    def lcd_puts(self, string, line):  
        if line == 1:  
            self.lcd_write(0x80)  
        if line == 2:  
            self.lcd_write(0xC0) 
        for char in string:  
            self.lcd_write_char(ord(char))
            
    def lcd_write_continue(self, string):
        for char in string:  
            self.lcd_write_char(ord(char))

    # clear lcd and set to home  
    def lcd_clear(self):  
        self.lcd_write(0x1)
        sleep(0.005)
        self.lcd_write(0x2)
        sleep(0.005)

    
if __name__=="__main__":
    lcd = lcd(0x27,1)  
    lcd.lcd_puts("Raspberry Pi",1)  #display "Raspberry Pi" on line 1
    sleep(1)
    lcd.lcd_puts("  Take a byte!",2)  #display "Take a byte!" on line 2  
    sleep(1)
    lcd.lcd_clear()
    lcd.lcd_puts("4,000 = ",1)
    sleep(1)
    lcd.lcd_write_continue("3,985")
    sleep(1)
    lcd.lcd_backlight_off()