import serial
import time

class ArduinoCommand:
    def __init__(self, port=None): 
        if port:
            self.my_serial = serial.Serial(port, 9600, timeout=1)  # Initialize with the given port
        time.sleep(2)  # Allow time for Arduino to reset
        self.hat_tem = 0
        self.hat_hum = 0
        self.inc_tem = 0
        self.inc_hum = 0
        self.characters = ""
        self.numbers = ""

    def read_values(self):
        try:
            # Read sensor data from Arduino
            values = self.my_serial.read_until(b" done").decode('utf-8').strip()
            
            # Reset characters and numbers
            self.characters = ""
            self.numbers = ""

            # Separate into integers and characters
            for value in values:
                if value.isdigit() or value == '.' or value == '-':
                    self.numbers += value
                else:
                    self.characters += value

            # Print for debugging
            # print(f"Characters: {self.characters}")
            # print(f"Numbers: {self.numbers}")

            # Extract values based on the characters
            if "tempreture_of_hat=" in self.characters:
                self.hat_tem = float(self.numbers)
            elif "humidety_of_hat=" in self.characters:
                self.hat_hum = float(self.numbers)
            elif "tempreture_of_inc=" in self.characters:
                self.inc_tem = float(self.numbers)
            elif "humidety_of_inc=" in self.characters:
                self.inc_hum = float(self.numbers)

            # Print for debugging
            # print(f"hat_tem: {self.hat_tem}, hat_hum: {self.hat_hum}, inc_tem: {self.inc_tem}, inc_hum: {self.inc_hum}")

            return self.hat_tem, self.hat_hum, self.inc_tem, self.inc_hum
        except serial.SerialException as e:
            print(f"Error reading from serial port: {e}")
            return None

    def close_serial(self):
        self.my_serial.close()

    def my_serial_write(self, string):
        """Send command to Arduino in string, for example:
        my_serial_write("move_to_x")
        NOTE: send numbers in a similar format to make it easier for the Arduino to find them.
        Know that x in this case is a number, integer, representing a position as an index for the place to move to.
        """
        self.my_serial.write(string.encode())
        print(string)
        time.sleep(0.5)  # Small delay to ensure data is sent
        response = self.my_serial.readline().decode("utf-8").strip()
        print(response)

    def read_line(self):
        try : 
            if self.my_serial.in_waiting > 0:
                line = self.my_serial.readline().decode('utf-8').rstrip()
                print(line)
                return line
        except :
            print("no line to read ") 
            
    

    @staticmethod
    def find_arduinos():
        move_arduino = None
        env_arduino = None

        for i in range(3):
            port = f"/dev/ttyACM{i}"
            try :
                arduino = ArduinoCommand(port)
                arduino.my_serial_write("move")
                time.sleep(1)  # Give some time for the Arduino to respond

                response = arduino.read_line()
                print(f"Response from {port}: {response}")  # Debugging print
                if response== "move":
                    move_arduino = arduino
                    print(f"{port} is set as move_arduino")
                elif response and response.endswith("done"):
                    env_arduino = arduino
                    print(f"{port} is set as env_arduino")
            except : 
                print(f"port {port} didn't connect ")

            return move_arduino, env_arduino

# Example usage
if __name__ == "__main__":
    move_arduino, env_arduino = ArduinoCommand.find_arduinos()

    if move_arduino and env_arduino:
        print("Both Arduinos are set correctly.")
    else:
        print("Failed to set one or both Arduinos.")
