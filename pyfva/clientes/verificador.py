'''
Created on 20 jul. 2017

@author: luis
'''
from pyfva.soap.verificador import ValideElServicio, VerificadorSoapServiceStub,\
    ExisteUnaSolicitudDeFirmaCompleta
import warnings
from pyfva.soap import settings


class ClienteVerificador(object):
    """Verifica si una firma ha sido completada

    .. note:: 
        Los parámetros negocio y entidad de momento no son requeridos, pero puede que en un futuro cercano
        lo sean, por lo que se recomienda suministrarlos.

    :param negocio: número de identificación del negocio (provisto por el BCCR)
    :param entidad: número de identificación de la entidad (provisto por el BCCR)
    """

    DEFAULT_ERROR = {
        'codigo_error': 2,
        'existe_firma': False,
        'fue_exitosa': False

    }

    def __init__(self,
                 negocio=settings.DEFAULT_BUSSINESS,
                 entidad=settings.DEFAULT_ENTITY):
        self.negocio = negocio
        self.entidad = entidad

    def existe_solicitud_de_firma_completa(self, identificacion):
        """Verifica si una solicitud de firma ha sida completada por el usuario en el sistema del BCCR

        :param identificacion: número de identificación de la persona

        Retorna una diccionario con los siguientes elementos, en caso de error retorna
        **DEFAULT_ERROR**.

        :returns:   
            **codigo_error:** Número con el código de error 1 es éxito

            **exitosa:** True si fue exitosa, False si no lo fue

            **existe_firma:** Retorna True si hay un proceso de firma activo o False si no.

        """
        try:
            dev = self._existe_solicitud_de_firma_completa(identificacion)
        except:
            dev = self.DEFAULT_ERROR
        return dev

    def validar_servicio(self):
        """
        Valida si el servicio está disponible.  

        :returns: True si lo está o False si ocurrió algún error contactando al BCCR o el servicio no está disponible
        """
        return self._validar_servicio()

    # Private methods
    def _existe_solicitud_de_firma_completa(self, identificacion):
        stub = VerificadorSoapServiceStub()
        options = ExisteUnaSolicitudDeFirmaCompleta()
        options.laCedulaDelUsuario = identificacion
        status = stub.ExisteUnaSolicitudDeFirmaCompleta(options)
        result = status.soap_body.ExisteUnaSolicitudDeFirmaCompletaResult
        return self._extract_solicitud_firma_completa(result)

    def _extract_solicitud_firma_completa(self, result):
        dev = {}
        dev.update(self.DEFAULT_ERROR)
        dev['codigo_error'] = result.CodigoDeError
        dev['existe_firma'] = result.FueExitosa
        dev['fue_exitosa'] = result.ExisteUnaFirmaCompleta
        return dev

    def _validar_servicio(self):
        stub = VerificadorSoapServiceStub()
        option = ValideElServicio()
        try:
            status = stub.ValideElServicio(option)
            dev = status.soap_body.ValideElServicioResult
        except Exception as e:
            warnings.warn("servicio de verificación fallando %s" %
                          (e,), RuntimeWarning)

            dev = False
        return dev