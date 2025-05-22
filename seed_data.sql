-- SEED DATA PARA PRUEBAS

-- 1. Usuarios (admin, operador, cliente) con contraseña '12345'
INSERT INTO usuarios (username, password_hash, role_id) VALUES
  ('admin1', crypt('12345', gen_salt('bf')), 1),
  ('admin2', crypt('12345', gen_salt('bf')), 1),
  ('op1',    crypt('12345', gen_salt('bf')), 2),
  ('op2',    crypt('12345', gen_salt('bf')), 2),
  ('op3',    crypt('12345', gen_salt('bf')), 2),
  ('cli1',   crypt('12345', gen_salt('bf')), 3),
  ('cli2',   crypt('12345', gen_salt('bf')), 3),
  ('cli3',   crypt('12345', gen_salt('bf')), 3),
  ('cli4',   crypt('12345', gen_salt('bf')), 3),
  ('cli5',   crypt('12345', gen_salt('bf')), 3)
ON CONFLICT (username) DO NOTHING;

-- 2. Bicicletas (5 con dueño, 5 sin dueño)
-- NOTA: Asegúrate de que los IDs de usuarios existan antes de correr esto.

-- Bicis con dueño (asignadas a clientes del 6 al 10)
INSERT INTO ebikes (serial, owner_id, estado_id, novedad_id) VALUES
  ('E-BIKE-001', 6, 1, 1),
  ('E-BIKE-002', 7, 1, 1),
  ('E-BIKE-003', 8, 1, 1),
  ('E-BIKE-004', 9, 1, 1),
  ('E-BIKE-005',10, 1, 1)

-- Bicis sin dueño
, ('E-BIKE-006', NULL, 1, 1),
  ('E-BIKE-007', NULL, 1, 1),
  ('E-BIKE-008', NULL, 1, 1),
  ('E-BIKE-009', NULL, 1, 1),
  ('E-BIKE-010', NULL, 1, 1)
ON CONFLICT (serial) DO NOTHING;
