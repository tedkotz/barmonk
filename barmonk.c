#include <phidgets/interfacekit.h>
#include <stdio.h>
#include <unistd.h>


typedef enum 
{
    ARG_COMMAND=0,
    ARG_PRODUCT_ID,
    ARG_SERIAL,
    ARG_DURATION_0,
    MIN_ARG_COUNT
} ARGS;



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
		atoi(argv[ARG_PRODUCT_ID]), 
		atoi(argv[ARG_SERIAL]), 
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
			tmp=atol(argv[x]);
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

