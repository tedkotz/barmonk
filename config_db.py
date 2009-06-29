#!/usr/bin/python
# -*- coding: utf-8 -*-
## 
# @file    config_db.py
# @author  Ted Kotz <ted@kotz.us>
# @version 1.0
#
# @section LICENSE
#
# Copyright 2009-2009 Theodore Kotz.  All rights reserved.
#  See license distributed with this file and
#  available online at http://[Project Website]/license.html
#
# @section DESCRIPTION
#
# This holds the common code for parsing the configuration DB
# 


# - Imports -------------------------------------------------------------------
import sys
import string
import xml.sax 
import numpy
import os

# - Types ---------------------------------------------------------------------
##
# Configuration Parser and Storage Database
class BarMonkConfigDB(xml.sax.handler.ContentHandler):             
    ##
    # @var controllers 
    #   List of controllers by id 
    #
    
    ##
    # @var ingredients 
    #   List of ingredients by id 
    #
    
    ##
    # @var groups 
    #   List of groups by Description
    #
    
    ##
    # @var drinks 
    #   List of drinks by Description 
    #

    ##
    # Constructor
    #
    # @param self object reference
    #
    def __init__(self):
        self.controllers = {}
        self.ingredients = {}
        self.groups = {}
        self.drinks = {}

    ##
    # Start of Document Handler 
    #
    # @param self object reference
    #
    def startDocument(self):                                    
        self.controllers = {}
        self.ingredients = {}
        self.groups = {}
        self.drinks = {}

    ##
    # End of Document Handler
    #
    # @param self object reference
    #
    def endDocument(self):                                      
        None

    ##
    # Start of Element Handler
    #
    # @param self Object reference
    # @param name Element name string
    # @param attrs List of attribute values by attribute name
    #
    def startElement(self, name, attrs):
        if name == CONTROLLER_ELEMENT:
            self.controllers[ attrs.get( ID_ATTRIBUTE )  ] = attrs
        elif name == INGREDIENT_ELEMENT:
            self.ingredients[ attrs.get( ID_ATTRIBUTE ) ] = attrs
        elif name == GROUP_ELEMENT:
            self.groups[ attrs.get( DESC_ATTRIBUTE ) ] = attrs
        elif name == DRINK_ELEMENT:
            self.drinks[ attrs.get( DESC_ATTRIBUTE ) ] = attrs
        elif name == CONTROLLERS_ELEMENT:
            self.controllers = {}
        elif name == INGREDIENTS_ELEMENT:
            self.ingredients = {}
        elif name == GROUPS_ELEMENT:
            self.groups = {}
        elif name == DRINKS_ELEMENT:
            self.drinks = {}
        else:
            None

    ##
    # End of Element Handler
    #
    # @param self Object reference
    # @param name Element name string
    #
    def endElement(self, name):
        None

    ##
    # Characters Handler
    #
    # @param self Object reference
    # @param chrs A block of non-Tag Characters
    #
    def characters(self, chrs):
        None

    ##
    # Returns the list of groups descriptions
    #
    # @param self object reference
    # @return The list of group descriptions
    #
    def getGroups(self):
        returnVal=sorted(self.groups.keys())
        returnVal.insert(0, FAV_GROUP)
        returnVal.insert(0, ALL_GROUP)
        return returnVal
    
    ##
    # Returns the list of drink descriptions of all drinks in the 
    # specified group
    #
    # @param self Object reference
    # @param groupDesc The Description string of the group to search for.
    # @return The list of drink descriptions of all drinks in the 
    #         specified group
    #
    def getDrinks(self, groupDesc):
        if groupDesc == ALL_GROUP:
            return self.drinks.keys()
        elif groupDesc == FAV_GROUP:
            returnVal = []
            for i in self.drinks.keys():
                if int(self.drinks[ i ][FAV_ATTRIBUTE]):
                    returnVal.append( i )
            return returnVal
        elif groupDesc in self.groups.keys():
            returnVal = []
            groupType = self.groups[groupDesc][ID_ATTRIBUTE]
            for i in self.drinks.keys():
                if self.drinks[ i ][GROUP_ATTRIBUTE] == groupType:
                    returnVal.append( i )
            return returnVal
        else:
            None

    ##
    # Activates the specified controller with each output for the 
    # specified duration.
    #
    # @param self object reference
    # @param controllerId The controller id of the controller to activate
    # @param durations The list of durations in usec by output number
    #
    def activateController(self, controllerId, durations ):
        controller=self.controllers[ controllerId ]
        mesg=BACKEND_COMMAND + controller[ USB_ID_ATTRIBUTE ] +u' '+ controller[ SERIAL_ATTRIBUTE ] +u' '
        for i in range (0, int(controller[OUTPUTS_ATTRIBUTE]) ):
            mesg = mesg + str(int(durations[ i ])) + u' '
        print mesg
        os.system( mesg )
        

    ##
    # Mixes the drink with the specified description
    #
    # @param self object reference
    # @param drinkDesc The description of the drink to mix
    #
    def mixDrink(self, drinkDesc):
        if drinkDesc in self.drinks.keys():
            drink = self.drinks[ drinkDesc ]
            recipe = {}
            for i in self.controllers.keys():
                x=self.controllers[ i ][OUTPUTS_ATTRIBUTE]
                recipe[ i ] = numpy.zeros(int(x))
            for i in drink.keys():
                if i in [ FAV_ATTRIBUTE, GROUP_ATTRIBUTE, DESC_ATTRIBUTE ]:
                    None
                elif i in self.ingredients.keys():
                    ingredient=self.ingredients[ i ]
                    recipe[ingredient[CONTROLLER_ATTRIBUTE]][int(ingredient[OUTPUT_ATTRIBUTE])]=float(ingredient[MULT_ATTRIBUTE]) * float(drink[i])
                else:
                    None
            for i in recipe.keys():
                self.activateController( i, recipe[ i ] )
        else:
            None

    ##
    # Returns the list of ounces of each ingredient by ingredient description
    # for the drink with the specified description
    #    
    # @param self Object reference
    # @param drinkDesc The Description of the drink to return
    # @return The list of ounces of each ingredient by ingredient description
    #
    def getRecipe(self, drinkDesc):
        if drinkDesc in self.drinks.keys():
            drink = self.drinks[ drinkDesc ]
            recipe = {}
            for i in drink.keys():
                if i in [ FAV_ATTRIBUTE, GROUP_ATTRIBUTE, DESC_ATTRIBUTE ]:
                    None
                elif i in self.ingredients.keys():
                    ingredient=self.ingredients[ i ]
                    recipe[ingredient[DESC_ATTRIBUTE]]=float(drink[i])
                else:
                    None
            return recipe
        else:
            return None

    ##
    # Return the list of controller IDs
    #
    # @param self object reference
    # @return The list of controller IDs
    #
    def getControllers(self):
        return self.controllers.keys()
        
    ##
    # Return the number of outputs on the specified controller
    #
    # @param self Object reference
    # @param controllerId The specified controller ID
    # @return The number of outputs on the specified controller
    #
    def getNumOutputs(self, controllerId ):
        if controllerId in self.controllers.keys():
            return int(self.controllers[controllerId][OUTPUTS_ATTRIBUTE])
        else:
            return 0
        

# - Data ----------------------------------------------------------------------
##
# xml elemement attribute.
#
ID_ATTRIBUTE=u'id'
##
# xml elemement attribute.
#
FAV_ATTRIBUTE=u'fav'
##
# xml elemement attribute.
#
GROUP_ATTRIBUTE=u'type'
##
# xml elemement attribute.
#
DESC_ATTRIBUTE=u'desc'
##
# xml elemement attribute.
#
OUTPUTS_ATTRIBUTE=u'outputs'
##
# xml elemement attribute.
#
OUTPUT_ATTRIBUTE=u'output'
##
# xml elemement attribute.
#
MULT_ATTRIBUTE=u'multiplier'
##
# xml elemement attribute.
#
CONTROLLER_ATTRIBUTE=u'controller'
##
# xml elemement attribute.
#
USB_ID_ATTRIBUTE=u'phidget_usb_productid'
##
# xml elemement attribute.
#
SERIAL_ATTRIBUTE=u'phidget_serial'

##
# xml elemement name.
#
CONTROLLER_ELEMENT=u'controller'
##
# xml elemement name.
#
INGREDIENT_ELEMENT=u'ingredient'
##
# xml elemement name.
#
GROUP_ELEMENT=u'group'
##
# xml elemement name.
#
DRINK_ELEMENT=u'drink'
##
# xml elemement name.
#
CONTROLLERS_ELEMENT=u'controllers'
##
# xml elemement name.
#
INGREDIENTS_ELEMENT=u'ingredients'
##
# xml elemement name.
#
GROUPS_ELEMENT=u'groups'
##
# xml elemement name.
#
DRINKS_ELEMENT=u'drinks'

##
# The Description for the Group containing all drinks
#
ALL_GROUP=u'All'
##
# The Description for the Group containing all drinks with
# the FAV_ATTRIBUTE set
#
FAV_GROUP=u'Favorites'

##
# The command that calls the C backend
#
BACKEND_COMMAND=u'barmonk '

# - Modules -------------------------------------------------------------------
##
# A simple test of the parsing library
#
# @param inFileName
#
def test(inFileName):
    # Create an instance of the Handler.
    handler = BarMonkConfigDB()
    # Create an instance of the parser.
    parser = xml.sax.make_parser()
    # Set the content handler.
    parser.setContentHandler(handler)
    inFile = open(inFileName, 'r')
    # Start the parse.
    parser.parse(inFile)                                        
    # Alternatively, we could directly pass in the file name.
    #parser.parse(inFileName)
    inFile.close()
    print handler.getGroups()
    print handler.getDrinks('ZAmbo')
    print handler.getDrinks(FAV_GROUP)
    handler.mixDrink( u'Berry Soda' )

##
# A main to call the simple test
#
#
def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print 'usage: python test.py infile.xml'
        sys.exit(-1)
    test(args[0])

# - Start ---------------------------------------------------------------------
if __name__ == '__main__':
    main()

