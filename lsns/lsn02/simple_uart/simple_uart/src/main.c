/*******************************************************************
 * CDT Snuffy                                                      *
 * USART                                                           *
 * 12 January 2021                                                 *
 * EE487                                                           *
 * COL Korpela                                                     *
 *                                                                 *
 * File name: main.c                                               * 
 * Description: UART serial I/O example                            *
 *******************************************************************/

/* Include statements */
#include "uart.h"
#include <avr/io.h>
#include <util/delay.h>

/* Main program */

int main(void)
{
	/* Declare variables */
	unsigned char keypress;	

	/* Initialize UART */
	UART_init();	
	
	/* Main program */
	while (1)
	{	
		// Transmit character 'a' to ensure UART is working
		UART_transmit('a');
		// Transmit an entire string
		//UART_print_string("Hello world\n");
		_delay_ms(500);
	}

	return(1);
}

/*******************************************************************/