#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, wxID_FRAME1STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(341, 167), size=wx.Size(535, 258),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(535, 258))

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Hola', name='staticText1', parent=self, pos=wx.Point(216,
              16), size=wx.Size(25, 18), style=0)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label=u'aceptar',
              name='button1', parent=self, pos=wx.Point(112, 96),
              size=wx.Size(85, 30), style=0)

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label=u'cancelar',
              name='button2', parent=self, pos=wx.Point(296, 96),
              size=wx.Size(85, 32), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
