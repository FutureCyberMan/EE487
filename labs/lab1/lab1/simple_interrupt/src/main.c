/*******************************************************************
 * CDT Liebers                                                     *
 * EE487                                                           *
 * COL Korpela                                                     *
 *                                                                 *
 * simple_interrupt												   *
 *																   *
 *******************************************************************/ 
 
//#define F_CPU 16000000UL

#include <avr/io.h>
#include <avr/interrupt.h>
#include "uart.h"
#include <stdlib.h>
#include <stdio.h>
#include "servo.h"
#include <util/delay.h>

unsigned char toggle;
unsigned int temp = 80;
unsigned int Ftemp;
char output[36];

/*******************************************************************/
/* Interrupt Service Routine for External Interrupt 0 */
/* Turn on/off the LED */

ISR(INT0_vect)
{
	temp = temp - 1;
	// itoa(temp, output, 10);
	// UART_print_string(output);
	// UART_print_string("BAAAAAAD");
	
}
ISR(INT1_vect)
{
	temp = temp + 1;
	// itoa(temp, output, 10);
	// UART_print_string(output);
	// UART_print_string("BAAAAAAD");
	
}

/*******************************************************************/

int main(void)
{

	DDRB = DDRB | (1 << PB5);			// OR Mask - set PB5 on PORTB to output
	PORTB = PORTB & ~(1 << PB5);		// AND mask to clear only PB5 - turn off LED
	
	PORTD = PORTD | (1 << PD2);			// Pull up PD2 which is external INT0
	PORTD = PORTD | (1 << PD3);         // Pull up PD3 which is external INT1
		
	/* Enable INT0 external interrupt */
	// EICRA = ( 1<<ISC01 ) | ( 1<<ISC00 );	// Set interrupt trigger to a falling edge
	EICRA = 0xF; // See EICRA for INT0 and INT1 falling edge configuration
	//EIMSK = ( 1<<INT0);					// Set INT0 enable bit
	//EIMSK = ( 1<<INT1);
	EIMSK = 0x3;

	/* Enable global interrupts */
	sei();
	
	UART_init();
	int pos = 0;
	servo_init();
	//_delay_ms(500);
	
	unsigned char channel = 0;			// Connect analog signal to PORTF.0, Channel 0
	unsigned int adc_data;				// Variable for ADC results
	
	ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
	ADMUX |= (1 << REFS0) | channel;	// Set reference to AVCC and channel
	ADCSRA |= (1 << ADSC);				// Set the bit to start the conversion
	UART_print_string("THIS IS THE START OF THE PROGRAM\n\n");
	while(1)
	{
		// Your program here
		while(ADCSRA & (1 <<ADSC));		// Waits for ADC conversion to complete
		adc_data = ADCW;				// Read all 10 bits into variable
		
		float voltage = adc_data * (5000 / 1024.0);
		float Ctemp = voltage / 10;
		Ftemp = (Ctemp * 9)/5 + 32;
		UART_print_string("\n\n");
		sprintf(output, "Current Temp: %d Desired Temp: %d\r", Ftemp, temp);
		UART_print_string(output);
		
		if (Ftemp > temp) {
			pos += 1;
			servo_set(pos);
			PORTB = PORTB | (1 << PB5);
			// _delay_ms(15);
			// sprintf(output, "Current Temp: %d Desired Temp: %d\r\n\n", Ftemp, temp);
			// UART_print_string(output);
		} else PORTB = PORTB & ~(1 << PB5);	// AND mask to clear only PB5 - turn off LED

		ADCSRA |= (1 << ADSC);			// Set the bit to start conversion again
	}
}