Bar Monkey Robotic Bartender
============================

Introduction
------------
1. This package contains a collection of tools for operating a automated drink mixing machine based on a Phidgets controller.
2. This page also covers our experimentation, designs and implementation of our own bar monkey.
3. "What is a bar monkey?" you may ask. It is an automated mixed drink vending robot. Many people have worked on this area before. Our goal was to make a more sophisticated system with a simplified design.
4. The design was broken up between us based on our areas of expertise. and separate reproducible sub-components.
5. For our initial revision we decided upon 16 different ingredient paths allowing for ~200 different drinks. We also decided against the pumps common in most other designs. As solenoid valves and pneumatic systems are still required, we went with a constant pressure system with solenoid valves. This cut cost and complexity.

Pneumatics
----------
1. 5 lb CO2 canister
2. Pressure Regulator
3. Gas Manifold

Hydraulics
----------
1. 2 Liter Canisters
2. Bulk head quick connect fittings
3. Solenoid Valves
4. Flow Rate Calculations

Electronics
-----------
1. The solenoids that were selected were rated for running at 24VDC at X watts. I had an old power supply that met the requirements and decided to use that. They also were default closed so if the machine loses power it won't be pouring drinks.
2. The controller circuit that was selected was the [0/16/16 Phidget](http://www.phidgets.com/products.php?category=0&product_id=1012). It was rated for 30V, had Debian GNU/Linux libraries and 16 outputs.
3. At the [Trenton Computer Festival](https://tcf-nj.org/), I came upon a used Fujitsu Stylistic LT C-500 for only $75. It has a touchscreen, battery backup, wireless IR keyboard, on board sound and a docking station with networking and power connectors. It was a donation so it had its hard drive wiped clean no OS and now drives from which to install, but I was able to find an online site describing how to install a basic Debian GNU/Linux system.
4. The wiring was fairly straight forward. The phidget instructions make a good reference. I wired the negative terminal from my power supply to one of the common ground terminals on the phidget. I then wired one lead from each solenoid to a common Positive source from the power supply. I then wired each of the solenoids remaining leads to one of the output terminals on the phidget. Now when the phidget output it turned on, the solenoid completes it's connection to ground and is able to switch on.

Note
: The phidgets have over-current protection to buffer them against the direct connection of an inductor. Other control circuits may need additional buffering if the terminal connects directly to a transistor or else extreme voltage spikes could result. It seems unlikely that a control circuit without an external power supply could drive a solenoid valve. If you get solenoids designed for AC or high voltage, you may want to consider getting more isolation by using one of the relay models, these will have a lower switching speed though.

Software
--------
1. A wealth of software went into building up the controller, fortunately we were able to largely leverage Open Source Software to speed up development. Once we had a working base Debian system we made sure we had the following packages: libphidgets-dev, python-wxgtk2.8, python-numpty. We were running with the LXDE desktop environment and also installed a music player (gmpc/mpd) so that the machine could function as a jukebox while dishing out drinks.
2. On top of this base I created a C based command line utility that would connect to the phidget and cycle thru each output turning it on for a certain period of time. This command `barmonk` takes the Phidget USB ID (0x44) and the serial number as its first parameters to know which phidget to use. The remaining parameters are a list of how long to turn on each output in microseconds. If you get errors, make sure you are in the phidgets group and check this [bug report](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=338750).
3. A wxPython Graphical User Interface, `wxbarmonkgui`, was the next piece of software. It parses the list of drinks, ingredients and controllers to create a menu for the user to select which drink to make. The `drinks.xml` file is the configuration database of the entire control software. New drinks can be added for personal preference. Ingredient properties can be changed, including the ever important multiplier field which is how long the ingredient must be on in microseconds to get 1 ounce (~30 ml). The shot drinks in the menu should pour that one multiplier amount. We use them and a graduated cylinder to tune the system. For 20 PSI and 1/16" opening our times should be pretty close or use 1000000 for new ingredients. The controller section needs to be set to use the correct serial number of the phidget. The system could be upgraded to 32 ingredients just by adding a second controller, 16 more ingredients and the drinks to use them to the XML. Drink groups can be created and drinks moved between groups and favorites with the XML as well. In order to fill the dead space I chose a quite nice image from the Debian version of the [openclipart](https://openclipart.org/) package. Of course, feel free to replace it with anything you'd rather look at.
4. We also created a cgi-bin, `barcgi.py`, that would allow other front ends, such as a flash interface in the works, to contact the back end and get a drink poured.

### Tools

barmonk
: a command line control program written in C.

wxbarmonkgui
: a python based front end to barmonk using the wxWidgets framework that provides drink selection features.

barcgi.py
: a cgi script frontend to barmonk that allows alternative frontends to interoperate (such as Flash).


### Requirements
- [libphidgets(libphidgets-dev)](http://libphidgets.alioth.debian.org/)
- [wxpython(python-wxgtk2.8)](http://wxpython.org/what.php)
- [python-numpy](http://numpy.scipy.org/)
- [Doxygen](http://www.stack.nl/~dimitri/doxygen/index.html) - to generate API documentation

### Install

To build barmonk:
```
    make
```

To build the api documentation:
```
    make doc
```

To install into file system:
```
    make install
```

Note
: This was built on a Debian system and may make some file system assumptions accordingly. Editing the Makefile will allow you to adjust target directories however the run times assume locations for the image and configuration data, but will try `./` as well.

#### [Software Releases](https://github.com/tedkotz/barmonk/releases)
- [barmonk_20090711_release](https://github.com/tedkotz/barmonk/releases/tag/v1.0.1)
- [barmonk_20090703_release](https://github.com/tedkotz/barmonk/releases/tag/v1.0.0)

User Interfaces
---------------
1. There was a more CPU/Memory intensive flash interface. It has on screen tutorials, dancing monkeys and a more pleasing full screen mode.

Wrap Up
-------
1. If you have questions, feel free to drop us a line.
2. We will try to post answers to questions on this site. As well as update as we get more chance to add content/new releases. So keep your eyes open.

TODO
----

- [ ] Update python to python 3.0 compatible
- [ ] Add support to use RaspberryPi GPIOs instead of Phidget
- [ ] Update to newer version of wxpython
- [ ] Convert recipe database to JSON
- [ ] Add support for storing but not displaying invalid recipes
- [ ] Create HTML5 based Web front end
- [ ] Add support for arbitrary length shift register based outputs
- [ ] Build an Android APP to control the Phidget over USB

