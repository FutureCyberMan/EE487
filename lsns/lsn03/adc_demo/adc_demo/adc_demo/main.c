/*******************************************************************
 * CDT Snuffy                                                      *
 * EE487                                                           *
 * COL Korpela                                                     *
 *                                                                 *
 * File name: adc_demo.c                                           *
 * Description: Demonstrate ADC interface                          *
 *******************************************************************/

/* Include statements */

#include "config.h"
#include <avr/io.h>
#include <util/delay.h>

/*******************************************************************/
/* Main program */

int main(void)
{
	/* Set up I/O PORTs */
	DDRB = DDRB | (1 << PB5);			// OR Mask - set PB5 on PORTB to output
		
	/* Declare local variables */
	unsigned char channel = 0;			// Connect analog signal to PORTF.0, Channel 0
	unsigned int adc_data;				// Variable for ADC results
		
	/* Initialize ADC */
	ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);  // Enable the ADC with prescaler=128

	/* Set ADC channel and reference */
	ADMUX |= (1 << REFS0) | channel;	// Set reference to AVCC and channel  
	
	/* Start the first conversion */
	ADCSRA |= (1 << ADSC);				// Set the bit to start the conversion	
		
	/* Loop */
	while(1)
	{
		while(ADCSRA & (1 <<ADSC));		// Waits for ADC conversion to complete

		adc_data = ADCW;				// Read all 10 bits into variable

		if ( adc_data > (2.5*1023)/5 )
			PORTB = PORTB | (1 << PB5);	// OR mask to set only PB5 or Pin13 on Arduino - turn on LED
		else
			PORTB = PORTB & ~(1 << PB5); // AND mask to clear only PB5 - turn off LED

		ADCSRA |= (1 << ADSC);			// Set the bit to start conversion again
	}

} // End of main

/*******************************************************************/