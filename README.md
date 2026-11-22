# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto del curso Programación (213023), UNAD – Fase 4, Anexo 3.
Sin bases de datos: todo se maneja con objetos y listas; el único archivo que se escribe es `software_fj.log`.

## Estructura

```
Software_FJ_Proyecto/
├── main.py                  # Punto de entrada (menú interactivo)
├── README.md
└── software_fj/
    ├── excepciones.py       # Excepciones personalizadas
    ├── registro.py          # Configuración del log
    ├── entidades.py         # Entidad (abstracta) y Cliente
    ├── servicios.py         # Servicio (abstracta), ReservaSala, AlquilerEquipo, AsesoriaEspecializada
    ├── reservas.py          # Reserva (confirmar, cancelar, procesar)
    ├── sistema.py           # SistemaSoftwareFJ: listas internas y búsquedas
    ├── pruebas.py           # 18 operaciones de demostración
    └── menu.py              # Menú interactivo
```

## Ejecución

Requiere Python 3.9 o superior.

```bash
python main.py        # En Windows también: py main.py
```

La opción **10** del menú ejecuta las 18 operaciones automáticas (válidas e inválidas). Los eventos y errores quedan en `software_fj.log`.

## Requisitos del Anexo 3 y dónde están

| Requisito | Dónde |
|---|---|
| Clase abstracta general | `Entidad` (`entidades.py`) |
| Cliente con validaciones y encapsulación | `Cliente` (`entidades.py`) |
| Servicio abstracto + 3 especializados | `servicios.py` |
| Polimorfismo (métodos sobrescritos) | `validar_parametros`, `calcular_subtotal`, `describir` |
| Reserva (cliente, servicio, duración, estado) | `reservas.py` |
| Métodos sobrecargados | `calcular_costo`, `calcular_costo_con_impuesto`, `calcular_costo_con_descuento`, `calcular_costo_total` |
| Excepciones personalizadas | `excepciones.py` (7 clases) |
| try/except/else/finally | `pruebas.py` (`ejecutar`) y `Reserva.procesar` |
| Encadenamiento de excepciones | `raise ... from error` en `Servicio.__init__` y `Reserva.procesar` |
| Archivo de logs | `software_fj.log` |
| 10 o más operaciones | 18 en `pruebas.py` |

**Nota sobre sobrecarga:** Python no sobrecarga métodos por tipo o cantidad de parámetros como Java o C++. Aquí se ofrecen variantes con distinto nombre y parámetros opcionales para el mismo cálculo.
