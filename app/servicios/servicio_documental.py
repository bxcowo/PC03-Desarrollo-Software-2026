from sqlalchemy.orm import Session
from app.dominio.propuesta import Propuesta
from app.dominio.seccion import Seccion
from app.dominio.articulo import Articulo
from app.infraestructura.repositorios.repositorio_propuestas import RepositorioPropuestas
from app.infraestructura.adaptadores import AdaptadorPDF, AdaptadorDOCX

class ServicioDocumental:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = RepositorioPropuestas(db)

    def crear_propuesta_inicial(self, iniciativa_id: int, ciudadano_id: int, titulo: str) -> dict:
        self._validar_permisos(iniciativa_id, ciudadano_id)
        
        propuesta = Propuesta(iniciativa_id, titulo)
        self._repo.guardar(propuesta)
        self._db.commit()
        return propuesta.exportar_a_json()

    def agregar_seccion(self, iniciativa_id: int, ciudadano_id: int, titulo_seccion: str) -> dict:
        self._validar_permisos(iniciativa_id, ciudadano_id)
        
        propuesta = self._repo.obtener_por_iniciativa(iniciativa_id)
        if not propuesta:
            raise ValueError(f"No existe propuesta para la iniciativa {iniciativa_id}")
        
        nueva_seccion = Seccion(titulo_seccion)
        propuesta.agregar(nueva_seccion)
        
        self._repo.guardar(propuesta)
        self._db.commit()
        return propuesta.exportar_a_json()

    def agregar_articulo_a_seccion(self, iniciativa_id: int, ciudadano_id: int, titulo_seccion: str, titulo_articulo: str, contenido: str) -> dict:
        self._validar_permisos(iniciativa_id, ciudadano_id)
        
        propuesta = self._repo.obtener_por_iniciativa(iniciativa_id)
        if not propuesta:
            raise ValueError(f"No existe propuesta para la iniciativa {iniciativa_id}")
        
        seccion_objetivo = self._buscar_seccion(propuesta.hijos, titulo_seccion)
        
        if not seccion_objetivo:
            raise ValueError(f"No se encontró la sección '{titulo_seccion}'")
            
        nuevo_articulo = Articulo(titulo_articulo, contenido)
        seccion_objetivo.agregar(nuevo_articulo)
        
        self._repo.guardar(propuesta)
        self._db.commit()
        return propuesta.exportar_a_json()

    def adjuntar_recurso_externo(self, iniciativa_id: int, ciudadano_id: int, nombre_archivo: str, contenido_binario: bytes) -> dict:
        self._validar_permisos(iniciativa_id, ciudadano_id)
        
        propuesta = self._repo.obtener_por_iniciativa(iniciativa_id)
        if not propuesta:
            raise ValueError(f"No existe propuesta para la iniciativa {iniciativa_id}")

        if nombre_archivo.lower().endswith(".pdf"):
            adaptador = AdaptadorPDF(contenido_binario, nombre_archivo)
        elif nombre_archivo.lower().endswith(".docx"):
            adaptador = AdaptadorDOCX(contenido_binario, nombre_archivo)
        else:
            raise ValueError("Formato de archivo no soportado. Use PDF o DOCX.")
            
        info = adaptador.extraer_informacion()
        
        # Verificar si existe la sección "Anexos", si no, crearla
        seccion_anexos = self._buscar_seccion(propuesta.hijos, "Anexos")
        if not seccion_anexos:
            seccion_anexos = Seccion("Anexos")
            propuesta.agregar(seccion_anexos)
            self._repo.guardar(propuesta)
        
        nuevo_articulo = Articulo(f"Anexo: {info.nombre_original}", f"Contenido Extraído: {info.texto}\nFormato: {info.formato}\nTamaño: {info.tamano_bytes} bytes")
        seccion_anexos.agregar(nuevo_articulo)
        
        self._repo.guardar(propuesta)
        self._db.commit()
        return propuesta.exportar_a_json()

    def _validar_permisos(self, iniciativa_id: int, ciudadano_id: int):
        if not self._repo.verificar_autoria(iniciativa_id, ciudadano_id):
            raise PermissionError("No tiene permisos para modificar esta iniciativa.")

    def _buscar_seccion(self, componentes, titulo):
        for c in componentes:
            if isinstance(c, Seccion) and c.titulo == titulo:
                return c
            if isinstance(c, Seccion):
                encontrado = self._buscar_seccion(c.hijos, titulo)
                if encontrado:
                    return encontrado
        return None
