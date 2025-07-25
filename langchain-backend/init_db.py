from db.database import engine
from db.models import Base

# Create all tables from models
Base.metadata.create_all(bind=engine)
