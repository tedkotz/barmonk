/**
 * @file    barmonk.c
 * @author  Theodore Kotz <ted@kotz.us>
 * @version 1.0
 *
 * @section LICENSE
 *
 * Copyright 2009-2009 Theodore Kotz.  All rights reserved.
 *  See license distributed with this file and
 *  available online at http://[Project Website]/license.html
 *
 * @section DESCRIPTION
 *
 * Backend Barmonkey controller command line interface.
 * 
 */

 
/* Includes ******************************************************************/
#include <phidgets/interfacekit.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


/* Defines *******************************************************************/
/* Types *********************************************************************/

/**
 * Enumerated List of command line argument ordering
 *
 */
typedef enum 
{
    ARG_COMMAND=0,
    ARG_PRODUCT_ID,
    ARG_SERIAL,
    ARG_DURATION_0,
    MIN_ARG_COUNT
} ARGS;


/* Interfaces ****************************************************************/
/* Data **********************************************************************/
/* Functions *****************************************************************/

/**
 * Main execution point.
 *
 * Takes in the command line arguments. Does some basic syntax checking. 
 * Then connects to the specified Phidget and pulses each output for the
 * specified duration.
 *
 * @param argc the number of command line arguments
 * @param argv the values of the command line arguments
 * @return Always successful (0) unless exit() it called.
 */
int main( int argc , char** argv )
{
    phidget_return preturnVal;
    PhidgetInterfaceKit* pik=phidget_new_PhidgetInterfaceKit();
    int x;
    long tmp;


    phidget_init();
    if (argc < MIN_ARG_COUNT )
    {
        printf( "\n\nToo Few Parameters:\n%s <usb product id> <serial> [<durations in usec> ...]\n", argv[ARG_COMMAND] );
    }
    else if( (preturnVal=phidget_interfacekit_open( 
        pik, 
        strtol(argv[ARG_PRODUCT_ID], NULL, 0), 
        strtol(argv[ARG_SERIAL], NULL, 0), 
        1000)) != PHIDGET_RET_SUCCESS )
    {
        printf ( "\n\nUnable to connect: reason %d\n", (int)preturnVal );
    }
    else if( argc > ( ARG_DURATION_0 + pik->numDigitalOutputs ) )
    {
        printf( "\n\nToo Many Parameters, Phidget supports %d:\n %s <usb product id> <serial> [<durations in usec> ...]\n",
            pik->numDigitalOutputs,
            argv[ARG_COMMAND] );
    }
    else
    {
        for( x=0; x<pik->numDigitalOutputs; x++)
        {
            pik->digitalOutput[x] = 0;
        }
        if( (preturnVal=phidget_interfacekit_digitaloutputs_update(pik)) != PHIDGET_RET_SUCCESS )
        {
            printf ( "Unable to status: reason %d\n", (int)preturnVal );
        }
        
        for( x=ARG_DURATION_0; x < argc; x++ )
        {
            tmp=strtol(argv[x], NULL, 0);
            if(tmp>0)
            {
                pik->digitalOutput[x-ARG_DURATION_0]=1;
                if( (preturnVal=phidget_interfacekit_digitaloutputs_update(pik)) != PHIDGET_RET_SUCCESS )
                {
                    printf ( "Unable to status: reason %d\n", (int)preturnVal );
                }
                if(usleep(tmp)!=0)
                {
                    printf ( "usleep error.\n");
                }	
                pik->digitalOutput[x-ARG_DURATION_0]=0;
                if( (preturnVal=phidget_interfacekit_digitaloutputs_update(pik)) != PHIDGET_RET_SUCCESS )
                {
                    printf ( "Unable to status: reason %d\n", (int)preturnVal );
                }
            }
        }
    
        for( x=0; x<pik->numDigitalOutputs; x++)
        {
            pik->digitalOutput[x] = 0;
        }
        if( (preturnVal=phidget_interfacekit_digitaloutputs_update(pik)) != PHIDGET_RET_SUCCESS )
        {
            printf ( "Unable to status: reason %d\n", (int)preturnVal );
        }
    }
    
    
    phidget_interfacekit_close(pik);	
    phidget_delete_PhidgetInterfaceKit(&pik);
    phidget_cleanup();
    if (pik) { free ((void *) pik); pik = NULL; }


    return 0;
}

/*****************************************************************************/

