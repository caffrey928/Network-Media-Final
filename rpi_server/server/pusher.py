import RPi.GPIO as GPIO
import time

def pusher():
    BUTTON_PIN = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    previous_button_state = GPIO.input(BUTTON_PIN)

    CONTROL_PIN = 11
    PWM_FREQ = 50

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN, GPIO.OUT)

    pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
    pwm.start(12)

    degrees = [12.0, 7.0, 2.0, 12.0]
    try:
        while True:
            time.sleep(0.01)
            button_state = GPIO.input(BUTTON_PIN)
            if button_state != previous_button_state:
                previous_button_state = button_state
                if button_state == GPIO.HIGH:
                    print("Pressed")
                    for i in range(1):
                        for deg in degrees:
                            pwm.ChangeDutyCycle(deg)
                            time.sleep(3)
    except KeyboardInterrupt:
        pwm.ChangeDutyCycle(0)
        pwm.stop()
        GPIO.cleanup()
        print("End")
