#include <phidgets/interfacekit.h>
#include <stdio.h>
#include <unistd.h>


void play_frame( PhidgetInterfaceKit* pik, int* frame )
{
	int i;
	phidget_return preturnVal;
	
	usleep(100000);
}


int main( int argc , char** argv )
{
	phidget_return preturnVal;
	PhidgetInterfaceKit* pik=phidget_new_PhidgetInterfaceKit();
	int x;
	long tmp;


	phidget_init();
	if (argc<2 || argc>17)
	{
		printf( "%s <1-16 durations in usec>\n", argv[0] );
	}
	else if( (preturnVal=phidget_interfacekit_open( 
		pik, 
		PHIDGETS_USB_PRODUCTID_INTERFACEKIT_0_16_16, 
		81213,
		1000)) != PHIDGET_RET_SUCCESS )
	{
		printf ( "Unable to connect: reason %d\n", (int)preturnVal );
	}
	else
	{
		for( x=0; x<16; x++)
		{
			pik->digitalOutput[x] = 0;
		}
		if( (preturnVal=phidget_interfacekit_digitaloutputs_update(pik)) != PHIDGET_RET_SUCCESS )
		{
			printf ( "Unable to status: reason %d\n", (int)preturnVal );
		}
		
		for( x=1; x < argc; x++ )
		{
			tmp=atol(argv[x]);
			if(tmp>0)
			{
				pik->digitalOutput[x-1]=1;
				if( (preturnVal=phidget_interfacekit_digitaloutputs_update(pik)) != PHIDGET_RET_SUCCESS )
				{
					printf ( "Unable to status: reason %d\n", (int)preturnVal );
				}
				if(usleep(tmp)!=0)
				{
					printf ( "usleep error.\n");
				}	
				pik->digitalOutput[x-1]=0;
				if( (preturnVal=phidget_interfacekit_digitaloutputs_update(pik)) != PHIDGET_RET_SUCCESS )
				{
					printf ( "Unable to status: reason %d\n", (int)preturnVal );
				}
			}
		}
	
		for( x=0; x<16; x++)
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

