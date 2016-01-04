import serial
from time import sleep
from sys import argv
import os

SAVEFILE = "relay_state_file.dat"
if (os.name == 'nt'):
  SERIAL_PORT = 'COM5'
else:
  SERIAL_PORT = '/dev/cu.usbmodem1421'

def update_relay(state):
  ser = serial.Serial(SERIAL_PORT, 9600)
  sleep(2)
  ser.write(state)
  ser.close()

def update_if_needed(new_state, old_state):
  if (new_state != old_state):
    update_relay(new_state)

def get_old_state_from_file(filename):
  old_state = '0'
  try:
    with open(filename, "r") as text_file:
      old_state = text_file.read()
  except IOError:
    # File doesn't exist, that's okay. Assume state is '0'
    pass
  return old_state

def write_state_to_file(filename, state):
  with open(filename, "w+") as text_file:
    text_file.write(state)


def main():
  toggle = False
  if (len(argv) < 2):
    # Didn't pass status, assuming toggle
    toggle = True
  else:
    new_state = str(argv[1])
    if (new_state != '0' and new_state != '1'):
      toggle = True

  old_state = get_old_state_from_file(SAVEFILE)
  if (toggle):
    new_state = '0' if old_state == '1' else '1'

  update_if_needed(new_state, old_state)

  write_state_to_file(SAVEFILE, new_state)


if __name__ == "__main__":
  main()
