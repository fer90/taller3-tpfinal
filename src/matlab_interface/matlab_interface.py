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

    def solve_both(self, na, nbr, nc, d):

        ret = self.eng.resonancia(float(na), float(nbr), float(nc), float(d))

        # La funcion devuelve [[lista de nbi][lista de nz]]
        return ret[0][1::-1]

    def solve_parallel(self, na, nbr, nc, d):

        # ret = self.eng.resonancia_paralelo(float(na), float(nbr), float(nc), float(d))

        # return ret[0][1::-1]
        pass

    def solve_perpendicular(self, na, nbr, nc, d):

        # ret = self.eng.resonancia_paralelo(float(na), float(nbr), float(nc), float(d))

        # return ret[0][1::-1]
        pass

#interface = MatlabInterface()
#interface.solve_both()
