import os
from app import app, db, User, Entry, bcrypt

with app.app_context():
    # Create a test user
    test_email = "test@example.com"
    existing = User.query.filter_by(email=test_email).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
    
    hashed = bcrypt.generate_password_hash("password").decode('utf-8')
    u = User(username="testuser", email=test_email, hashed_password=hashed)
    db.session.add(u)
    db.session.commit()
    
    # Create an entry
    e = Entry(title="Test Entry", content="Hello world", owner_id=u.id)
    db.session.add(e)
    db.session.commit()
    
    print(f"Created user ID: {u.id}")
    print(f"Created entry ID: {e.id}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
