# delete_users.py
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User

db: Session = next(get_db())  # get a DB session

# delete a specific user
user = db.query(User).filter(User.email == "angweteryila@gmail.com").first()
if user:
    db.delete(user)
    db.commit()
    print("User deleted successfully")
else:
    print("User not found")
