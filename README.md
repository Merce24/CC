# Recomendador de Juegos de Mesa --- Aplicación Cloud-Native

## 1. Descripción del dominio

### 1.1. Contexto y problema de negocio

El proyecto consiste en una aplicación web *cloud-native* orientada a la
**recomendación de juegos de mesa y gestión de ludotecas personales o de
asociaciones**.

El mercado de los juegos de mesa dispone de catálogos muy amplios y
heterogéneos. Elegir un juego adecuado no depende únicamente de su
valoración general, sino de factores como el número de jugadores, la
duración disponible, la complejidad deseada, las mecánicas, las
categorías o temáticas y el tipo de experiencia buscada. Esto dificulta
que un usuario encuentre rápidamente un juego apropiado para una
situación concreta.

Además, los jugadores y asociaciones pueden disponer de ludotecas con
decenas o cientos de títulos. A medida que la colección crece, resulta
más difícil conocer qué juegos se poseen, decidir cuál jugar y
aprovechar adecuadamente la colección.

La aplicación pretende resolver estos problemas mediante una plataforma
centralizada que permita:

-   consultar un catálogo de juegos de mesa;
-   obtener recomendaciones adaptadas a las necesidades del usuario;
-   gestionar una ludoteca personal;
-   gestionar ludotecas de asociaciones;
-   consultar información detallada de cada juego;
-   consultar y comprender las mecánicas de los juegos;
-   publicar y consultar comentarios de la comunidad;
-   mantener sincronizados los datos del catálogo con fuentes externas,
    principalmente la API de BoardGameGeek (BGG).

La aplicación se plantea como una arquitectura de microservicios
desplegable en infraestructura cloud, de forma que los componentes
puedan evolucionar, desplegarse y escalar de manera independiente.

### 1.2. Usuarios del sistema

Se contemplan inicialmente los siguientes perfiles funcionales:

-   **Visitante:** puede consultar juegos, mecánicas, comentarios
    públicos y utilizar las funciones públicas disponibles.
-   **Usuario registrado:** dispone de una cuenta y puede gestionar su
    ludoteca, publicar comentarios y obtener recomendaciones
    personalizadas.
-   **Asociación:** cuenta especializada cuya ludoteca representa la
    colección de una asociación de juegos de mesa. Los administradores
    pueden realizar cargas masivas de juegos mediante identificadores
    BGG.
-   **Administrador:** gestiona usuarios, catálogo, sincronizaciones,
    contenido y operaciones de mantenimiento.

### 1.3. Casos de uso principales

1.  **Consultar el catálogo.** Buscar juegos y consultar su información,
    incluyendo número de jugadores, duración, complejidad, categorías,
    mecánicas, valoración y rankings.
2.  **Obtener recomendaciones.** Solicitar juegos adecuados indicando
    restricciones y preferencias como jugadores, duración, complejidad,
    mecánicas, categorías y tipo de juego.
3.  **Gestionar una ludoteca.** Añadir o eliminar juegos de la colección
    de un usuario.
4.  **Gestionar una ludoteca de asociación.** Incorporar de forma masiva
    una lista de juegos a partir de sus identificadores BGG.
5.  **Consultar mecánicas.** Acceder a un diccionario de mecánicas en
    español con una explicación comprensible de cada una.
6.  **Participar en la comunidad.** Leer comentarios públicos y, si se
    dispone de una cuenta, publicar o eliminar los comentarios propios.
7.  **Sincronizar el catálogo.** Obtener o actualizar información de
    juegos desde BGG sin que el usuario tenga que introducir manualmente
    los datos.
8.  **Administrar la plataforma.** Gestionar usuarios, contenido,
    sincronizaciones y estado de mantenimiento.

------------------------------------------------------------------------

## 2. Justificación según NIST SP 800-145

NIST SP 800-145 define *cloud computing* mediante cinco características
esenciales: **autoservicio bajo demanda, acceso amplio a la red,
agrupación de recursos, rápida elasticidad y servicio medido**.

La arquitectura objetivo del proyecto se diseña para aprovechar estas
características de la siguiente forma.

### 2.1. Autoservicio bajo demanda (*On-demand self-service*)

Los usuarios pueden utilizar las capacidades de la aplicación sin
intervención manual del proveedor del servicio:

-   crear y utilizar una cuenta;
-   consultar el catálogo;
-   solicitar recomendaciones;
-   añadir o eliminar juegos de su ludoteca;
-   consultar mecánicas;
-   publicar comentarios.

Desde el punto de vista de infraestructura, los servicios se diseñan
para poder desplegarse y aprovisionarse mediante automatización,
evitando configuraciones manuales específicas para cada usuario.

### 2.2. Acceso amplio a la red (*Broad network access*)

La aplicación se ofrece mediante protocolos web estándar:

-   **HTTPS** para el acceso desde navegadores y clientes;
-   **REST/JSON** para la comunicación con la API;
-   diseño adaptable para ordenadores, tabletas y dispositivos móviles.

Esto permite acceder al servicio desde diferentes plataformas sin
requerir software cliente específico.

### 2.3. Asignación común de recursos (*Resource pooling*)

Los recursos cloud de cómputo, red y almacenamiento son compartidos por
múltiples usuarios mediante un modelo multiusuario.

Las instancias de los microservicios atienden peticiones de diferentes
consumidores y utilizan recursos compartidos del proveedor cloud. La
información lógica de cada usuario se mantiene aislada mediante
autenticación, autorización e identificadores de propietario.

Los servicios de base de datos y caché pueden ejecutarse sobre
infraestructura administrada y compartida, manteniendo separación lógica
entre los datos de los distintos dominios.

### 2.4. Rápida elasticidad (*Rapid elasticity*)

Los microservicios se diseñan como procesos independientes y, siempre
que sea posible, sin estado local persistente. Esto permite crear o
eliminar réplicas según la demanda.

Ejemplos:

-   escalar el servicio de recomendaciones cuando aumente el número de
    consultas;
-   escalar el servicio de catálogo durante procesos intensivos de
    consulta;
-   mantener el servicio de usuarios con una capacidad diferente a la
    del motor de recomendaciones;
-   utilizar caché para reducir carga sobre servicios y bases de datos.

La separación por microservicios evita tener que escalar toda la
aplicación cuando únicamente aumenta la demanda de una funcionalidad.

### 2.5. Servicio medido (*Measured service*)

La infraestructura y la aplicación deberán recopilar métricas como:

-   número de peticiones;
-   latencia y tasa de errores;
-   consumo de CPU y memoria;
-   almacenamiento utilizado;
-   tráfico de red;
-   número y duración de consultas a base de datos;
-   uso de caché;
-   número de sincronizaciones realizadas contra servicios externos.

Estas métricas permiten observar el comportamiento del sistema, detectar
problemas y relacionar el consumo real de recursos con el coste de la
infraestructura.


## 3. Mapeo de actores según NIST SP 500-292

NIST SP 500-292 define cinco actores principales: **Cloud Consumer,
Cloud Provider, Cloud Broker, Cloud Auditor y Cloud Carrier**. En este
proyecto se realiza el siguiente mapeo.

  -----------------------------------------------------------------------
  Actor NIST        Correspondencia   Responsabilidad   Impacto económico
                    en el proyecto                      
  ----------------- ----------------- ----------------- -----------------
  **Consumidor      Usuarios,         Consumir las      El crecimiento
  (Cloud            asociaciones y    funcionalidades   del número de
  Consumer)**       administradores   ofrecidas por la  consumidores
                    que utilizan la   plataforma        incrementa
                    aplicación                          peticiones,
                                                        almacenamiento y
                                                        transferencia,
                                                        afectando al
                                                        coste operativo.
                                                        En un modelo
                                                        comercial podría
                                                        existir una
                                                        suscripción o
                                                        plan de uso

  **Proveedor       Proveedor de      Proporcionar      Principal coste
  (Cloud            infraestructura o cómputo, red,     recurrente del
  Provider)**       plataforma cloud  almacenamiento,   sistema.
                    donde se          bases de datos y  Normalmente
                    desplieguen los   servicios         depende de
                    servicios         administrados     recursos
                                                        reservados o
                                                        consumidos

  **Intermediario   Plataforma de     Simplificar       Puede añadir una
  (Cloud Broker)**  intermediación o  despliegue,       tarifa de
                    PaaS, si se       operación,        gestión, pero
                    utiliza para      agregación o      reduce costes de
                    abstraer y        selección de      operación y
                    gestionar         servicios cloud   complejidad. Si
                    servicios de uno                    se despliega
                    o varios                            directamente
                    proveedores                         sobre un único
                                                        proveedor, este
                                                        actor no necesita
                                                        materializarse
                                                        como entidad
                                                        independiente

  **Auditor (Cloud  Entidad o         Evaluar de forma  Introduce costes
  Auditor)**        servicio          independiente la  de auditoría y
                    independiente     operación,        monitorización,
                    encargado de      seguridad,        pero reduce
                    revisar           disponibilidad y  riesgo operativo,
                    seguridad,        controles del     de seguridad y de
                    rendimiento y     sistema           incumplimiento
                    cumplimiento                        

  **Operador /      Proveedores de    Proporcionar      Su coste se
  Carrier (Cloud    Internet y redes  conectividad y    refleja en
  Carrier)**        que transportan   transporte de     conectividad,
                    las               datos             ancho de banda y
                    comunicaciones                      transferencia de
                    entre                               datos; la calidad
                    consumidores y                      de la red influye
                    servicios cloud                     directamente en
                                                        latencia y
                                                        disponibilidad
  -----------------------------------------------------------------------


## 4. Arquitectura propuesta

### 4.1. Componentes

La arquitectura objetivo se divide inicialmente en tres microservicios
de negocio:

1.  **Servicio de Usuarios y Ludotecas**
    -   registro e inicio de sesión;
    -   perfiles y roles;
    -   cuentas de usuario y asociación;
    -   ludotecas personales y de asociaciones;
    -   autorización sobre recursos del usuario.
2.  **Servicio de Catálogo**
    -   información de juegos;
    -   categorías y mecánicas;
    -   traducciones;
    -   rankings BGG;
    -   comentarios públicos;
    -   sincronización con la API externa de BGG.
3.  **Servicio de Recomendaciones**
    -   aplicación de filtros;
    -   cálculo de puntuaciones;
    -   recomendaciones personalizadas;
    -   consulta del catálogo y, cuando sea necesario, de la ludoteca
        del usuario.

Además se incorporan los siguientes componentes de infraestructura:

-   **API Gateway / Ingress:** punto de entrada único para los clientes.
-   **PostgreSQL de Usuarios:** persistencia del dominio de usuarios y
    ludotecas.
-   **PostgreSQL de Catálogo:** persistencia de juegos, mecánicas,
    rankings y comentarios.
-   **Redis:** caché de consultas frecuentes y resultados temporales de
    recomendación.
-   **API de BGG:** fuente externa utilizada para sincronizar datos del
    catálogo.
-   **Observabilidad:** métricas, logs y monitorización de los
    servicios.

Se aplica el principio de **base de datos por servicio**: un
microservicio no accede directamente a las tablas pertenecientes a otro
servicio; la comunicación entre dominios se realiza a través de sus
APIs.

### 4.2. Diagrama de arquitectura

``` mermaid
flowchart TB
    U["Usuario / Asociación / Administrador"]

    subgraph CLOUD["Entorno Cloud"]
        GW["API Gateway / Ingress"]

        US["Microservicio de<br/>Usuarios y Ludotecas"]
        CS["Microservicio de<br/>Catálogo"]
        RS["Microservicio de<br/>Recomendaciones"]

        UDB[("PostgreSQL<br/>Usuarios y Ludotecas")]
        CDB[("PostgreSQL<br/>Catálogo")]
        CACHE[("Redis<br/>Caché")]

        OBS["Logs / Métricas /<br/>Monitorización"]

        GW -->|"HTTPS · REST/JSON"| US
        GW -->|"HTTPS · REST/JSON"| CS
        GW -->|"HTTPS · REST/JSON"| RS

        US -->|"SQL/TLS"| UDB
        CS -->|"SQL/TLS"| CDB

        RS -->|"HTTP · REST/JSON"| US
        RS -->|"HTTP · REST/JSON"| CS
        RS -->|"RESP/TLS"| CACHE

        US -.->|"métricas / logs"| OBS
        CS -.->|"métricas / logs"| OBS
        RS -.->|"métricas / logs"| OBS
    end

    BGG["API externa de BoardGameGeek"]

    U -->|"HTTPS"| GW
    CS -->|"HTTPS · XML"| BGG
```

### 4.3. Protocolos de comunicación

  -------------------------------------------------------------------------
  Origen              Destino           Protocolo         Formato
  ------------------- ----------------- ----------------- -----------------
  Navegador/cliente   API Gateway       HTTPS             HTTP + JSON/HTML

  API Gateway         Microservicios    HTTP/HTTPS REST   JSON

  Recomendaciones     Catálogo          HTTP REST         JSON

  Recomendaciones     Usuarios y        HTTP REST         JSON
                      Ludotecas                           

  Catálogo            BGG               HTTPS             XML

  Microservicios      PostgreSQL        TCP/TLS           Protocolo
                                                          PostgreSQL

  Recomendaciones     Redis             TCP/TLS           RESP

  Microservicios      Observabilidad    HTTPS/OTLP o      Métricas y logs
                                        protocolo         
                                        equivalente       
  -------------------------------------------------------------------------

### 4.4. Decisiones arquitectónicas iniciales

-   Los microservicios serán desplegables de forma independiente.
-   No se almacenará estado de sesión crítico en memoria local de una
    instancia.
-   Los datos persistentes se almacenarán fuera de los contenedores.
-   Cada servicio será propietario de sus datos.
-   La comunicación síncrona entre servicios utilizará REST/JSON
    inicialmente.
-   Las operaciones externas costosas, como sincronizaciones masivas,
    podrán evolucionar a procesamiento asíncrono mediante una cola de
    mensajes.
-   Redis se utilizará únicamente como caché; la pérdida de la caché no
    debe implicar pérdida de información de negocio.
-   Las APIs públicas se versionarán mediante el prefijo `/api/v1`.

------------------------------------------------------------------------

## 5. Especificación sintética de la API REST

La API se expone bajo el prefijo:

``` text
/api/v1
```

Los ejemplos siguientes representan el contrato objetivo inicial y
podrán refinarse durante la definición de historias de usuario.

### 5.1. Autenticación y usuarios

#### `POST /api/v1/auth/register`

Crea una cuenta.

``` json
{
  "nombre": "Carlos",
  "email": "usuario@ejemplo.com",
  "contrasena": "********"
}
```

Respuesta `201 Created`:

``` json
{
  "id": 42,
  "nombre": "Carlos",
  "email": "usuario@ejemplo.com",
  "tipo_cuenta": "usuario"
}
```

#### `POST /api/v1/auth/login`

Autentica al usuario.

``` json
{
  "email": "usuario@ejemplo.com",
  "contrasena": "********"
}
```

Respuesta `200 OK`:

``` json
{
  "usuario": {
    "id": 42,
    "nombre": "Carlos",
    "tipo_cuenta": "usuario"
  }
}
```

#### `POST /api/v1/auth/logout`

Finaliza la sesión del usuario.

#### `GET /api/v1/users/me`

Devuelve los datos del usuario autenticado.

------------------------------------------------------------------------

### 5.2. Catálogo

#### `GET /api/v1/games`

Busca o lista juegos.

Parámetros de consulta opcionales:

``` text
?query=terraforming&players=4&mechanic=deck-building&page=1
```

#### `GET /api/v1/games/{bgg_id}`

Devuelve la ficha completa de un juego.

Respuesta simplificada:

``` json
{
  "id_bgg": 167791,
  "nombre": "Terraforming Mars",
  "min_jugadores": 1,
  "max_jugadores": 5,
  "duracion_minima": 120,
  "duracion_maxima": 120,
  "complejidad": 3.26,
  "valoracion_media": 8.3,
  "tipos_bgg": ["estrategia"],
  "mecanicas": [
    {
      "id": 1,
      "nombre": "Gestión de mano"
    }
  ]
}
```

#### `POST /api/v1/admin/catalog/sync`

Sincroniza juegos con la fuente externa. Requiere permisos de
administrador.

``` json
{
  "bgg_ids": [167791, 174430, 224517]
}
```

Respuesta `202 Accepted`:

``` json
{
  "estado": "aceptado",
  "total": 3
}
```

------------------------------------------------------------------------

### 5.3. Mecánicas

#### `GET /api/v1/mechanics`

Devuelve las mecánicas disponibles.

#### `GET /api/v1/mechanics/{mechanic_id}`

Devuelve la explicación de una mecánica.

``` json
{
  "id": 15,
  "nombre": "Colocación de trabajadores",
  "nombre_original": "Worker Placement",
  "descripcion": "Los jugadores colocan trabajadores en espacios de acción para obtener recursos, puntos o efectos."
}
```

------------------------------------------------------------------------

### 5.4. Ludoteca

#### `GET /api/v1/library`

Obtiene la ludoteca del usuario autenticado.

#### `POST /api/v1/library/games`

Añade un juego.

``` json
{
  "bgg_id": 167791
}
```

Respuesta `201 Created`:

``` json
{
  "bgg_id": 167791,
  "anadido": true
}
```

#### `DELETE /api/v1/library/games/{bgg_id}`

Elimina un juego de la ludoteca del usuario autenticado.

#### `PATCH /api/v1/library/games/{bgg_id}`

Actualiza datos propios del usuario asociados al juego.

``` json
{
  "valoracion": 9.0,
  "num_partidas": 12
}
```

------------------------------------------------------------------------

### 5.5. Ludotecas de asociaciones

#### `POST /api/v1/admin/associations/{user_id}/games/bulk`

Carga una lista de juegos en la ludoteca de una cuenta de tipo
asociación. Requiere permisos administrativos.

``` json
{
  "bgg_ids": [
    167791,
    174430,
    224517,
    266192
  ]
}
```

Respuesta:

``` json
{
  "recibidos": 4,
  "anadidos": 4,
  "omitidos": 0
}
```

------------------------------------------------------------------------

### 5.6. Recomendaciones

#### `POST /api/v1/recommendations`

Solicita recomendaciones.

``` json
{
  "jugadores_min": 3,
  "jugadores_max": 4,
  "duracion_maxima": 90,
  "complejidad_maxima": 3.0,
  "mecanicas": [
    "Worker Placement",
    "Deck Building"
  ],
  "categorias": [
    "Economic"
  ],
  "tipo_juego": "estrategia",
  "ambito": "todos",
  "limite": 10
}
```

Valores previstos para `ambito`:

-   `todos`: catálogo completo;
-   `ludoteca`: únicamente juegos que posee el usuario;
-   `fuera_ludoteca`: excluye los juegos que ya posee.

Respuesta simplificada:

``` json
{
  "resultados": [
    {
      "id_bgg": 12345,
      "nombre": "Ejemplo",
      "puntuacion": 8.7,
      "motivos": [
        "Adecuado para 4 jugadores",
        "Duración compatible",
        "Coincide con las mecánicas seleccionadas"
      ]
    }
  ]
}
```

------------------------------------------------------------------------

### 5.7. Comentarios públicos

#### `GET /api/v1/games/{bgg_id}/comments`

Obtiene los comentarios públicos de un juego.

#### `POST /api/v1/games/{bgg_id}/comments`

Publica un comentario. Requiere autenticación.

``` json
{
  "comentario": "Funciona especialmente bien a cuatro jugadores."
}
```

#### `DELETE /api/v1/comments/{comment_id}`

Elimina un comentario. Solo puede hacerlo su autor o un administrador.

------------------------------------------------------------------------

## 6. Códigos HTTP principales

  Código                        Uso
  ----------------------------- -------------------------------------------------
  `200 OK`                      Consulta o modificación realizada correctamente
  `201 Created`                 Recurso creado
  `202 Accepted`                Operación larga aceptada para procesamiento
  `204 No Content`              Eliminación correcta sin cuerpo de respuesta
  `400 Bad Request`             Payload o parámetros no válidos
  `401 Unauthorized`            Usuario no autenticado
  `403 Forbidden`               Usuario autenticado sin permisos
  `404 Not Found`               Recurso inexistente
  `409 Conflict`                Conflicto con el estado actual del recurso
  `422 Unprocessable Entity`    Error de validación
  `500 Internal Server Error`   Error interno no controlado
  `503 Service Unavailable`     Servicio temporalmente no disponible

------------------------------------------------------------------------
