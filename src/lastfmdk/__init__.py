"""
    Rhythmbox plugin for Last.fm desktop client
    
    Sends the current playing details to Last.fm Desktop Client 
    
    @author: Jean-Lou Dupont
"""

import rhythmdb, rb #@UnresolvedImport
import dkplayer

PLUGIN_NAME="lastfmdk"

class LastFMDKPlugin (rb.Plugin):
    
    def __init__ (self):
        rb.Plugin.__init__ (self)
        self.current_entry=None
        self.details=None

    def activate (self, shell):
        self.shell = shell
        sp = shell.get_player ()
        self.cb = (
                   sp.connect ('playing-song-changed', self.playing_song_changed)
                   ,sp.connect('playing-changed',      self.playing_changed)
                   )

    def deactivate (self, shell):
        self.shell = None
        sp = shell.get_player()
        
        for id in self.cb:
            sp.disconnect (id)

    def playing_changed (self, sp, playing):
        fncName="_h"
        if self.new_song:
            self.new_song = False
            fncName+="New"
            
            if playing: fncName+="Playing"
            else:       fncName+="Stopped"
        else:
            if playing: fncName+="Resumed"
            else:       fncName+="Paused"
        
        # dynamic dispatch
        getattr(self, fncName)()        
        
        
    def _hNewPlaying(self):
        """
        New Song started playing
        """
        self.details=EntryHelper.track_details(self.shell, self.current_entry)
        print self.details
        
        dkp = dkplayer.dkPlayer(PLUGIN_NAME)
        
        try:    dkp.announce_start(**self.details)
        except: print "Last.fm Desktop Client unreachable"
    
    def _hNewStopped(self):
        """
        New Song loaded
        """
        #self.details=EntryHelper.track_details(self.shell, self.current_entry)
        
    
    def _hPaused(self):
        """
        Current Song paused
        """
        dkp = dkplayer.dkPlayer(PLUGIN_NAME)
        try:     dkp.announce_pause()
        except:  pass
    
    def _hResumed(self):
        """
        Current Song resumed
        """
        dkp = dkplayer.dkPlayer(PLUGIN_NAME)
        try:     dkp.announce_resume()
        except:  pass
    
            
    def playing_song_changed (self, sp, entry):
        """
        Just grab the current playing entry
        The rest of the work will be done through the
        event "playing_changed"
        """
        self.current_entry = sp.get_playing_entry()
        self.new_song=True
        



class EntryHelper:
    """
    Helper functions for song database entries
    """
    props = {   "artist":    rhythmdb.PROP_ARTIST
                ,"album":    rhythmdb.PROP_ALBUM
                ,"duration": rhythmdb.PROP_DURATION
                ,"track":    rhythmdb.PROP_TITLE
                ,"mb_id":    rhythmdb.PROP_MUSICBRAINZ_TRACKID
                ,"duration": rhythmdb.PROP_DURATION
             }
    
    @classmethod
    def track_details(cls, shell, entry):
        """
        Retrieves details associated with a db entry
        
        @return: (artist, title)
        """
        db = shell.props.db
        result={}
        try:
            for prop, key in cls.props.iteritems():
                result[prop]=db.entry_get(entry, key)
        except:
            pass
        return result
    
