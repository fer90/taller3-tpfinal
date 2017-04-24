# -*- coding: utf-8 -*-

import matlab.engine

import logging

"""
Esta clase es la encargada de interfacear con el script en matlab
"""

class MatlabInterface(object):

    class __MatlabInterface:

        def __init__(self):

            #super(MatlabInterface.__MatlabInterface, self).__init__()

            try:
                self.future = matlab.engine.connect_matlab(async=True)
            
                self.eng = self.future.result()
            except Exception:

                logging.warning("No se ha podido conectar a una sesion de matlab existente. Creando una...");

                try:
                    # No se ha podido conectar a una sesion activa -> creo una
                    self.eng = matlab.engine.start_matlab('-nodesktop -nojvm -nosplash')

                except Exception as e:

                    logging.error("No se ha podido crear una sesión de Matlab. Por favor,"
                        + " corroborar que Matlab esté instalado correctamente. "
                        + "Si el problema persiste, contactar al administrador")
                    raise e

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

            logging.debug("Na: " + str(na) + ". Nbr: " + str(nbr) + ". Nc: " + str(nc) + ". D: " + str(d) + ". m_from: " + str(m_from) + ". m_to: " + str(m_to))

            ret = self.eng.resonancia_p(float(na), float(nbr), float(nc), float(d), float(m_from), float(m_to))

            logging.debug("Resonancia paralelo: " + str(ret))

            return ret[0][1::-1]

        def solve_perpendicular(self, na, nbr, nc, d, m_from, m_to):

            ret = self.eng.resonancia_s(float(na), float(nbr), float(nc), float(d), float(m_from), float(m_to))

            logging.debug("Resonancia perpendicular: " + str(ret))

            return ret[0][1::-1]

        def solve_field_parallel(self, na, nbr, nbi, nc, nz, d):
            
            h_2_4, h_5_3 = self.eng.field_p(float(na), float(nbr), nbi, float(nc), nz, float(d), nargout=2)

            logging.debug("Campos paralelos H2/H4 = " + str(h_2_4) + ". H5/H3 = " + str(h_5_3))

            return [h_2_4, h_5_3]

        def solve_field_perpendicular(self, na, nbr, nbi, nc, nz, d):
            
            e_2_4, e_5_3 = self.eng.field_s(float(na), float(nbr), nbi, float(nc), nz, float(d), nargout=2)

            logging.debug("Campos paralelos E2/E4 = " + str(e_2_4) + ". E5/E3 = " + str(e_5_3))

            return [e_2_4, e_5_3]

        def stop_engine(self):

            self.eng.quit()

    # Singleton
    instance = None

    def __new__(cls):

        if not MatlabInterface.instance:

            MatlabInterface.instance = MatlabInterface.__MatlabInterface()

        return MatlabInterface.instance

#interface = MatlabInterface()
#interface.solve_field_parallel(1, 1.2, 0.98, 1, 0.5, 2)
#interface.solve_field_perpendicular(1, 1.2, 0.98, 1, 0.5, 2)
