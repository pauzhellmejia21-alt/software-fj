"""Configuración del archivo de logs (software_fj.log).

El log es el único uso de archivos del sistema: guarda eventos y errores.
"""

import logging
from pathlib import Path

# El log se guarda junto a main.py, sin importar desde dónde se ejecute.
RUTA_LOG = Path(__file__).resolve().parent.parent / "software_fj.log"

logging.basicConfig(
    filename=RUTA_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

# Logger compartido por todos los módulos.
logger = logging.getLogger("SoftwareFJ")
