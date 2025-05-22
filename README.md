Documentación Completa: Microservicio 
e-Bike Autolock 
Este documento describe en detalle la arquitectura, capas, entidades, repositorios, 
fábricas, casos de uso, interfaces API (Blueprints), conexión a BD, migraciones, 
simulación GPS, triggers, hashing de contraseñas, Dockerización y mecanismos de 
seguridad de la solución. 
1. Arquitectura General (Clean Architecture) 
src/ 
├── domain/               
├── usecases/             
├── interfaces/ 
│   ├── api/              
│   └── device/           
├── infrastructure/ 
│   ├── db/               
# Entidades y reglas de negocio 
# Servicios de aplicación (casos de uso) 
# Flask Blueprints (auth, bikes, users) 
# Stub HTTP del GPS/autolock 
# SQLAlchemy (Base, models, sesión) 
│   ├── repositories/     # Repositorios concretos 
│   └── services/         
# Cliente HTTP al stub GPS 
├── config/               
└── main.py               
# Carga de `.env` y settings 
# Factory de Flask, registro de Blueprints 
● Dependencias: Flask, Flask-JWT-Extended, Flask-Migrate, Flask-SQLAlchemy, 
python-dotenv, psycopg2-binary, Flask-CORS, APScheduler (opcional), 
bcrypt/pgcrypto, pytest, requests. 
● Principio: cada capa solo conoce la capa interior (Inversión de Dependencias). 
2. Capa de Dominio (src/domain) 
2.1 Entidades 
● Usuario: id, username, password_hash (pgcrypto), role_id, created_at 
● Rol: id, nombre 
● Estado: id, nombre, descripcion 
● Novedad: id, nombre 
● EBike: id, serial, owner_id, estado_id, novedad_id, updated_at 
● TimelineEBike: id, ebike_id, estado_id, novedad_id, change_ts, actor_id, 
comentario 
2.2 Repositorios (Interfaces) 
● AbstractUserRepository 
● AbstractBikeRepository 
● AbstractEventRepository 
3. Infraestructura 
3.1 Modelos SQLAlchemy (infrastructure/db/models.py) 
class Usuario(Base): 
__tablename__ = 'usuarios' 
id             
= Column(Integer, primary_key=True) 
username       
= Column(String(50), unique=True, nullable=False) 
password_hash  = Column(Text, nullable=False)  # pgcrypto hashed 
role_id        
= Column(Integer, ForeignKey('roles.id'), nullable=False) 
created_at     = Column(TIMESTAMP(timezone=True), server_default=func.now()) 
rol            
= relationship('Rol', back_populates='usuarios') 
ebikes         
= relationship('EBike', back_populates='owner') 
3.2 Trigger de BD (roda_schema.sql) 
● Objetivo: Mantener trazabilidad en timeline_ebikes al insertar o actualizar 
ebikes. 
Trigger y función: 
CREATE FUNCTION fn_actualizar_ebike() RETURNS trigger AS $$ 
BEGIN 
NEW.updated_at = now(); 
INSERT INTO timeline_ebikes(ebike_id, estado_id, novedad_id, actor_id, comentario, 
change_ts) 
VALUES (NEW.id, NEW.estado_id, NEW.novedad_id, 
current_setting('jwt.claims.user_id')::int, NULL, now()); 
RETURN NEW; 
END; 
$$ LANGUAGE plpgsql; 
CREATE TRIGGER trg_ebikes_change 
BEFORE INSERT OR UPDATE ON ebikes 
FOR EACH ROW EXECUTE PROCEDURE fn_actualizar_ebike(); 
●  
● Beneficio: no hay necesidad de lógica adicional en la capa de aplicación para 
registrar el historial. 
3.3 Repositorios SQLAlchemy 
● UserRepository: métodos get_by_username, get_by_id, save, 
update_role 
● BikeRepository: list_all, get_by_id, update_state, get_timeline 
● Cada consulta usa parametrización del ORM, evitando inyección SQL. 
3.4 Factories 
● UserFactory: genera Usuario con pgcrypto hashing (crypt + 
gen_salt('bf')). 
● EBikeFactory: valida unicidad y crea instancia. 
4. Casos de Uso (src/usecases) 
● AuthService: autenticación, validación Base64→Hash + JWT 
● ChangeUserRoleService: cambio de rol con validación de permisos 
● ImmobilizeBikeService: lock/unlock integrando GPSHttpClient, manejo de 
errores (502 si falla stub) 
5. Interfaces API (Flask Blueprints) 
5.1 Auth (auth_blueprint.py) 
● POST /api/auth/login 
○ Valida usuario/password hash 
○ Genera JWT con claims: user_id, username, role 
5.2 eBikes (bikes_blueprint.py) 
● GET /api/bikes/ 
● GET /api/bikes/<id> 
● POST /api/bikes/<id>/lock 
● POST /api/bikes/<id>/unlock 
● POST /api/bikes/register 
● PATCH /api/bikes/<id>/assign-owner 
● Seguridad: @jwt_required, @roles_required 
5.3 Users (users_blueprint.py) 
● POST /api/users/register 
● POST /api/users/<id>/set-role 
● GET /api/roles 
5.4 GPS Stub (device/gps_service_stub.py) 
● POST /api/device/lock, /unlock 
● GET /api/device/status/<id> 
● Simula delays y errores aleatorios, mantiene estado en memoria. 
6. Conexión a BD y Migraciones 
6.1 Settings (config/settings.py) 
load_dotenv() 
SQLALCHEMY_DATABASE_URI = ( 
f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 
) 
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') 
6.2 Alembic 
● alembic.ini: sqlalchemy.url = ${SQLALCHEMY_DATABASE_URI} 
● Migraciones generadas con flask db migrate y flask db upgrade. 
7. Seguridad y Calidad 
● Hashing: pgcrypto en BD o bcrypt en Python para password_hash. 
● Inyección SQL: protegido por SQLAlchemy (parametrización). 
● Control de roles: @roles_required(admin, operador, cliente). 
● Rate limiting: opcional con Flask-Limiter. 
● Tests: pytest para flujos críticos; reportes con pytest-cov. 
8. Docker & Despliegue 
● Dockerfile: Python 3.11, instala deps, copia código, ejecuta run.sh. 
● run.sh: crea .env, instala deps, exporta variables, arranca python src/main.py. 
● docker-compose.yml: servicios app + postgres-db, volumenes y redes. 
docker-compose up --build 
9. Flow de Roles 
● Admin: registra usuarios, asigna roles, crea/edita ebikes, lock/unlock. 
● Operador: lock/unlock, assign-owner. 
● Cliente: reporta robo (lock), consulta estado. 
Fin de la documentación.
