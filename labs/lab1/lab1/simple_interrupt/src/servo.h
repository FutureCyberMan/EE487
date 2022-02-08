/*
 * servo.h
 *
 * Created: 2/24/2015 7:28:17 AM
 *  Author: Korpela
 */ 

#include <avr/io.h>

// #define F_CPU 16000000U

void servo_init(void);
void servo_set(uint8_t p);