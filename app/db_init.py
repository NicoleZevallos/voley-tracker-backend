from app.database import engine
from app.models import user, role

def init_db():
    role.Base.metadata.create_all(bind=engine)
    user.Base.metadata.create_all(bind=engine)
