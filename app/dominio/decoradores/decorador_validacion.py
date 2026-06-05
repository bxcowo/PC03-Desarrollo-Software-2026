from datetime import datetime, UTC

from app.dominio.firma_entity import FirmaEntity
from app.dominio.iniciativa_entity import IniciativaEntity
from app.dominio.enums.estado_iniciativa import EstadoIniciativaEnum
from app.dominio.interfaces.validador_firma import IValidadorFirma


class ValidadorBase(IValidadorFirma):
    """
        Verifica que la firma tenga ciudadano e iniciativa asociados.
    """

    def validar(self, firma: FirmaEntity, iniciativa: IniciativaEntity) -> bool:
        if not firma.ciudadano_id:
            raise ValueError("La firma debe tener un ciudadano asociado.")
        if not firma.iniciativa_id:
            raise ValueError("La firma debe tener una iniciativa asociada.")
        if not iniciativa.id == firma.iniciativa_id:
            raise ValueError("La firma y la iniciativa no están asociados")
        return True


class DecoradorValidacionFirma(IValidadorFirma):
    """
        Añade verificación de estado ACTIVA y ventana de 90 días sobre el validador envuelto.
    """

    def __init__(self, validador: IValidadorFirma) -> None:
        self._validador = validador

    def validar(self, firma: FirmaEntity, iniciativa: IniciativaEntity) -> bool:
        self._validador.validar(firma, iniciativa)

        if iniciativa.estado != EstadoIniciativaEnum.ACTIVA:
            raise ValueError(
                f"La iniciativa '{iniciativa.id}' no está ACTIVA "
                f"(estado actual: {iniciativa.estado.value})."
            )

        if datetime.now(UTC) > iniciativa.fecha_limite.replace(tzinfo=UTC):
            raise ValueError(
                f"El plazo de firma para la iniciativa '{iniciativa.id}' "
                f"venció el {iniciativa.fecha_limite.date()}."
            )

        return True
