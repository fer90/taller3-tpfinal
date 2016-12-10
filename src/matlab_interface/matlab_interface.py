# -*- coding: utf-8 -*-

import matlab.engine

import logging

"""
Esta clase es la encargada de interfacear con el script en matlab
"""

class MatlabInterface(object):

    def __init__(self):

        super(MatlabInterface, self).__init__()

        self.future = matlab.engine.connect_matlab(async=True)
        
        self.eng = self.future.result()

    def solve_m_parallel(self, na, nbr, nc, d):

        m0, m1 = self.eng.m_range_p(float(na), float(nbr), float(nc), d, nargout=2)

        logging.debug("Parallel: m_0 = " + str(m0) + ", m_1 = " + str(m1))

        return [int(m0), int(m1)]

    def solve_m_perpendicular(self, na, nbr, nc, d):

        m0, m1 = self.eng.m_range_s(float(na), float(nbr), float(nc), d, nargout=2)

        logging.debug("Parallel: m_0 = " + str(m0) + ", m_1 = " + str(m1))

        return [int(m0), int(m1)]

    def solve_both(self, na, nbr, nc, d):

        res = self.eng.resonancia(float(na), float(nbr), float(nc), float(d))

        logging.debug(res)

        # La funcion devuelve [[lista de nbi][lista de nz]]
        return res[0][1::-1]

    def solve_parallel(self, na, nbr, nc, d):

        ret = self.eng.resonancia_p(float(na), float(nbr), float(nc), float(d))

        return ret[0][1::-1]

    def solve_perpendicular(self, na, nbr, nc, d):

        # ret = self.eng.resonancia_paralelo(float(na), float(nbr), float(nc), float(d))

        # return ret[0][1::-1]
        pass

#interface = MatlabInterface()
#interface.solve_both()
