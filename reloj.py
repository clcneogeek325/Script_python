import pygtk
pygtk.require('2.0')
import gobject
import gtk
import gtk.glade
import re
from cf.gui.AppBase import AppBase
from cf.ifaces.DateTime import dateIface, timeIface, timeZoneIface
import Clock

def clock_widget(*args):
    return Clock.Clock()

class DateTimeApp(AppBase):
    def __init__(self, default_cont = None, default_city = None, utc = False, curr_time = None):
        gtk.glade.set_custom_handler(clock_widget)
        super(DateTimeApp, self).__init__('datetime.glade', 'datetime')
        self.continentCBEntry = self.xml.get_widget('continentCBEntry')
        self.cityCBEntry = self.xml.get_widget('cityCBEntry')
        self.utcCBut = self.xml.get_widget('utcCBut')
        self.hourSpinBut = self.xml.get_widget('hourSpinBut')
        self.minSpinBut = self.xml.get_widget('minSpinBut')
        self.secSpinBut = self.xml.get_widget('secSpinBut')
        self.calendar = self.xml.get_widget('calendar')
        self.timeChanged = False
        
        self.populateTimeZones()
        self.__setDefaultValues(default_cont, default_city, utc, curr_time)
        
        self.hourSpinBut.connect('changed', self.__timeChanged)
        self.minSpinBut.connect('changed', self.__timeChanged)
        self.secSpinBut.connect('changed', self.__timeChanged)
    
    def __timeChanged(self, *args):
        self.timeChanged = True
    
    def __setDefaultValues(self, continent, city, utc, time_dict):
        if continent:
            conts = self.continentCBEntry.get_model()
            for (i, cont) in enumerate(conts):
                if cont[0] == continent:
                    self.continentCBEntry.set_active(i)
                    break
        if city:
            cities = self.cityCBEntry.get_model()
            for (i, c) in enumerate(cities):
                if c[0] == city:
                    self.cityCBEntry.set_active(i)
                    break
        if utc:
            self.utcCBut.set_active(utc)
        
        curr_time = {}
        if time_dict:
            curr_time = time_dict
        else:
            curr_time = timeIface.get_time()
        self.hourSpinBut.set_value(curr_time['hour'])
        self.minSpinBut.set_value(curr_time['min'])
        self.secSpinBut.set_value(curr_time['sec'])
    
    @staticmethod
    def splitTZName(tz_name):
        tz_patt = re.compile(r'^(\w+?)/(.+)')
        
        return tz_patt.match(tz_name).groups()
    
    def populateTimeZones(self):
        self.timeZones = {} # Splitted tz names
        continentsLS = gtk.ListStore(gobject.TYPE_STRING)
        
        self.continentCBEntry.connect('changed', self.populateCities)
        
        # Split time-zone name
        for tz in timeZoneIface.get_tz_list():
            (continent, city) = self.splitTZName(tz['tz'])
            if not continent in self.timeZones:
                self.timeZones[continent] = []
            self.timeZones[continent].append(city)
        
        # Populate continent list
        for cont in self.timeZones.keys():
            continentsLS.append([cont])
        
        continentsLS.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self.continentCBEntry.set_model(continentsLS)
        self.continentCBEntry.set_text_column(0) 
        self.continentCBEntry.set_active(0)
    
    def populateCities(self, widget):
        '''
        Load cities list when continent changes.
        '''
        citiesLS = gtk.ListStore(gobject.TYPE_STRING)
        curr_cont =  widget.child.get_text()
        
        for city in self.timeZones[curr_cont]:
            citiesLS.append([city])
        
        citiesLS.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self.cityCBEntry.set_model(citiesLS)
        self.cityCBEntry.set_text_column(0) 
        self.cityCBEntry.set_active(0)
    
    def onApply(self, w):
        # Make time dictionary
        if self.timeChanged:
            time_dict = {'hour' : self.hourSpinBut.get_value_as_int(),
                         'min'  : self.minSpinBut.get_value_as_int(),
                         'sec'  : self.secSpinBut.get_value_as_int()}
        else:
            time_dict = timeIface.get_time()
        
        # Set time zone
        tz = "%s/%s" % (self.continentCBEntry.child.get_text(), self.cityCBEntry.child.get_text())
        utc = self.utcCBut.get_active()
        timeZoneIface.set_timezone({'tz' : tz, 'utc' : utc})
        
        # Set date
        date = {}
        (date['year'], date['month'], date['day']) = self.calendar.get_date()
        date['month'] += 1
        dateIface.set_date(date)
        
        # Set time
        timeIface.set_time(time_dict)
        
        gtk.Widget.destroy(self.win)

if __name__ == '__main__':
    tz = timeZoneIface.get_timezone()
    (default_cont, default_city) = DateTimeApp.splitTZName(tz['tz'])
    DateTimeApp(default_cont, default_city, tz['utc']).run()
