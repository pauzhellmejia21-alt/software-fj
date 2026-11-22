"""Simulación de 18 operaciones completas (válidas e inválidas)."""

from .entidades import Cliente
from .excepciones import ErrorSistema
from .registro import logger
from .servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from .sistema import SistemaSoftwareFJ


def ejecutar_pruebas():
    """Ejecuta las operaciones de demostración; ningún error detiene el programa."""
    sistema = SistemaSoftwareFJ()
    print("=" * 72)
    print(" SOFTWARE FJ - SISTEMA INTEGRAL DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 72)

    def ejecutar(numero, descripcion, accion):
        """Corre una operación con try/except/else/finally."""
        print(f"\nOPERACIÓN {numero}: {descripcion}")
        try:
            resultado = accion()
            print("RESULTADO:", resultado if resultado is not None else "Operación realizada.")
            logger.info("Operación %s exitosa: %s", numero, descripcion)
        except ErrorSistema as error:  # errores propios, ya previstos
            print("ERROR CONTROLADO:", error)
            logger.error("Operación %s fallida: %s", numero, error)
        except Exception as error:  # cualquier otro error imprevisto
            print("ERROR INESPERADO CONTROLADO:", error)
            logger.exception("Error inesperado en operación %s.", numero)
        else:
            print("ESTADO: La operación terminó sin excepciones.")
        finally:
            print("FIN: La aplicación continúa funcionando.")

    # --- Clientes ---
    ejecutar(1, "Registrar un cliente válido", lambda: sistema.registrar_cliente(
        Cliente("C001", "Laura Gómez", "laura@gmail.com", "3001234567")).mostrar_informacion())
    ejecutar(2, "Registrar un segundo cliente válido", lambda: sistema.registrar_cliente(
        Cliente("C002", "Carlos Pérez", "carlos@gmail.com", "3107654321")).mostrar_informacion())
    ejecutar(3, "Cliente con correo inválido", lambda: sistema.registrar_cliente(
        Cliente("C003", "Ana Torres", "correo-no-valido", "3005556677")))
    ejecutar(4, "Cliente con parámetro faltante (nombre None)", lambda: sistema.registrar_cliente(
        Cliente("C004", None, "ana@gmail.com", "3005556677")))

    # --- Servicios ---
    ejecutar(5, "Registrar servicio de sala", lambda: sistema.registrar_servicio(
        ReservaSala("S001", "Sala de reuniones", 50000, 12)).describir())
    ejecutar(6, "Registrar alquiler de equipos", lambda: sistema.registrar_servicio(
        AlquilerEquipo("S002", "Computador portátil", 35000, 5)).describir())
    ejecutar(7, "Registrar asesoría especializada", lambda: sistema.registrar_servicio(
        AsesoriaEspecializada("S003", "Asesoría tecnológica", 80000, "programación")).describir())
    ejecutar(8, "Servicio con tarifa negativa", lambda: sistema.registrar_servicio(
        ReservaSala("S004", "Sala inválida", -1000, 10)))

    # --- Reservas ---
    ejecutar(9, "Crear reserva de sala R001",
             lambda: sistema.crear_reserva("R001", "C001", "S001", 2).mostrar_informacion())
    ejecutar(10, "Confirmar reserva R001", lambda: sistema.buscar_reserva("R001").confirmar())
    ejecutar(11, "Procesar reserva R001",
             lambda: f"Costo total: ${sistema.buscar_reserva('R001').procesar():,.2f}")
    ejecutar(12, "Cancelar una reserva ya procesada",
             lambda: sistema.buscar_reserva("R001").cancelar())
    ejecutar(13, "Reserva con cliente inexistente",
             lambda: sistema.crear_reserva("R002", "C999", "S001", 1))
    ejecutar(14, "Reserva con duración inválida (0 horas)",
             lambda: sistema.crear_reserva("R003", "C002", "S001", 0))

    def reserva_equipo():
        reserva = sistema.crear_reserva("R004", "C002", "S002", 3, 2)
        reserva.confirmar()
        costo = reserva.procesar(descuento=0.10)
        return f"{reserva.mostrar_informacion()} | Total: ${costo:,.2f}"
    ejecutar(15, "Crear y procesar alquiler de dos computadores", reserva_equipo)

    def cancelar_pendiente():
        return sistema.crear_reserva("R005", "C001", "S003", 1).cancelar()
    ejecutar(16, "Crear y cancelar una reserva pendiente", cancelar_pendiente)

    def procesar_sin_confirmar():
        return sistema.crear_reserva("R006", "C001", "S003", 1).procesar()
    ejecutar(17, "Procesar una reserva sin confirmar", procesar_sin_confirmar)

    def descuento_invalido():
        reserva = sistema.crear_reserva("R007", "C001", "S003", 2)
        reserva.confirmar()
        return reserva.procesar(descuento=1.5)  # cálculo inconsistente
    ejecutar(18, "Procesar con descuento inconsistente (150%)", descuento_invalido)

    print("\n" + "=" * 72)
    print("RESUMEN FINAL DE RESERVAS")
    print("=" * 72)
    for detalle in sistema.listar_reservas():
        print(detalle)
    print("\nTotal de clientes registrados:", len(sistema.clientes))
    print("Total de servicios registrados:", len(sistema.servicios))
    print("Total de reservas creadas:", len(sistema.reservas))
    print("\nLos eventos y errores quedaron registrados en: software_fj.log")
    print("El sistema finalizó la demostración sin detenerse por los errores.")
