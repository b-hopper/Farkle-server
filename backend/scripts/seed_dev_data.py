# backend/scripts/seed_dev_data.py
import uuid
from datetime import datetime
from backend.database import SessionLocal, engine
from backend.models import Base, User, PlayerProfile, Game, GameResult

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def seed():
    user_id = str(uuid.uuid4())
    user = User(user_id=user_id, login_type="anonymous")
    db.add(user)

    player_ids = []
    for name in ["Alice", "Bob"]:
        pid = str(uuid.uuid4())
        player_ids.append(pid)
        profile = PlayerProfile(
            player_id=pid,
            user_id=user_id,
            display_name=name,
        )
        db.add(profile)

    game_id = str(uuid.uuid4())
    game = Game(game_id=game_id, user_id=user_id, played_at=datetime.utcnow())
    db.add(game)

    result1 = GameResult(
        result_id=str(uuid.uuid4()),   # Add this line
        game_id=game_id,
        player_id=player_ids[0],
        score=9800,
        turns_taken=8,
        farkles=1,
        won=True
    )
    result2 = GameResult(
        result_id=str(uuid.uuid4()),   # Add this line
        game_id=game_id,
        player_id=player_ids[1],
        score=8700,
        turns_taken=9,
        farkles=3,
        won=False
    )

    db.add_all([result1, result2])
    db.commit()
    print("Seeded dev data with players and game session.")

if __name__ == "__main__":
    seed()
