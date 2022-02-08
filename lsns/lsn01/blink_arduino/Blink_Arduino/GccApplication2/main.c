/*
 * Blink LED on Arduino
 * 
 * LED on Arduino board is connect to PB5 (which is referred to as Pin13 in the Arduino IDE)
 * 
 * Created: 1/18/2017 12:23:20 PM
 * Author : LTC Lowrance
 * Edits  : COL Korpela, 1/16/2021
 */ 

#define F_CPU 16000000UL				// Arduino clock frequency - 16 MHz

#include <avr/io.h>
#include <util/delay.h>

int main(void)
{
	DDRB = DDRB | (1 << PB5);			// OR Mask - set PB5 on PORTB to output
	
	while(1)
	{
		PORTB = PORTB | (1 << PB5);		// OR mask to set only PB5 or Pin13 on Arduino
		_delay_ms(1000);
		PORTB = PORTB & ~(1 << PB5);	// AND mask to clear only PB5 - turn off LED
		_delay_ms(1000);
	}
}