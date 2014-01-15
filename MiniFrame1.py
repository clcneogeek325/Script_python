#Boa:MiniFrame:MiniFrame1

import wx

def create(parent):
    return MiniFrame1(parent)

[wxID_MINIFRAME1] = [wx.NewId() for _init_ctrls in range(1)]

class MiniFrame1(wx.MiniFrame):
    def _init_ctrls(self, prnt):
        wx.MiniFrame.__init__(self, style=wx.DEFAULT_FRAME_STYLE, name='', parent=prnt, title='MiniFrame1', pos=(341, 167), id=wxID_MINIFRAME1, size=(911, 445))

    def __init__(self, parent):
        self._init_ctrls(parent)
