#
# @author Jean-Lou Dupont
#
#
PRJ=rb_lastfmdk

PYTHON=`which python`
RBP=/usr/lib/rhythmbox/plugins

all:
	@echo "make install"
	@echo "make clean"
	@echo "make buildsrc"

clean:
	@rm -f $(DESTDIR)/*.pyc
		
install:
	@install -D $(CURDIR)/lastfmdk/__init__.py          $(DESTDIR)$(RBP)/lastfmdk/__init__.py
	@install -D $(CURDIR)/lastfmdk/dkplayer.py          $(DESTDIR)$(RBP)/lastfmdk/dkplayer.py
	@install -D $(CURDIR)/lastfmdk/lastfmdk.rb-plugin   $(DESTDIR)$(RBP)/lastfmdk/lastfmdk.rb-plugin
	@python -m py_compile ${DESTDIR}$(RBP)/lastfmdk/__init__.py ${DESTDIR}$(RBP)/lastfmdk/dkplayer.py
	
buildsrc:
	debuild -S