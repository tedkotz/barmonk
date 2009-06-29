# Quick Makefile

CC=gcc
STRIP=strip
LIBS=-lphidgets
CFLAGS=-Wall -O3
PREFIX=/usr/local
PYTHONLIBDIR=$(PREFIX)/lib/python2.5/site-packages
CGIBINDIR=/usr/lib/cgi-bin
CONFIGDIR=/etc
PKG=barmonk
OBJ=barmonk.o
SRCEXT=.c
DOCDIR=doc
DOCCMD=doxygen
DOCCFG=Doxyfile

$(PKG): $(OBJ)
	$(CC) $(LIBS) $(CFLAGS) $(OBJ) -o $(PKG)
	$(STRIP) $(PKG)


$(SRCEXT).o:
	$(CC) $(CFLAGS) -c $<

test: $(PKG)
	./$(PKG)

install: $(PKG)
	cp -i barmonk.xml $(CONFIGDIR)/
	cp $(PKG) $(PREFIX)/bin/
	cp config_db.py $(PYTHONLIBDIR)/
	cp wxbarmonkgui.py $(PREFIX)/bin/
	ln -sf $(PREFIX)/bin/wxbarmonkgui.py $(PREFIX)/bin/wxbarmonkgui
	cp barcgi.py $(CGIBINDIR)/
	mkdir -p $(PREFIX)/share/images/
	cp -i monkey_head_nicu_buculei_01.png $(PREFIX)/share/images/
	
clean-obj:
	rm -rf *~ *.o

clean: clean-obj
	rm -rf $(PKG) *.pyc 

rebuild: clean $(PKG)

doc: 
	$(DOCCMD) $(DOCCFG)

clean-doc: 
	rm -rf $(DOCDIR)

rebuild-doc: clean-doc doc

all: $(PKG) doc

clean-all: clean clean-doc

rebuild-all: clean-all all
