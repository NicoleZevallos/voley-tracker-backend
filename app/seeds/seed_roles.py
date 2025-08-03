from app.database import SessionLocal
from app.models.role import Role

def seed_roles():
    db = SessionLocal()
    try:
        roles = ["admin", "coach", "player"]
        for role_name in roles:
            existing = db.query(Role).filter_by(name=role_name).first()
            if not existing:
                db.add(Role(name=role_name))
        db.commit()
    finally:
        db.close()