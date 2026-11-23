-- Esquema mínimo de catálogo. No elimina tablas ni datos preexistentes.
-- Posteriormente se incorporará a las migraciones de Alembic.
CREATE TABLE IF NOT EXISTS juegos (
    id_bgg INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    anio_publicacion INTEGER,
    min_jugadores INTEGER,
    max_jugadores INTEGER,
    duracion_minima INTEGER,
    duracion_maxima INTEGER,
    edad_minima INTEGER,
    valoracion_media DOUBLE PRECISION,
    complejidad DOUBLE PRECISION,
    imagen_url TEXT,
    min_jugadores_recomendados INTEGER,
    max_jugadores_recomendados INTEGER,
    min_mejor_num_jugadores INTEGER,
    max_mejor_num_jugadores INTEGER,
    tipos_bgg TEXT DEFAULT '',
    ranking_general INTEGER,
    ranking_estrategia INTEGER,
    ranking_familiar INTEGER,
    ranking_tematico INTEGER,
    ranking_abstracto INTEGER,
    ranking_party INTEGER,
    ranking_wargame INTEGER,
    ranking_infantil INTEGER
);

CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS mecanicas (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS juego_categoria (
    juego_id INTEGER NOT NULL REFERENCES juegos(id_bgg) ON DELETE CASCADE,
    categoria_id INTEGER NOT NULL REFERENCES categorias(id) ON DELETE CASCADE,
    PRIMARY KEY (juego_id, categoria_id)
);

CREATE TABLE IF NOT EXISTS juego_mecanica (
    juego_id INTEGER NOT NULL REFERENCES juegos(id_bgg) ON DELETE CASCADE,
    mecanica_id INTEGER NOT NULL REFERENCES mecanicas(id) ON DELETE CASCADE,
    PRIMARY KEY (juego_id, mecanica_id)
);

CREATE INDEX IF NOT EXISTS idx_juegos_nombre ON juegos (lower(nombre));
CREATE INDEX IF NOT EXISTS idx_juegos_jugadores ON juegos (min_jugadores, max_jugadores);
CREATE INDEX IF NOT EXISTS idx_juegos_duracion ON juegos (duracion_maxima);
CREATE INDEX IF NOT EXISTS idx_juegos_valoracion ON juegos (valoracion_media DESC);
CREATE INDEX IF NOT EXISTS idx_juego_categoria_categoria ON juego_categoria (categoria_id);
CREATE INDEX IF NOT EXISTS idx_juego_mecanica_mecanica ON juego_mecanica (mecanica_id);
