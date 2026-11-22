"""Clase abstracta Servicio y los tres servicios especializados.

Polimorfismo: cada subclase sobrescribe validar_parametros, calcular_subtotal
y describir. El cálculo del costo final (con impuestos y descuentos) vive en
la clase base y se ofrece en varias variantes (sobrecarga).
"""

import math
from abc import abstractmethod

from .entidades import Entidad
from .excepciones import (CalculoInconsistenteError, DatosInvalidosError,
                          ParametroFaltanteError, ServicioNoDisponibleError)
from .registro import logger

IVA = 0.19  # impuesto por defecto


class Servicio(Entidad):
    """Servicio abstracto ofrecido por Software FJ."""

    # Indica si la reserva necesita una cantidad (solo alquiler de equipos).
    requiere_cantidad = False

    def __init__(self, identificador, nombre, tarifa_base):
        super().__init__(identificador)
        if nombre is None or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        try:
            tarifa = float(tarifa_base)
        except (TypeError, ValueError) as error:
            # Encadenamiento: se conserva el error original como causa.
            raise DatosInvalidosError("La tarifa debe ser numérica.") from error
        if tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero.")
        self._nombre = str(nombre).strip()
        self._tarifa_base = tarifa
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        """Activa o desactiva el servicio."""
        if not isinstance(estado, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadera o falsa.")
        self._disponible = estado
        logger.info("Disponibilidad del servicio %s: %s", self.identificador, estado)

    # ---- Métodos que cada servicio sobrescribe (polimorfismo) ----------
    @abstractmethod
    def validar_parametros(self, duracion, cantidad=1):
        """Valida duración y cantidad según las reglas del servicio."""

    @abstractmethod
    def calcular_subtotal(self, duracion, cantidad=1):
        """Costo antes de impuestos y descuentos."""

    @abstractmethod
    def describir(self):
        """Texto descriptivo del servicio."""

    def consumir_recursos(self, cantidad):
        """Gancho que se ejecuta al procesar una reserva (por defecto no hace nada)."""

    # ---- Cálculo de costos: variantes sobrecargadas --------------------
    def calcular_costo_total(self, duracion, cantidad=1, impuesto=IVA, descuento=0):
        """Variante completa: valida, aplica impuesto y descuento, y revisa coherencia."""
        self.validar_parametros(duracion, cantidad)
        if not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError("El impuesto debe estar entre 0 y 1.")
        if not 0 <= descuento < 1:
            raise CalculoInconsistenteError("El descuento debe estar entre 0 y menos de 1.")
        total = self.calcular_subtotal(duracion, cantidad) * (1 + impuesto) * (1 - descuento)
        if not math.isfinite(total) or total <= 0:
            raise CalculoInconsistenteError("El costo calculado no es un valor positivo válido.")
        return total

    def calcular_costo(self, duracion, cantidad=1):
        """Variante 1: solo duración (y cantidad). Usa el IVA por defecto."""
        return self.calcular_costo_total(duracion, cantidad)

    def calcular_costo_con_impuesto(self, duracion, impuesto, cantidad=1):
        """Variante 2: impuesto personalizado, sin descuento."""
        return self.calcular_costo_total(duracion, cantidad, impuesto=impuesto)

    def calcular_costo_con_descuento(self, duracion, descuento, cantidad=1):
        """Variante 3: descuento con el IVA por defecto."""
        return self.calcular_costo_total(duracion, cantidad, descuento=descuento)

    def mostrar_informacion(self):
        return f"{self.identificador} - {self.describir()}"


class ReservaSala(Servicio):
    """Reserva de una sala por horas."""

    def __init__(self, identificador, nombre, tarifa_base, capacidad):
        super().__init__(identificador, nombre, tarifa_base)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion, cantidad=1):
        if not isinstance(duracion, (int, float)) or not 0 < duracion <= 12:
            raise DatosInvalidosError("La duración de la sala debe ser mayor a 0 y máximo 12 horas.")

    def calcular_subtotal(self, duracion, cantidad=1):
        return self.tarifa_base * duracion  # tarifa por hora

    def describir(self):
        return f"Reserva de sala '{self.nombre}', capacidad para {self.capacidad} personas."


class AlquilerEquipo(Servicio):
    """Alquiler de equipos por días y por unidades."""

    requiere_cantidad = True

    def __init__(self, identificador, nombre, tarifa_base, unidades_disponibles):
        super().__init__(identificador, nombre, tarifa_base)
        if not isinstance(unidades_disponibles, int) or unidades_disponibles < 0:
            raise DatosInvalidosError("Las unidades disponibles deben ser un entero no negativo.")
        self.unidades_disponibles = unidades_disponibles

    def validar_parametros(self, duracion, cantidad=1):
        if not isinstance(duracion, (int, float)) or not 0 < duracion <= 30:
            raise DatosInvalidosError("La duración del alquiler debe ser mayor a 0 y máximo 30 días.")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser un entero positivo.")
        if cantidad > self.unidades_disponibles:
            raise ServicioNoDisponibleError("No hay suficientes unidades de equipo disponibles.")

    def calcular_subtotal(self, duracion, cantidad=1):
        return self.tarifa_base * duracion * cantidad  # tarifa por día y unidad

    def consumir_recursos(self, cantidad):
        """Descuenta del inventario las unidades alquiladas."""
        self.unidades_disponibles -= cantidad

    def describir(self):
        return f"Alquiler de equipo '{self.nombre}'. Unidades disponibles: {self.unidades_disponibles}."


class AsesoriaEspecializada(Servicio):
    """Asesoría por horas en una especialidad."""

    def __init__(self, identificador, nombre, tarifa_base, especialidad):
        super().__init__(identificador, nombre, tarifa_base)
        if especialidad is None or not str(especialidad).strip():
            raise ParametroFaltanteError("La especialidad de la asesoría es obligatoria.")
        self.especialidad = str(especialidad).strip()

    def validar_parametros(self, duracion, cantidad=1):
        if not isinstance(duracion, (int, float)) or not 0 < duracion <= 8:
            raise DatosInvalidosError("La asesoría debe durar más de 0 y máximo 8 horas.")

    def calcular_subtotal(self, duracion, cantidad=1):
        return self.tarifa_base * duracion  # tarifa por hora

    def describir(self):
        return f"Asesoría de '{self.nombre}' en {self.especialidad}."
