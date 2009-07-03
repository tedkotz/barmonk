#!/usr/bin/python
# -*- coding: utf-8 -*-
## 
# @file wxbarmonkgui.py
# @author  Ted Kotz <ted@kotz.us>
# @version 1.0
#
# @section LICENSE
#
# Copyright 2009-2009 Theodore Kotz.  All rights reserved.
#  See license distributed with this file and
#  available online at http://www.tyrfing.org/barmonk/license.txt
#
# @section DESCRIPTION
#
# The Wx Widgets GUI frontend to the bar monkey controller
# 

# - Imports -------------------------------------------------------------------
import os
import wx
import config_db
import xml.sax 

# - Types ---------------------------------------------------------------------

##
# The dialog that allows the user to confirm their drink selection.
#
class MixFrame(wx.Dialog):
    ##
    # @var config
    #   The configuration database and connection to the backend
    #

    ##
    # @var drinkName
    #   The description of the drink to mix.
    #
    
    ##
    # Constructor.
    #
    # @param self Object reference.
    # @param parent The parent component
    # @param config The configuration database and conection to the backend
    # @param drinkName The description of the drink to mix.
    #
    def __init__(self, parent, config, drinkName):
        wx.Dialog.__init__(self, name='', parent=parent,
            title=u'Mix Your Drink?', size=wx.Size(450,300))

        self.config=config
        self.drinkName=drinkName

        panel = wx.Panel(self)
        
        # contents of panel
        textLabel=wx.StaticText(label=u'Mix '+drinkName+u':', parent=panel ) 
        panel2 = wx.Panel(panel)
        panel3 = wx.Panel(panel)

        #contents of panel3
        mixButton = wx.Button(label=u'Mix', parent=panel3)
        mixButton.Bind(wx.EVT_BUTTON, self.OnMixButton)

        cancelButton = wx.Button(label=u'Cancel', parent=panel3)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancelButton)

        recipe=self.config.getRecipe( self.drinkName )

        # contents and layout of panel2
        grid = wx.GridSizer( rows=0, cols =4 )
        for i in sorted(recipe.keys()):
            grid.Add(wx.StaticText(panel2, wx.ID_ANY, i ) , 1, wx.EXPAND | wx.ALL, 1)
            textCtrl = wx.TextCtrl(panel2, wx.ID_ANY, str(recipe[i]) ) 
            grid.Add(textCtrl , 1, wx.EXPAND | wx.ALL, 1)
            textCtrl.SetEditable( False )


        panel2.SetSizer(grid)	
        
        #layout of panel3
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(cancelButton, 0, wx.ALL , 4 )
        hbox.Add(mixButton, 0, wx.ALL , 4 )
        panel3.SetSizer(hbox)
        
        #layout of panel
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(textLabel, 1, wx.EXPAND | wx.ALL , 2 )
        vbox.Add(panel2, 8, wx.EXPAND | wx.ALL , 1 )
        vbox.Add(panel3, 0, wx.ALIGN_RIGHT , 0  )
        panel.SetSizer(vbox)	
    
    ##
    # Cancel button handler
    #
    # @param self Object reference.
    # @param event the initiating event
    #
    def OnCancelButton(self, event):
        self.Close()
    
    ##
    # Mix button handler.
    #
    # @param self Object reference.
    # @param event the initiating event
    #
    def OnMixButton(self, event):
        self.config.mixDrink( self.drinkName )
        self.Close()

##
# A panel that holds a wxImage
#
class ImagePanel(wx.Panel):
    ##
    # @var image
    #   the wxImage to display 
    #
    
    ##
    # Constructor
    #
    # @param self Object reference.
    # @param parent The parent component
    # @param id The WxWidgets ID
    # @param img The WxImage contents
    #
    def __init__(self, parent, id, img):
        wx.Panel.__init__(self, parent, id)
        
        self.image = img
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    
    ##
    # The paint event handler method
    #
    # @param self Object reference.
    # @param event The initiating event
    #
    def OnPaint(self, event):
        size=self.GetSize()
        bitmap=self.image.Scale((size.GetWidth()-4),(size.GetHeight()-4),wx.IMAGE_QUALITY_NORMAL).ConvertToBitmap()
        dc = wx.PaintDC(self)
        dc.DrawBitmap(bitmap, 2, 2)
        
    
    ##
    # The Resize event handler
    #
    # @param self Object reference.
    # @param event The initiating event
    #
    def OnSize(self, event):
        self.Refresh()

##
# The Barmonkey apllications main frame
#
class BarMonkFrame(wx.Frame):
    ##
    # @var config
    #   The configuration database and connection to the backend.
    #

    ##
    # @var filterListBox
    #   The list box containing the drink groups to filter on.
    #

    ##
    # @var barMonkListBox
    #   The list box containing the filtered drink list.
    #

    ##
    # constructor
    #
    # @param self Object reference.
    # @param parent The parent component
    # @param config The configuration database and conection to the backend
    # @param image The image to show in the right box
    #
    def __init__(self, parent, config, image):
        wx.Frame.__init__(self, name='', parent=parent, size=wx.Size(800, 600),
            style=wx.DEFAULT_FRAME_STYLE, title=u'Bar Monkey')

        self.config=config

        panel = wx.Panel(self, wx.ID_ANY)

        self.filterListBox = wx.ListBox(choices= sorted(self.config.getGroups()), parent=panel )
        self.filterListBox.Bind(wx.EVT_LISTBOX, self.OnFilterListBox)
        
        self.barMonkListBox = wx.ListBox(choices=sorted(self.config.getDrinks(config_db.FAV_GROUP)), parent=panel )
        self.barMonkListBox.Bind(wx.EVT_LISTBOX, self.OnBarMonkListBox)

        imagePanel = ImagePanel(panel, wx.ID_ANY, wx.Image(image))


        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.filterListBox, 2, wx.EXPAND | wx.ALL , 2 )
        hbox.Add(self.barMonkListBox, 3, wx.EXPAND | wx.ALL , 2 )
        hbox.Add(imagePanel, 5, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.TOP, 2 )
        panel.SetSizer(hbox)
    
    ##
    # The filter selection handler
    #
    # @param self Object reference.
    # @param event The initiating event
    #
    def OnFilterListBox(self, event):
        selName = self.filterListBox.GetStringSelection()
        tmplist=self.config.getDrinks(selName)
        if tmplist == None:
            self.barMonkListBox.SetItems([])
        else:
            self.barMonkListBox.SetItems(sorted(tmplist))
    
    ##
    # The drink selection handler
    #
    # @param self Object reference.
    # @param event The initiating event
    #
    def OnBarMonkListBox(self, event):
        selName = self.barMonkListBox.GetStringSelection()
        mixDialog=MixFrame(self, self.config, selName)
        mixDialog.Centre()
        mixDialog.ShowModal()
        self.barMonkListBox.DeselectAll()
    
# - Data ----------------------------------------------------------------------

# - Modules -------------------------------------------------------------------

##
# Main function loads configuration then kicks off interface.
#
def main():
    panelImage = "/usr/local/share/images/monkey_head_nicu_buculei_01.png"
    sourceFileName = "/etc/barmonk.xml"

    homedir=os.environ["HOME"]
    
    if os.path.isfile(homedir +'/.barmonkrc'):
        execfile(homedir + '/.barmonkrc')

    if not os.path.isfile(panelImage):
        panelImage = os.path.basename(panelImage)

    if not os.path.isfile(sourceFileName):
        sourceFileName = os.path.basename(sourceFileName)
    
    # Create an instance of the Handler.
    handler = config_db.BarMonkConfigDB()
    # Create an instance of the parser.
    parser = xml.sax.make_parser()
    # Set the content handler.
    parser.setContentHandler(handler)
    # Start the parse.
    parser.parse(sourceFileName)
    
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    frame = BarMonkFrame(None, handler, panelImage)
    frame.Centre()
    frame.Show()
    
    app.MainLoop()




# - Start ---------------------------------------------------------------------
if __name__ == '__main__':
    main()

