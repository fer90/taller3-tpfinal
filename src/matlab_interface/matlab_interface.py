# -*- coding: utf-8 -*-

import matlab.engine

"""
Esta clase es la encargada de interfacear con el script en matlab
"""

class MatlabInterface(object):

    def __init__(self):

        super(MatlabInterface, self).__init__()

        self.future = matlab.engine.connect_matlab(async=True)
        
        self.eng = self.future.result()

    def solve_m_range(self):

        pass

    def solve_both(self):

        ret = self.eng.resonancia(float(1.0), float(1.3), float(1.5), float(2))
        
        return ret[0][0:1]

    def solve_parallel(self):

        pass

    def solve_perpendicular(self):

        pass

#interface = MatlabInterface()
#interface.solve_both()
