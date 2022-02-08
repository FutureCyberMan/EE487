/*
 * servo.c
 *
 * Created: 2/24/2015 7:29:29 AM
 *  Author: Korpela
 * ATmega328P with a 16 MHz CPU clock
 */ 

#include "servo.h"
#include <avr/io.h>

// These settings are for a Parallax standard servo
// https://www.parallax.com
// Good reference: https://embedds.com/controlling-servo-motor-with-avr/

// Form Fast PWM, one tick is 4us - so divide desired time by 4us
const static uint16_t servo_max = 562;	//2250 / 4us;
const static uint16_t servo_min = 187;	//750 / 4us;

void servo_init(void) {
	// Set pin to output - OC1A
	// Connect servo signal pin to PORTB.1, pin 9 on Arduino
	DDRB |= (1<<PB1);
	
	// Timer Top
	ICR1 = 4999; // (16MHz/64/50Hz) = 1+TOP -> page 102 in ATmega328P datasheet
	
	// Initial compare value 50%
	// Scale servo range for 0 to 180 degrees, 90 degrees is neutral position
	servo_set(90);
			
	// Set mode and start timer (Timer1)
	// Modes of operation on Page 109 of ATmega328P datasheet
	TCCR1A |= (0<<WGM10) | (1<<WGM11) | (1<<COM1A1) | (0<<COM1A0);			// Fast pwm = 14 & Enable pwm on OC1A
	TCCR1B |= (1<<WGM12) | (1<<WGM13) | (0<<CS12) | (1<<CS11) | (1<<CS10);	// Fast pwm = 14 & Clk/64
}

/*! \param p 0-255 */
void servo_set(uint8_t p) {
	uint16_t pos = (servo_max-servo_min)*(p/180.0) + servo_min;
	OCR1A = pos;
}