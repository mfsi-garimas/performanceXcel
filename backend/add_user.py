from app.db.init_db import SessionLocal, Base, engine
from app.models.user import User
from app.utils.security import hash_password  # make sure you have this function

# ⚡ Create tables if not yet created
Base.metadata.create_all(bind=engine)

# Create a new DB session
db = SessionLocal()

# Define user credentials
email = "testuser3@example.com"
password = "Test1234!"  # plain password
role="ADMIN"

# Hash the password
hashed_pw = hash_password(password)

# Check if user already exists
existing_user = db.query(User).filter(User.email == email).first()
if existing_user:
    print(f"User with email {email} already exists")
else:
    # Create user object
    user = User(
        email=email,
        hashed_password=hashed_pw,
        role=role
    )

    # Add to DB
    db.add(user)
    db.commit()
    print(f"User {email} created successfully ✅")

# Close session
db.close()