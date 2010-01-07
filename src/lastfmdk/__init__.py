"""
    @author: Jean-Lou Dupont
"""

import rhythmdb, rb

class LastFMDKPlugin (rb.Plugin):
    def __init__ (self):
        rb.Plugin.__init__ (self)

    def activate (self, shell):
        print "activate"
        self.shell = shell
        sp = shell.get_player ()
        self.cb = (
                   sp.connect ('playing-song-changed', self.playing_entry_changed)
                   , sp.connect ('playing-changed', self.playing_changed)
                   , sp.connect ('playing-song-property-changed', self.playing_song_property_changed)
                   )

    def deactivate (self, shell):
        print "deactivate"
        self.shell = None
        sp = shell.get_player ()
        
        for id in self.cb:
            sp.disconnect (id)

    def playing_changed (self, sp, playing):
        if playing:
            print sp.get_playing_entry ()
    
    def playing_entry_changed (self, sp, entry):
        pass
    
    def playing_song_property_changed (self, sp, uri, property, old, new):
        pass
  
