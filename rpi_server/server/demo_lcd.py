#! /usr/bin/env python

# Simple string program. Writes and updates strings.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import drivers
from time import sleep

def lcd(message = "Pay 5Mi to buy"):
    # Load the driver and set it to "display"
    # If you use something from the driver library use the "display." prefix first
    display = drivers.Lcd()

    # Main body of code
    try:
        print("Writing to display")
        # Remember that your sentences can only be 16 characters long!
        display.lcd_display_string("Welcome!", 1)  # Write line of text to first line of display
        display.lcd_display_string(message, 2)  # Write line of text to second line of display
    except KeyboardInterrupt:
        # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        print("Cleaning up!")
        #display.lcd_clear()
# lcd()
