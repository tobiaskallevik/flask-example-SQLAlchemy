import os
import sqlite3
import hashlib
import datetime
from sqlalchemy import create_engine, Table, MetaData, delete, select, insert, update
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash
import hashlib
from app import app

# Set up the database
with app.app_context():
    database_uri = app.config['DATABASE_URI']
    engine = create_engine(database_uri, echo=True)
    metadata = MetaData()
    metadata.bind = engine
    Session = sessionmaker(bind=engine)
    print("Database type:", engine.dialect.name)


# List all users in the database
def list_users():
    session = Session()
    users_table = Table('users', metadata, autoload_with=engine)
    result = [x.id for x in session.query(users_table).all()]
    session.close()
    return result

# Verify the user's credentials
def verify(id, pw):
    session = Session()
    users_table = Table('users', metadata, autoload_with=engine)
    user = session.query(users_table).filter_by(id=id).first()
    session.close()
    if user:
        return user.pw == hashlib.sha256(pw.encode()).hexdigest()
    return False

# Delete a user from the database
def delete_user_from_db(id):
    session = Session()
    users_table = Table('users', metadata, autoload_with=engine)
    session.execute(delete(users_table).where(users_table.c.id.__eq__(id.upper())))
    session.commit()
    session.close()

# Add a user to the database
def add_user(id, pw):
    session = Session()
    users_table = Table('users', metadata, autoload_with=engine)
    session.execute(users_table.insert().values(id=id.upper(), pw=hashlib.sha256(pw.encode()).hexdigest()))
    session.commit()
    session.close()

# Update a user's password
def read_note_from_db(id):
    session = Session()
    notes_table = Table('notes', metadata, autoload_with=engine)
    result = session.query(notes_table.c.note_id, notes_table.c.timestamp, notes_table.c.note).filter(notes_table.c.user.__eq__(id.upper())).all()
    session.close()
    return result

# Read a note from the database
def match_user_id_with_note_id(note_id):
    session = Session()
    notes_table = Table('notes', metadata, autoload_with=engine)
    result = session.query(notes_table.c.user).filter(notes_table.c.note_id.__eq__(note_id)).scalar()
    session.close()
    return result

# Write a note to the database
def write_note_into_db(id, note_to_write):
    session = Session()
    notes_table = Table('notes', metadata, autoload_with=engine)
    current_timestamp = str(datetime.datetime.now())
    session.execute(insert(notes_table).values(user=id.upper(), timestamp=current_timestamp, note=note_to_write,
                                               note_id=hashlib.sha1(
                                                   (id.upper() + current_timestamp).encode()).hexdigest()))
    session.commit()
    session.close()

# Update a note in the database
def delete_note_from_db(note_id):
    session = Session()
    notes_table = Table('notes', metadata, autoload_with=engine)
    session.execute(delete(notes_table).where(notes_table.c.note_id.__eq__(note_id)))
    session.commit()
    session.close()

# Update a note in the database
def image_upload_record(uid, owner, image_name, timestamp):
    session = Session()
    images_table = Table('images', metadata, autoload_with=engine)
    session.execute(insert(images_table).values(uid=uid, owner=owner, name=image_name, timestamp=timestamp))
    session.commit()
    session.close()

# List all images for a user
def list_images_for_user(owner):
    session = Session()
    images_table = Table('images', metadata, autoload_with=engine)
    result = (session.query(images_table.c.uid, images_table.c.timestamp, images_table.c.name)
              .filter(images_table.c.owner.__eq__(owner.upper())).all())
    session.close()
    return result

# Match a user ID with an image UID
def match_user_id_with_image_uid(image_uid):
    session = Session()
    images_table = Table('images', metadata, autoload_with=engine)
    result = session.query(images_table.c.owner).filter(images_table.c.uid.__eq__(image_uid)).scalar()
    session.close()
    return result

# Delete an image from the database
def delete_image_from_db(image_uid):
    session = Session()
    images_table = Table('images', metadata, autoload_with=engine)
    session.query(images_table).filter(images_table.c.uid.__eq__(image_uid)).delete()
    session.commit()
    session.close()


if __name__ == "__main__":
    print(list_users())
