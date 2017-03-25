# -*- coding: utf-8 -*-

import matlab.engine

import logging

"""
Esta clase es la encargada de interfacear con el script en matlab
"""

class MatlabInterface(object):

    class __MatlabInterface:

        def __init__(self):

            super(MatlabInterface.__MatlabInterface, self).__init__()

            try:
                self.future = matlab.engine.connect_matlab(async=True)
            
                self.eng = self.future.result()
            except Exception:

                logging.warning("No se ha podido conectar a una sesion de matlab existente. Creando una...");
                # No se ha podido conectar a una sesion activa -> creo una
                self.eng = matlab.engine.start_matlab('-nodesktop -nojvm -nosplash')

        def solve_m_parallel(self, na, nbr, nc, d):

            # NOTE: 'nargout' hace referencia a la cantidad de outputs que esperamos
            m0, m1 = self.eng.m_range_p(float(na), float(nbr), float(nc), d, nargout=2)

            logging.debug("M Parallel: m_0 = " + str(m0) + ", m_1 = " + str(m1))

            return [int(m0), int(m1)]

        def solve_m_perpendicular(self, na, nbr, nc, d):

            m0, m1 = self.eng.m_range_s(float(na), float(nbr), float(nc), d, nargout=2)

            logging.debug("M Perpendicular: m_0 = " + str(m0) + ", m_1 = " + str(m1))

            return [int(m0), int(m1)]

        """
        Metodo Deprecado: Se utilizaba solo a fines de testing
        """
        def solve_both(self, na, nbr, nc, d):

            res = self.eng.resonancia(float(na), float(nbr), float(nc), float(d))

            logging.debug(res)

            # La funcion devuelve [[lista de nbi][lista de nz]]
            return res[0][1::-1]

        def solve_parallel(self, na, nbr, nc, d, m_from, m_to):

            ret = self.eng.resonancia_p(float(na), float(nbr), float(nc), float(d), float(m_from), float(m_to))

            logging.debug("Resonancia paralelo: " + str(ret))

            return ret[0][1::-1]

        def solve_perpendicular(self, na, nbr, nc, d, m_from, m_to):

            ret = self.eng.resonancia_s(float(na), float(nbr), float(nc), float(d), float(m_from), float(m_to))

            logging.debug("Resonancia perpendicular: " + str(ret))

            return ret[0][1::-1]

        def stop_engine(self):

            self.eng.quit()

    # Singleton
    instance = None

    def __new__(cls):

        if not MatlabInterface.instance:

            MatlabInterface.instance = MatlabInterface.__MatlabInterface()

        return MatlabInterface.instance

#interface = MatlabInterface()
#interface.solve_both()
