from concoord import *
from exception import *

class DLock():
    def __init__(self):
        self.locked = False
        self.holder = None
        self.queue = []
        self.atomic = Lock()
    
    def acquire(self, kwargs):
        _concoord_designated, _concoord_owner, _concoord_command = kwargs['_concoord_designated'], kwargs['_concoord_owner'], kwargs['_concoord_command']
        with self.atomic:
            if self.locked:
                self.queue.append(_concoord_command)
                raise UnusualReturn
            else:
                self.locked = True
                self.holder = _concoord_command.client

    def release(self, kwargs):
        _concoord_designated, _concoord_owner, _concoord_command = kwargs['_concoord_designated'], kwargs['_concoord_owner'], kwargs['_concoord_command']
        with self.atomic:
            ### Release on unacquired lock
            if len(self.queue) > 0:
                newcommand = self.queue.pop(0)
                self.holder = newcommand.client
                # return to new holder which is waiting
                return_outofband(_concoord_designated, _concoord_owner, newcommand)
            elif len(self.queue) == 0:
                self.holder = None
                self.locked = False
                
    def __str__(self):
        temp = 'Distributed Lock'
        temp += "\nholder: %s\nqueue: %s\n" % (self.holder, " ".join([str(m) for m in self.queue]))
        return temp
