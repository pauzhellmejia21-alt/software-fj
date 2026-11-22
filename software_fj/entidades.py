"""Clase abstracta Entidad y clase Cliente."""

import re
from abc import ABC, abstractmethod

from .excepciones import DatosInvalidosError, ParametroFaltanteError

# Patrón simple de correo electrónico.
PATRON_CORREO = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"


class Entidad(ABC):
    """Entidad general del sistema: todo objeto tiene un identificador."""

    def __init__(self, identificador):
        # Un identificador ausente o vacío es un parámetro faltante.
        if identificador is None or not str(identificador).strip():
            raise ParametroFaltanteError("El identificador es obligatorio.")
        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        """Identificador de solo lectura (encapsulación)."""
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        """Cada entidad define cómo presenta su información."""

    def __str__(self):
        return self.mostrar_informacion()


class Cliente(Entidad):
    """Cliente con datos personales encapsulados y validados."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        # Se asignan mediante los setters, que validan cada dato.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        """Nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip().title()

    @property
    def correo(self):
        """Correo electrónico (se guarda en minúsculas)."""
        return self._correo

    @correo.setter
    def correo(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")
        if not isinstance(valor, str) or not re.fullmatch(PATRON_CORREO, valor.strip()):
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self):
        """Teléfono (solo dígitos)."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        numero = re.sub(r"\D", "", str(valor))  # elimina espacios, guiones, etc.
        if not 7 <= len(numero) <= 15:
            raise DatosInvalidosError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._telefono = numero

    def mostrar_informacion(self):
        return (f"Cliente {self.identificador}: {self.nombre} | "
                f"{self.correo} | Teléfono: {self.telefono}")
