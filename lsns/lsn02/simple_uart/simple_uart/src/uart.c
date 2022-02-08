/*******************************************************************
 * CDT Snuffy                                                      *
 * USART                                                           *
 * EE487                                                           *
 * COL Korpela                                                     *
 *                                                                 *
 * File name: uart.c                                               *
 * Description: Parallel IO example                                *
 *******************************************************************/

/* Include statements */
#include <avr/io.h>
#include "uart.h"

/*******************************************************************/
/* Functions */
/*******************************************************************/

void UART_init (void)
{
	/* Set Baudrate to 9600 for an 8 Mhz clock */
	UBRR0H = UBRR_INIT >> 8;
	UBRR0L = UBRR_INIT & 0xFF;

	/* Enable receiver and transmitter */
    UCSR0A = UCSRA_INIT;
    UCSR0B = UCSRB_INIT;
    UCSR0C = UCSRC_INIT;
}

/*******************************************************************/

void UART_transmit (unsigned char data)
{
	while (!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
}

/*******************************************************************/

unsigned char UART_receive (void)
{
	while (!(UCSR0A & (1<<RXC0)));
	return (UDR0);
}

/*******************************************************************/

void UART_print_string (char str[])
{
	int k = 0;
	
	while (str[k] != 0x00)
	{
		UART_transmit(str[k]);
		k = k + 1;
	}
}

/*******************************************************************/