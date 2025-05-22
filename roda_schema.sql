-- 1. Base de datos (solo si aún no está creada)
--  CREATE DATABASE roda_db;

-- 2. Habilitar la extensión pgcrypto para bcrypt
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 3. Tabla de roles
CREATE TABLE IF NOT EXISTS roles (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO roles (id, nombre) VALUES
  (1, 'admin'),
  (2, 'operador'),
  (3, 'cliente')
ON CONFLICT (id) DO NOTHING;

-- 4. Usuarios
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role_id INT NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Poblar usuarios con bcrypt
INSERT INTO usuarios (username, password_hash, role_id) VALUES
  ('juan', crypt('12345', gen_salt('bf')), 3),
  ('maria', crypt('12345', gen_salt('bf')), 2)
ON CONFLICT (username) DO NOTHING;

-- 5. Estados
CREATE TABLE estados (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) UNIQUE NOT NULL,
  descripcion TEXT NOT NULL
);

INSERT INTO estados (id, nombre, descripcion) VALUES
  (1, 'Disponible',    'Disponible/Desbloqueado/estado libre'),
  (2, 'Robo',          'Bloqueado por robo'),
  (3, 'Falta de Pago', 'Bloqueado por falta de pago')
ON CONFLICT (id) DO NOTHING;

-- 6. Novedades
CREATE TABLE novedades (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO novedades (id, nombre) VALUES
  (1, 'Disponible'),
  (2, 'No Disponible')
ON CONFLICT (id) DO NOTHING;

-- 7. Relación novedades ↔ estados
CREATE TABLE novedades_estados (
  novedad_id INT NOT NULL REFERENCES novedades(id) ON DELETE CASCADE,
  estado_id  INT NOT NULL REFERENCES estados(id)  ON DELETE CASCADE,
  PRIMARY KEY (novedad_id, estado_id)
);

INSERT INTO novedades_estados (novedad_id, estado_id) VALUES
  (1, 1),
  (2, 2),
  (2, 3)
ON CONFLICT (novedad_id, estado_id) DO NOTHING;

-- 8. Vista para describir estados
CREATE OR REPLACE VIEW vista_estados AS
SELECT
  e.id,
  e.nombre    AS state_name,
  (e.id <> 1) AS bloqueado,
  e.descripcion AS description
FROM estados e;

-- 9. eBikes
CREATE TABLE ebikes (
  id SERIAL PRIMARY KEY,
  serial     VARCHAR(100) UNIQUE NOT NULL,
  owner_id   INT NULL REFERENCES usuarios(id) ON DELETE SET NULL,
  estado_id  INT NOT NULL REFERENCES estados(id),
  novedad_id INT NOT NULL REFERENCES novedades(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 10. Timeline (ahora con actor y comentario)
CREATE TABLE timeline_ebikes (
  id         SERIAL PRIMARY KEY,
  ebike_id   INT NOT NULL REFERENCES ebikes(id) ON DELETE CASCADE,
  estado_id  INT NOT NULL REFERENCES estados(id),
  novedad_id INT NOT NULL REFERENCES novedades(id),
  change_ts  TIMESTAMPTZ NOT NULL,
  actor_id   INT NULL REFERENCES usuarios(id),
  comentario TEXT
);

-- 11. Función actualizada que usa actor_id y comentario de la sesión
CREATE OR REPLACE FUNCTION fn_actualizar_ebike() RETURNS trigger AS $$
DECLARE
  actor_id INT := current_setting('app.current_user_id', true)::INT;
  comentario TEXT := current_setting('app.comentario', true);
BEGIN
  NEW.updated_at = now();
  INSERT INTO timeline_ebikes (
    ebike_id, estado_id, novedad_id, change_ts, actor_id, comentario
  )
  VALUES (
    NEW.id, NEW.estado_id, NEW.novedad_id, now(), actor_id, comentario
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 12. Triggers para INSERT y UPDATE
DROP TRIGGER IF EXISTS trg_ebikes_update ON ebikes;
DROP TRIGGER IF EXISTS trg_ebikes_insert ON ebikes;

CREATE TRIGGER trg_ebikes_update
  AFTER UPDATE ON ebikes
  FOR EACH ROW EXECUTE PROCEDURE fn_actualizar_ebike();

CREATE TRIGGER trg_ebikes_insert
  AFTER INSERT ON ebikes
  FOR EACH ROW EXECUTE PROCEDURE fn_actualizar_ebike();
