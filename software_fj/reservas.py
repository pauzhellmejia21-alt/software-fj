"""Clase Reserva: integra cliente, servicio, duración y estado."""

from .entidades import Cliente, Entidad
from .excepciones import (CalculoInconsistenteError, DatosInvalidosError,
                          OperacionNoPermitidaError, ReservaInvalidaError,
                          ServicioNoDisponibleError)
from .registro import logger
from .servicios import Servicio


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    ESTADOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")

    def __init__(self, identificador, cliente, servicio, duracion, cantidad=1):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva debe estar asociada a un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva debe estar asociada a un servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError("No se puede reservar un servicio no disponible.")
        # Polimorfismo: cada servicio valida a su manera, sin if por tipo.
        servicio.validar_parametros(duracion, cantidad)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.cantidad = cantidad
        self.estado = "Pendiente"
        self.costo = 0.0
        logger.info("Reserva %s creada para el cliente %s.", self.identificador, cliente.nombre)

    def confirmar(self):
        """Pendiente -> Confirmada."""
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
        self.estado = "Confirmada"
        logger.info("Reserva %s confirmada.", self.identificador)
        return "Reserva confirmada correctamente."

    def cancelar(self):
        """Cancela una reserva que no esté cancelada ni procesada."""
        if self.estado in ("Cancelada", "Procesada"):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self.estado}.")
        self.estado = "Cancelada"
        logger.info("Reserva %s cancelada.", self.identificador)
        return "Reserva cancelada correctamente."

    def procesar(self, impuesto=0.19, descuento=0):
        """Confirmada -> Procesada, calculando el costo final."""
        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError("La reserva debe estar confirmada antes de procesarse.")
        try:
            costo = self.servicio.calcular_costo_total(
                self.duracion, self.cantidad, impuesto, descuento)
        except (DatosInvalidosError, ServicioNoDisponibleError,
                CalculoInconsistenteError) as error:
            logger.exception("Error al procesar la reserva %s.", self.identificador)
            # Encadenamiento: el error original queda como causa.
            raise ReservaInvalidaError("No fue posible procesar la reserva.") from error
        else:
            # Solo si el cálculo fue exitoso se consumen recursos y cambia el estado.
            self.servicio.consumir_recursos(self.cantidad)
            self.costo = costo
            self.estado = "Procesada"
            logger.info("Reserva %s procesada. Costo: %.2f", self.identificador, costo)
            return costo
        finally:
            logger.info("Finalizó el intento de procesamiento de la reserva %s.", self.identificador)

    def mostrar_informacion(self):
        return (f"Reserva {self.identificador} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | "
                f"Estado: {self.estado} | Costo: ${self.costo:,.2f}")
