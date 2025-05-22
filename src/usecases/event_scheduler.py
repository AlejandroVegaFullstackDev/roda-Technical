from apscheduler.schedulers.background import BackgroundScheduler
from infrastructure.db import SessionLocal
from infrastructure.repositories.bike_repository_sqlalchemy import BikeRepository
from infrastructure.services.gps_client_http import GPSHttpClient
from usecases.immobilize_bike_service import ImmobilizeBikeService

def revisar_morosos():
    db = SessionLocal()
    repo = BikeRepository(db)
    gps = GPSHttpClient()
    service = ImmobilizeBikeService(repo, gps)

    # Simulación: ebikes con estado "1" (disponible) y dueño con nombre "juan" están en mora
    bicis = repo.list_all()
    for bici in bicis:
        if bici.estado_id == 1 and bici.owner.username == "juan":  # reemplaza por lógica real
            try:
                print(f"🔁 Bloqueando bici ID={bici.id} por mora (cron)")
                service.lock_bike(bici, "mora")
            except Exception as e:
                print(f"❌ Error al bloquear bici {bici.id}: {e}")

def iniciar_cron():
    scheduler = BackgroundScheduler()
    scheduler.add_job(revisar_morosos, 'interval', minutes=20)
    scheduler.start()
