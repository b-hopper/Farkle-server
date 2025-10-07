# backend/tests/test_endpoints.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_player():
    res = client.post("/create-player", json={
        "user_id": "test-user-1",
        "display_name": "Tester"
    })
    assert res.status_code == 200
    assert "player_id" in res.json()
    
def test_delete_player():
    res = client.post("/create-player", json={
        "user_id": "test-user-1",
        "display_name": "ToDelete"
    })
    player_id = res.json()["player_id"]
    del_res = client.post("/delete-player", params={"player_id": player_id})
    assert del_res.status_code == 200

def test_post_game_result():
    # Create user and player
    user_id = "test-user-2"
    player_res = client.post("/create-player", json={
        "user_id": user_id,
        "display_name": "Player1"
    })
    player_id = player_res.json()["player_id"]

    # Submit game result
    game_res = client.post("/game-result", json={
        "user_id": user_id,
        "results": [{
            "player_id": player_id,
            "score": 10000,
            "turns": 9,
            "farkles": 2,
            "won": True
        }]
    })
    assert game_res.status_code == 200
    assert "game_id" in game_res.json()
