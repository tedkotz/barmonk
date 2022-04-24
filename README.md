This package contains a collection of tools for operating a automated drink mixing machine based on a Phidgets controller.

Tools
	barmonk - a command line control program written in C.
	wxbarmonkgui - a python based front end to barmonk using the wxWidgets framework that provides drink selection features.
	barcgi.py - a cgi script frontend to barmonk that allows alternative frontends to interoperate (such as Flash).
	

Requirements
	libphidgets(libphidgets-dev) - http://libphidgets.alioth.debian.org/
	wxpython(python-wxgtk2.8) - http://wxpython.org/what.php
	python-numpy - http://numpy.scipy.org/
	Doxygen - to generate API documentation - http://www.stack.nl/~dimitri/doxygen/index.html
	
	
Install
  To build barmonk:
	make
  To build the api documentation:
	make doc
  To install into file system:
	make install

Notes:
  This was built on a debian system and may make some file system assumptions accordingly. Editing the Makefile will allow you to 
  adjust target directories however the runtimes assume locations for the image and configuration data, but will try ./ as well.
  