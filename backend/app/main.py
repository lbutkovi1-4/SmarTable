from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine, SessionLocal
from .routers import auth as auth_router
from .routers import tables as tables_router
from .routers import reservations as reservations_router
from .routers import users as users_router
from . import auth as auth_utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmarTable API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(tables_router.router)
app.include_router(reservations_router.router)
app.include_router(users_router.router)


@app.on_event("startup")
def seed_admin():
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.email == "admin@smartable.com").first()
        if not existing:
            admin = models.User(
                full_name="Administrator",
                email="admin@smartable.com",
                hashed_password=auth_utils.hash_password("admin123"[:72]),
                role=models.UserRole.admin,
            )
            db.add(admin)
            db.commit()

        # Dodaj stolove ako ih nema
        if db.query(models.RestaurantTable).count() == 0:
            stolovi = [
    models.RestaurantTable(name="Stol 1", capacity=2, description="Romanticni kutak kraj prozora"),
    models.RestaurantTable(name="Stol 2", capacity=4, description="Idealno za obitelj"),
    models.RestaurantTable(name="Stol 3", capacity=6, description="Prostrani stol na terasi"),
    models.RestaurantTable(name="Stol 4", capacity=8, description="Savrseno za grupne proslave"),
    models.RestaurantTable(name="Stol 5", capacity=2, description="Tihi kutak u unutrasnjosti"),
]
            db.add_all(stolovi)
            db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "SmarTable API radi!"}