/*******************************************************************
 * CDT Snuffy                                                      *
 * USART                                                           *
 * EE487                                                           *
 * COL Korpela                                                     *
 *                                                                 *
 * File name: uart.h                                               *
 * Description: UART header file                                   *
 *******************************************************************/

/* Include Statement */
#include "config.h"

/* UART Settings */
#define UART_BAUD_RATE  9600
#define UART_DATA_BIT_8  (( 1 << UCSZ01 ) | ( 1 << UCSZ00 ))
#define UART_PARITY_NONE (( 0 << UPM01 )  | ( 0 << UPM00 ))
#define UART_STOP_BIT_1   ( 0 << USBS0 )

#define UBRR_INIT   (( F_CPU / 16 / UART_BAUD_RATE ) - 1 )

#define UCSRA_INIT  0
#define UCSRB_INIT  (( 0 << RXCIE0 ) | ( 1 << RXEN0 ) | ( 1 << TXEN0 ))
#define UCSRC_INIT  (( 0 << UMSEL01 ) | ( 0 << UMSEL00 ) | ( UART_DATA_BIT_8 | UART_PARITY_NONE | UART_STOP_BIT_1 ))

/* Function prototypes */
void UART_init (void);
void UART_transmit (unsigned char);
unsigned char UART_receive (void);
void UART_print_string (char str[]);

