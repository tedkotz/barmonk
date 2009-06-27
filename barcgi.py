#!/usr/bin/python
# -*- coding: utf-8 -*-

# - Imports -------------------------------------------------------------------
import cgi, os
import config_db
import xml.sax
import numpy

# - Types ---------------------------------------------------------------------
# - Data ----------------------------------------------------------------------
CONTENT_TYPE=u'Content-Type: text/plain\n\n'
INGREDIENT_BASE_NAME=u'item'

# - Modules -------------------------------------------------------------------
def main():
    sourceFileName = "barmonk.xml"

    homedir=os.environ["HOME"]
    
    if os.path.isfile('/etc/barmonk/config'):
            execfile('/etc/barmonk/config')
    
    # Create an instance of the Handler.
    handler = config_db.BarMonkConfigDB()
    # Create an instance of the parser.
    parser = xml.sax.make_parser()
    # Set the content handler.
    parser.setContentHandler(handler)
    inFile = open(sourceFileName, 'r')
    # Start the parse.
    parser.parse(inFile)                                        
    # Alternatively, we could directly pass in the file name.
    #parser.parse(inFileName)
    inFile.close()

    # Required header that tells the browser how to render the text.
    print CONTENT_TYPE

    form = cgi.FieldStorage()
    
    # default to the first controller
    controller_id = sorted(handler.getControllers())[0]

    outputs= handler.getNumOutputs( controller_id )

    durations = numpy.zeros(outputs)
    for i in range(outputs):
        key=INGREDIENT_BASE_NAME+str(i)
        if ( key in form.keys() ):
            durations[i] = int( form.getvalue(key))
        else:
            durations[i] = 0

    handler.activateController( controller_id, durations )

# - Start ---------------------------------------------------------------------
if __name__ == '__main__':
    main()


