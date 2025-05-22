-- 1. Base de datos (solo si aún no está creada)
CREATE DATABASE roda_db;
\c roda_db;

-- 2. Tabla de roles
CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) UNIQUE NOT NULL
);

-- 3. Usuarios
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_base64 TEXT NOT NULL,
  role_id INT NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4. Estados
CREATE TABLE estados (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) UNIQUE NOT NULL,
  descripcion TEXT NOT NULL
);

-- 5. Novedades
CREATE TABLE novedades (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) UNIQUE NOT NULL
);

-- 6. Relación novedades ↔ estados
CREATE TABLE novedades_estados (
  novedad_id INT NOT NULL REFERENCES novedades(id) ON DELETE CASCADE,
  estado_id  INT NOT NULL REFERENCES estados(id)  ON DELETE CASCADE,
  PRIMARY KEY (novedad_id, estado_id)
);

-- 7. Vista para describir estados
CREATE OR REPLACE VIEW vista_estados AS
SELECT
  e.id,
  e.nombre AS state_name,
  (e.id <> 1) AS bloqueado,
  e.descripcion AS description
FROM estados e;

-- 8. eBikes
CREATE TABLE ebikes (
  id SERIAL PRIMARY KEY,
  serial VARCHAR(100) UNIQUE NOT NULL,
  owner_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
  estado_id INT NOT NULL REFERENCES estados(id),
  novedad_id INT NOT NULL REFERENCES novedades(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 9. Timeline (ahora con actor y comentario)
CREATE TABLE timeline_ebikes (
  id SERIAL PRIMARY KEY,
  ebike_id INT NOT NULL REFERENCES ebikes(id) ON DELETE CASCADE,
  estado_id INT NOT NULL REFERENCES estados(id),
  novedad_id INT NOT NULL REFERENCES novedades(id),
  change_ts TIMESTAMPTZ NOT NULL,
  actor_id INT REFERENCES usuarios(id),
  comentario TEXT
);

-- 10. Función de timeline + timestamp actualizado
CREATE OR REPLACE FUNCTION fn_actualizar_ebike() RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  INSERT INTO timeline_ebikes(ebike_id, estado_id, novedad_id, change_ts)
    VALUES (NEW.id, NEW.estado_id, NEW.novedad_id, now());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 11. Triggers para INSERT y UPDATE
DROP TRIGGER IF EXISTS trg_ebikes_update ON ebikes;
DROP TRIGGER IF EXISTS trg_ebikes_insert ON ebikes;

CREATE TRIGGER trg_ebikes_update
  AFTER UPDATE ON ebikes
  FOR EACH ROW EXECUTE PROCEDURE fn_actualizar_ebike();

CREATE TRIGGER trg_ebikes_insert
  AFTER INSERT ON ebikes
  FOR EACH ROW EXECUTE PROCEDURE fn_actualizar_ebike();
