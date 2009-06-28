#!/usr/bin/python
# -*- coding: utf-8 -*-

# - Imports -------------------------------------------------------------------
import sys
import string
import xml.sax 
import numpy

# - Types ---------------------------------------------------------------------
class BarMonkConfigDB(xml.sax.handler.ContentHandler):             
    def __init__(self):
        self.controllers = {}
        self.ingredients = {}
        self.groups = {}
        self.ingredients = {}

    def startDocument(self):                                    
        self.controllers = {}
        self.ingredients = {}
        self.groups = {}
        self.drinks = {}

    def endDocument(self):                                      
        None
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

    def endElement(self, name):
        None

    def characters(self, chrs):
        None

    def getGroups(self):
        returnVal=sorted(self.groups.keys())
        returnVal.insert(0, FAV_GROUP)
        returnVal.insert(0, ALL_GROUP)
        return returnVal
    
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

    def activateController(self, controllerId, durations ):
        controller=self.controllers[ controllerId ]
        mesg=BACKEND_COMMAND + controller[ USB_ID_ATTRIBUTE ] +u' '+ controller[ SERIAL_ATTRIBUTE ] +u' '
        for i in range (0, int(controller[OUTPUTS_ATTRIBUTE]) ):
            mesg = mesg + str(int(durations[ i ])) + u' '
        print mesg
        #os.system( mesg + ' >> /tmp/barmonk')
        #os.system('echo "' + mesg + '" >> /tmp/barmonk')
        

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

    def getControllers(self):
        return self.controllers.keys()
        
    def getNumOutputs(self, controllerId ):
        if controllerId in self.controllers.keys():
            return int(self.controllers[controllerId][OUTPUTS_ATTRIBUTE])
        else:
            return 0
        

# - Data ----------------------------------------------------------------------
ID_ATTRIBUTE=u'id'
FAV_ATTRIBUTE=u'fav'
GROUP_ATTRIBUTE=u'type'
DESC_ATTRIBUTE=u'desc'
OUTPUTS_ATTRIBUTE=u'outputs'
OUTPUT_ATTRIBUTE=u'output'
MULT_ATTRIBUTE=u'multiplier'
CONTROLLER_ATTRIBUTE=u'controller'
USB_ID_ATTRIBUTE=u'phidget_usb_productid'
SERIAL_ATTRIBUTE=u'phidget_serial'
ALL_GROUP=u'All'
FAV_GROUP=u'Favorites'

CONTROLLER_ELEMENT=u'controller'
INGREDIENT_ELEMENT=u'ingredient'
GROUP_ELEMENT=u'group'
DRINK_ELEMENT=u'drink'

CONTROLLERS_ELEMENT=u'controllers'
INGREDIENTS_ELEMENT=u'ingredients'
GROUPS_ELEMENT=u'groups'
DRINKS_ELEMENT=u'drinks'

BACKEND_COMMAND=u'barmonk '

# - Modules -------------------------------------------------------------------
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

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print 'usage: python test.py infile.xml'
        sys.exit(-1)
    test(args[0])

# - Start ---------------------------------------------------------------------
if __name__ == '__main__':
    main()

