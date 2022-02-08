/*******************************************************************
 * CDT Snuffy                                                      *
 * EE487                                                           *
 * COL Korpela                                                     *
 *                                                                 *
 * simple_interrupt												   *
 *																   *
 *******************************************************************/ 
 
#define F_CPU 16000000UL

#include <avr/io.h>
#include <avr/interrupt.h>
//#include "uart.h"
#include <stdio.h>

unsigned char toggle;
//UART_init();

/*******************************************************************/
/* Interrupt Service Routine for External Interrupt 0 */
/* Turn on/off the LED */

ISR(INT0_vect)
{
	PORTB = PORTB ^ (1 << PB5);
	//UART_transmit('a');
	//printf("a");
}

/*******************************************************************/

int main(void)
{

	DDRB = DDRB | (1 << PB5);			// OR Mask - set PB5 on PORTB to output
	PORTB = PORTB & ~(1 << PB5);		// AND mask to clear only PB5 - turn off LED
	
	PORTD = PORTD | (1 << PD2);			// Pull up PD2 which is external INT0
		
	/* Enable INT0 external interrupt */
	// EICRA = ( 1<<ISC01 ) | ( 1<<ISC00 );	// Set interrupt trigger to a falling edge
	EICRA = 0x3;
	EIMSK = ( 1<<INT0  );					// Set INT0 enable bit

	/* Enable global interrupts */
	sei();
	
	while(1)
	{
		// Your program here
	}
}