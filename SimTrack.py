
import numpy as np

class SimTrack:
    
    def __init__(self, _charge, _hit_id):
        self.charge = _charge
        self.hit_id = _hit_id
    
    def __repr__(self):
        cs = "+"
        if -1 == self.charge:
            cs = "-"

        return "%s %d" % ( cs, self.hit_id )
