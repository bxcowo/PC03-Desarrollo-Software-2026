import re

_RE_DNI = re.compile(r"^\d{8}$")
_DNI_MIN = 10_000_000
_DNI_MAX = 99_999_999


class FachadaVerificacionIdentidad:
    """
        Orquesta las validaciones de identidad del ciudadano tras un único punto de entrada.
    """

    def validar_ciudadano(
        self,
        dni: str,
    ) -> bool:
        self._validar_formato_dni(dni)
        self._validar_rango_dni(dni)
        self._validar_estado_padron(dni)
        return True

    def _validar_formato_dni(self, dni: str) -> None:
        if not _RE_DNI.match(dni):
            raise ValueError(f"DNI '{dni}' inválido: debe contener exactamente 8 dígitos.")

    def _validar_rango_dni(self, dni: str) -> None:
        # RENIEC no emite DNIs fuera del rango conocido de 8 dígitos
        numero = int(dni)
        if not (_DNI_MIN <= numero <= _DNI_MAX):
            raise ValueError(f"DNI '{dni}' fuera del rango de números emitidos por RENIEC.")

    def _validar_estado_padron(self, dni: str) -> None:
        # DNIs que empiezan en 0X son series anuladas por RENIEC
        if dni.startswith("0"):
            raise ValueError(f"DNI '{dni}' pertenece a una serie anulada en el padrón electoral.")
