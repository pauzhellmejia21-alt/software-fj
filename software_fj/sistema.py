"""Sistema central: administra las listas internas (sin base de datos)."""

from .entidades import Cliente
from .excepciones import DatosInvalidosError, ReservaInvalidaError
from .registro import logger
from .reservas import Reserva
from .servicios import Servicio


class SistemaSoftwareFJ:
    """Guarda clientes, servicios y reservas en listas en memoria."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El objeto que se intenta registrar no es un cliente.")
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise DatosInvalidosError("Ya existe un cliente con ese identificador.")
        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.nombre)
        return cliente

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El objeto que se intenta registrar no es un servicio.")
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise DatosInvalidosError("Ya existe un servicio con ese identificador.")
        self.servicios.append(servicio)
        logger.info("Servicio registrado: %s", servicio.nombre)
        return servicio

    # Busca un cliente por su identificador; si no lo encuentra, lanza un error.
    def buscar_cliente(self, identificador):
        cliente = next((c for c in self.clientes if c.identificador == str(identificador)), None)
        if cliente is None:
            raise ReservaInvalidaError("No se encontró el cliente indicado.")
        return cliente

    def buscar_servicio(self, identificador):
        servicio = next((s for s in self.servicios if s.identificador == str(identificador)), None)
        if servicio is None:
            raise ReservaInvalidaError("No se encontró el servicio indicado.")
        return servicio

    def buscar_reserva(self, identificador):
        reserva = next((r for r in self.reservas if r.identificador == str(identificador)), None)
        if reserva is None:
            raise ReservaInvalidaError("No se encontró la reserva.")
        return reserva

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion, cantidad=1):
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)
        # Se revisa el ID duplicado ANTES de crear la reserva.
        if any(r.identificador == str(identificador).strip() for r in self.reservas):
            raise ReservaInvalidaError("Ya existe una reserva con ese identificador.")
        reserva = Reserva(identificador, cliente, servicio, duracion, cantidad)
        self.reservas.append(reserva)
        return reserva

    def listar_reservas(self):
        return [reserva.mostrar_informacion() for reserva in self.reservas]
