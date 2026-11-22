"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de ErrorSistema, de modo que el programa puede capturar
cualquier error propio con un único `except ErrorSistema`.
"""


class ErrorSistema(Exception):
    """Excepción base de todo el sistema."""


class DatosInvalidosError(ErrorSistema):
    """Un dato no cumple las validaciones (formato, rango, tipo)."""


class ParametroFaltanteError(DatosInvalidosError):
    """Falta un parámetro obligatorio (None o vacío)."""


class ServicioNoDisponibleError(ErrorSistema):
    """El servicio no está disponible o no tiene unidades suficientes."""


class ReservaInvalidaError(ErrorSistema):
    """Una reserva no puede crearse o procesarse."""


class OperacionNoPermitidaError(ErrorSistema):
    """Se intenta una operación que el estado actual no permite."""


class CalculoInconsistenteError(ErrorSistema):
    """El cálculo de un costo produjo un resultado incoherente."""
