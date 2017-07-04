import logging
import gevent
import traceback

class _Adapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        thread_id = id(gevent.getcurrent())
        msg = '(thread-%d) %s' % (thread_id, msg)
        return msg, kwargs

def getLogger(name):
	return _Adapter(logging.getLogger(name), {})
	
def format_exc():
	return traceback.format_exc().replace('\n', '; ')
	
