"""
    @summary: Last.fm Desktop Client interface
    @author: jldupont
"""
import socket

class dkPlayerException(Exception):
    """
    dkPlayer specific exception
    """
    

class dkPlayer():
    """
    Proxy for the Last.fm Desktop Client
    
    Supports sending the principal commands to the desktop client
    """
    HOST="127.0.0.1"  #safest
    PORT=33367
    TIMEOUT=2         #can't really except to take much more time!
    
    def __init__(self, plugin_name):
        self.plugin_name=plugin_name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.TIMEOUT)
    
    def __del__(self):
        try:    self.sock.close()
        except: pass
    
    def announce_start(self, artist=None, track=None, album=None, mb_id=None, path=None, duration=None):
        """
        Announce the 'start' of a playing track 
        
        Method signature required to be keyword-based
        """
        cmdf="START c=%s&a=%s&t=%s&b=%s&m=%s&l=%s&p=%s\n"
        cmd=cmdf % (self.plugin_name, artist, track, album, mb_id, duration, path)
        return self._send_cmd(cmd)

    def announce_stop(self):
        """
        Announce the end of a track - playing stopped
        """
        cmd="STOP c=%s\n" % self.plugin_name
        return self._send_cmd(cmd)

    def announce_pause(self):
        """
        Announce that the current playing track was paused
        """
        cmd="PAUSE c=%s\n" % self.plugin_name
        return self._send_cmd(cmd)
    
    def announce_resume(self):
        """
        Announce that the current paused track was resumed
        """
        cmd="RESUME c=%s\n" % self.plugin_name
        return self._send_cmd(cmd)

    def _send_cmd(self, cmd):
        """
        Send the command to the desktop client
        
        If the communication protocol changes or the client
        can't be reached, there isn't much that can be done
        hence the reason for not being fancy about exception 
        handling here.
        """
        try:
            self.sock.connect((self.HOST, self.PORT))
            sent_count=self.sock.send(cmd)
            
            #we aren't expecting a long response
            #in the successful case so don't bother much
            response=self.sock.recv(32)
        
            if sent_count != len(cmd):
                raise dkPlayerException("send error")

            return response
 
        except:
            raise dkPlayerException()

        
        

if __name__=="__main__":
    """
    Quick and dirty tests
    """
    import time
    
    p=dkPlayer("test_dkPlayer")
    result=p.announce_start("Depeche Mode", "In Your Room", "Songs of Faith and Devotion", "", "file:///mnt/music/track.mp3", 360)
    print "start: %s" % result
    del p 
    
    time.sleep(2)
    
    p2=dkPlayer("test_dkPlayer")
    print "pause: %s" % p2.announce_pause()
    del p2
    
    time.sleep(2)
    
    p3=dkPlayer("test_dkPlayer")
    print "resume: %s" % p3.announce_resume()
    del p3
    
    time.sleep(2)
    
    p4=dkPlayer("test_dkPlayer")
    print "stop: %s" % p4.announce_stop()

    