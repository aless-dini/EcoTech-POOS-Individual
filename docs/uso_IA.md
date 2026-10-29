# Uso de herramientas de IA en el desarrollo

EcoTech Solutions – Sistema de Gestión de Empleados · TI3021 · Criterio 2.1.5

Este proyecto individual parte del proyecto grupal. Los casos marcados como **(etapa grupal)** vienen de esa etapa; el resto corresponde al trabajo individual.

## 1. Herramienta y forma de trabajo

Se usó **Claude Code** (asistente de IA de Anthropic) integrado en VS Code. El flujo fue siempre el mismo:

1. **Pedir** un cambio concreto (por ejemplo, "implementa listar empleados por departamento").
2. **Revisar** el código propuesto contra el diagrama UML, las tablas de la base de datos y los requisitos.
3. **Probar** el programa ejecutándolo con datos válidos e inválidos.
4. **Decidir**: adoptar, modificar o descartar. Las decisiones de diseño (qué se guarda, qué reglas aplica el sistema, cómo queda el diagrama) no se delegaron a la IA.

## 2. Qué partes se apoyaron en IA

| Área | Apoyo de la IA | Trabajo y decisiones propias |
|---|---|---|
| Base inicial | — | Ya existía al empezar a usar el asistente: estructura en capas, `conexion.py`, CRUD inicial de empleados y tablas MySQL. |
| Persistencia (`BaseDAO`, DAOs, `crear_bd`) | Corrigió y completó los DAOs, propuso la clase base `BaseDAO` y las tablas para SQLite. En la etapa individual creó `errores.py` (`ErrorBaseDatos`) y unificó las tres funciones de acceso de `BaseDAO` en una sola (`_correr`). | Modelo de datos: horas con decimales, registro de tiempo ligado a proyecto, tabla intermedia empleado–proyecto. Qué mensajes ve el usuario y qué queda solo en el log. |
| Dominio | Agregó ids y referencias a las clases. En la etapa individual convirtió los atributos en `@property` con validación y creó `validaciones.py`. | Cada clase se comparó con el UML. Se decidió reemplazar `reasignar_empleado` por `eliminar_empleado` y se fijaron los límites (salario, largo de textos, teléfono). |
| Menús y validaciones | Generó los menús y las funciones de validación. En la etapa individual movió las validaciones de los menús al dominio. | Reglas: búsqueda por palabra completa, dirección como un solo texto, departamento y gerente opcionales. |
| Reglas de negocio (`servicios/registros.py`) | Implementó las reglas de horas: sin fechas futuras, no antes del inicio del proyecto, máximo 24 horas por día. | Qué reglas exige el sistema y en qué capa va cada una (ver caso 3.12). |
| Autenticación | Implementó el login sin contraseña para la primera cuenta `admin`. | Pedido propio, con el riesgo evaluado (ver caso 3.9). |
| Diagrama UML | Propuso correcciones de multiplicidad, relaciones y tipos. | Versión final en draw.io, corrigiendo errores de notación de la propuesta. |
| Errores y pruebas | Ejecutó pruebas automáticas y corrigió las caídas encontradas. | Se revisó qué cambios se mantenían y se descartaron los innecesarios. |

## 3. Casos de validación crítica

Casos reales en que el código o la propuesta de la IA no era correcta o no convenía, y cómo se resolvió.

### Etapa grupal

| # | Caso | Problema detectado | Decisión | Criterio |
|---|---|---|---|---|
| 3.1 | DAOs preliminares de proyecto, registro de tiempo y usuario | Usaban una tabla inexistente (`registro_tiempo`) y columnas inexistentes (`username`, `password`). También creaban `Proyecto(id=…)` sin que la clase recibiera `id` y cifraban la contraseña dos veces, así que nadie podía iniciar sesión. | Modificado | **Coherencia** con la base de datos y el dominio. **Seguridad**: el inicio de sesión estaba roto. |
| 3.2 | Error de sintaxis generado por la IA | Al editar `empleado.py` dejó un f-string cortado en dos líneas y el programa no arrancaba. Se detectó al ejecutar las pruebas. | Modificado | **Funcionamiento**: todo código generado se ejecuta antes de aceptarlo. |
| 3.3 | Búsqueda por nombre | La primera versión usaba `LIKE '%ana%'`, y "Ana" encontraba "Mariana". Además, `LOWER()` de SQLite no convierte letras con tilde ("PÉREZ"). Se cambió a comparar palabras completas en Python. | Modificado | **Coherencia** con el requisito definido. |
| 3.4 | Notación del diagrama UML | La IA marcó atributos con `{FK}`, que es notación del modelo relacional y no de UML. También quitó la flecha de navegabilidad del gerente, que era correcta. | Descartado | **Coherencia** con el estándar UML. |
| 3.5 | Métodos de `Empleado` | La IA eliminó `crear_proyecto`, `crear_departamento`, etc. sin consultar. Se revisó: nadie los usaba y esas responsabilidades eran de otras clases. | Adoptado tras revisión | **Diseño**: cada clase con su responsabilidad. |
| 3.6 | `import *` en los menús | Se consideró para acortar los imports, pero puede reemplazar sin avisar funciones con el mismo nombre (`eliminar_empleado` existía en dos menús). Se mantuvieron los imports explícitos. | Descartado | **Estabilidad** y legibilidad. |
| 3.7 | Motor MyISAM en MySQL | El servidor creaba las tablas con MyISAM, que ignora las claves foráneas y no tiene transacciones. Además, sin modo estricto, MySQL cortaba los textos largos sin avisar. Se agregó `ENGINE=InnoDB`, `STRICT_ALL_TABLES` y, en SQLite, `PRAGMA foreign_keys = ON`. | Modificado | **Integridad** de los datos sin depender de la configuración del servidor. |
| 3.8 | Sugerencias de otra herramienta de IA *(completar cuál)* | Proponía tres cosas: (1) atrapar el error dentro de `crear_tablas()` y seguir, con lo que el menú se abría con la base caída; (2) un `except Exception` de respaldo, que esconde errores de programación; (3) un `crear_bd` de ejemplo que habría eliminado las demás tablas. | Descartado | **Estabilidad** y coherencia con la solución existente. |

### Etapa individual

| # | Caso | Problema detectado | Decisión | Criterio |
|---|---|---|---|---|
| 3.9 | Login sin contraseña para `admin` | Se pidió poder entrar la primera vez sin contraseña y cambiarla después. La IA lo implementó con estos límites: solo ocurre si `ADMIN_PASSWORD` está vacío en el `.env`, solo esa cuenta acepta Enter vacío, el programa avisa al iniciar sesión y, una vez cambiada la contraseña, Enter vacío deja de funcionar. | Adoptado con riesgo aceptado | **Seguridad vs. usabilidad**: mientras no se cambie, cualquiera con acceso al programa entra como administrador. Fuera de un entorno de prueba hay que definir `ADMIN_PASSWORD`. |
| 3.10 | Mensajes de validación sin `f` | En `menuEmpleado.py`, `print("... {maximo} carácteres")` no tenía la `f`, y el usuario veía literalmente `{maximo}`. El error estaba en código generado en una etapa anterior y se detectó al revisar el proyecto con la pauta. | Modificado (la función se eliminó al mover la validación al dominio) | **Funcionamiento**: revisar también los textos que ve el usuario, no solo la lógica. |
| 3.11 | Atributos públicos sin protección | El profesor observó que predominaban atributos públicos. Se evaluaron dos opciones: métodos `get_x()`/`set_x()` o `@property`. Se eligió `@property`, porque los DAOs y menús siguen usando `empleado.salario` sin cambios, pero cada asignación pasa por la validación. | Adoptado | **Encapsulamiento** con el menor cambio en el resto del código. |
| 3.12 | Dónde poner la regla "no fechas futuras" | La primera idea era validarla en el constructor de `RegistroTiempo`. Pero el constructor también se usa al leer de la base, y un registro guardado antes de la regla impediría listar todos los registros. Se dejó en `servicios/registros.py`, que se aplica solo al registrar o editar. | Modificado | **Coherencia**: el dominio valida lo que siempre debe cumplirse (formato) y el servicio las reglas del proceso. |
| 3.13 | Teléfono vs. columna `INT` de MySQL | Los menús aceptaban hasta 12 dígitos, pero la columna `telefono` en MySQL es `INT` (máximo 2.147.483.647), así que un teléfono de 10 o más dígitos fallaba al guardar. Se limitó a 8–9 dígitos (formato chileno sin código de país). | Modificado | **Coherencia** entre la validación y la base de datos. Pendiente: pasar la columna a `VARCHAR` para aceptar el prefijo `+56`. |
| 3.14 | Errores técnicos mostrados al usuario | `BaseDAO` hacía `print(f"Error al {accion}: {e}")`, que mostraba el mensaje interno de SQLite o MySQL y no distinguía la causa. Ahora `BaseDAO` lanza `ErrorBaseDatos` con un mensaje claro según el tipo de error (sin conexión, dato repetido o relacionado, dato demasiado grande), el detalle va a `ecotech.log` y el menú principal es el único que lo muestra. | Modificado | **Seguridad** (no revelar la estructura interna) y **separación de capas**: la persistencia ya no imprime en pantalla. |
| 3.15 | Métodos duplicados en `UsuarioDAO` | `UsuarioDAO` reescribía `eliminar`, `listar_todos` y `buscar_por_id` con el mismo código que ya heredaba de `BaseDAO`. Se eliminaron. | Modificado | **Reutilización**: no repetir lo que da la herencia. |
| 3.16 | Datos inválidos ya guardados | Al validar en el dominio, un dato guardado que no cumpla las reglas lanzaría `ValueError` al listar y cerraría el programa. Se agregó `_convertir_filas` en `BaseDAO`, que lo transforma en un mensaje claro. | Modificado | **Estabilidad**. |
| 3.17 | Suma de horas con decimales | Al sumar horas como 8,33 + 8,33 + 7,34, la aritmética de punto flotante puede dar 24,000000000000004 y rechazar un día válido. Se redondea a 2 decimales antes de comparar con 24. | Modificado | **Funcionamiento** correcto en los bordes. |

## 4. Criterios técnicos aplicados

**Seguridad**
- Consultas SQL parametrizadas: los datos nunca se pegan en el texto SQL, lo que evita la inyección SQL.
- Contraseñas con `bcrypt` (sal aleatoria incluida en el hash y comparación segura con `bcrypt.checkpw`). La versión grupal usaba PBKDF2-SHA256.
- Credenciales en `.env`, que está en el `.gitignore`. Solo se versiona `.env.example`, sin valores.
- Claves foráneas aplicadas de verdad (InnoDB y `PRAGMA foreign_keys`) y modo estricto en MySQL.
- Los errores técnicos van al archivo `ecotech.log`, no a la pantalla.

**Encapsulamiento**
- Los atributos de las clases del dominio se guardan como `_atributo` y se exponen con `@property`. El setter valida, así que no se puede crear ni modificar un objeto con datos inválidos.
- Las listas internas (`_empleados` en `Departamento` y `Proyecto`) se entregan como tupla, para que no se modifiquen desde fuera.

**Reutilización**
- `BaseDAO` concentra la conexión, el `try/except`, el `commit`/`rollback` y el cierre en un solo método (`_correr`). Los DAOs heredan `eliminar`, `buscar_por_id` y `listar_todos`.
- `dominio/validaciones.py` reúne las reglas comunes (largo de textos, fechas, ids) que usan todas las clases del dominio.
- `entradas.pedir_dato` recibe cualquier validador del dominio, así que los menús no repiten bucles de validación.

**Coherencia**
- Los límites de largo de las clases coinciden con las columnas `VARCHAR(100)` de MySQL.
- Cada cambio se comparó contra el diagrama de clases, las tablas y los requisitos.

## 5. Cómo se validó el código

- **(Etapa grupal)** Ejecución manual de cada opción de los cinco menús. Pruebas con MySQL 8.4 real en una base de prueba separada: 19 pruebas específicas y más de 35.000 acciones al azar en SQLite y MySQL, que encontraron 6 formas de hacer caer el programa, todas corregidas.
- **(Etapa individual)** Script de pruebas sobre una base SQLite temporal, sin tocar la base real:
  - Encapsulamiento: se rechazan salario fuera de rango, nombre de más de 100 caracteres, teléfono de 12 dígitos, correo y fecha inválidos, y horas `nan`.
  - Reglas de negocio: se rechazan fechas futuras, fechas anteriores al inicio del proyecto, superar 24 horas en un día (también al editar), registrar sin estar asignado al proyecto y mover el inicio de un proyecto después de sus horas registradas.
  - Errores de base de datos: correo duplicado, id gigante, dato inválido guardado y base MySQL no disponible al iniciar. En todos los casos aparece un mensaje claro y el detalle queda en el log.
  - Recorrido del programa real con entradas escritas por script: login sin contraseña, creación de departamento (incluido el nombre repetido), proyecto y empleado con datos inválidos antes de los válidos.

## 6. Para la defensa

- Contar dos casos de la sección 3 con palabras propias: qué propuso la IA, qué estaba mal y por qué se decidió así.
- Explicar sin leer: `@property` en el dominio, `BaseDAO` y la herencia, `ErrorBaseDatos` y dónde se captura, y el cifrado con `bcrypt`.

**Aporte propio** *(completar)*: …
