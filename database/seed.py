import uuid
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from database.models import Base, engine, SessionLocal, User, Document, DocumentChunk, Session

def seed_database():
    session = SessionLocal()
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)

        # Seed Users
        user1 = User(id=uuid.uuid4(), email="user1@example.com", password_hash="hashed_password1")
        user2 = User(id=uuid.uuid4(), email="user2@example.com", password_hash="hashed_password2")
        user3 = User(id=uuid.uuid4(), email="user3@example.com", password_hash="hashed_password3")
        session.add_all([user1, user2, user3])
        session.commit()

        # Seed Documents
        document1 = Document(id=uuid.uuid4(), user_id=user1.id, filename="doc1.pdf", status="processed")
        document2 = Document(id=uuid.uuid4(), user_id=user2.id, filename="doc2.docx", status="processing")
        document3 = Document(id=uuid.uuid4(), user_id=user3.id, filename="doc3.txt", status="failed")
        session.add_all([document1, document2, document3])
        session.commit()

        # Seed DocumentChunks
        chunk1 = DocumentChunk(id=uuid.uuid4(), document_id=document1.id, content="Chunk 1 content", chunk_index=0, embedding=[0.1, 0.2, 0.3])
        chunk2 = DocumentChunk(id=uuid.uuid4(), document_id=document1.id, content="Chunk 2 content", chunk_index=1, embedding=[0.4, 0.5, 0.6])
        chunk3 = DocumentChunk(id=uuid.uuid4(), document_id=document2.id, content="Chunk 1 content", chunk_index=0, embedding=[0.7, 0.8, 0.9])
        session.add_all([chunk1, chunk2, chunk3])
        session.commit()

        # Seed Sessions
        session1 = Session(id=uuid.uuid4(), user_id=user1.id, token="token1", created_at=datetime.utcnow(), expires_at=datetime.utcnow() + timedelta(days=1))
        session2 = Session(id=uuid.uuid4(), user_id=user2.id, token="token2", created_at=datetime.utcnow(), expires_at=datetime.utcnow() + timedelta(days=1))
        session3 = Session(id=uuid.uuid4(), user_id=user3.id, token="token3", created_at=datetime.utcnow(), expires_at=datetime.utcnow() + timedelta(days=1))
        session.add_all([session1, session2, session3])
        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()