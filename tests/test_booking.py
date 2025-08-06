import os
import sqlite3
import argparse
from datetime import datetime, timedelta
import pytest

import booking.db as db_module
from booking import cli


@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_booking.db"
    monkeypatch.setattr(db_module, "DB_PATH", str(db_file))
    db_module.init_db()
    return db_file


def test_init_db_creates_rooms(tmp_db):
    conn = sqlite3.connect(tmp_db)
    cur = conn.execute("SELECT name FROM rooms ORDER BY id")
    rooms = [row[0] for row in cur.fetchall()]
    assert rooms == [f"Cabinet {i}" for i in range(1, 6)]


def test_is_free_and_add_booking(tmp_db):
    room_id = 1
    now = datetime.now()
    start = now
    end = now + timedelta(hours=1)

    assert db_module.is_free(room_id, start, end)

    db_module.add_booking(room_id, "User", "u@example.com", "123", start, end)
    assert not db_module.is_free(room_id, start, end)

    assert not db_module.is_free(
        room_id,
        start + timedelta(minutes=30),
        end + timedelta(minutes=30)
    )

    assert db_module.is_free(
        room_id,
        start - timedelta(hours=2),
        start - timedelta(hours=1)
    )
    assert db_module.is_free(
        room_id,
        end + timedelta(hours=1),
        end + timedelta(hours=2)
    )


def test_get_current_booking(tmp_db):
    room_id = 2
    now = datetime.now()
    start = now
    end = now + timedelta(hours=2)

    db_module.add_booking(room_id, "Alice", "a@b.com", "111", start, end)
    b = db_module.get_current_booking(
        room_id,
        start + timedelta(minutes=30),
        end + timedelta(minutes=30)
    )
    assert b["user_name"] == "Alice"
    assert b["email"] == "a@b.com"


def run_check(room, start, end, capsys):
    args = argparse.Namespace(room=room, start=start, end=end)
    cli.check(args)
    out = capsys.readouterr().out.strip()
    return out


def test_cli_check_free(tmp_db, capsys):
    room = 3
    now = datetime.now()
    start = now.strftime(cli.DATE_FMT)
    end = (now + timedelta(hours=1)).strftime(cli.DATE_FMT)

    out = run_check(room, start, end, capsys)
    assert f"Кабинет {room} свободен" in out


def test_cli_book_and_then_check(tmp_db, capsys, monkeypatch):
    monkeypatch.setattr(cli, "send_email", lambda *a, **k: None)
    monkeypatch.setattr(cli, "send_sms", lambda *a, **k: None)

    room = 4
    now = datetime.now()
    start = now.strftime(cli.DATE_FMT)
    end = (now + timedelta(hours=1)).strftime(cli.DATE_FMT)

    book_args = argparse.Namespace(
        room=room,
        start=start,
        end=end,
        user="Bob",
        email="b@e.com",
        phone="321"
    )
    cli.book(book_args)
    booked_out = capsys.readouterr().out
    assert f"Кабинет {room} успешно забронирован" in booked_out

    out2 = run_check(room, start, end, capsys)
    assert "занят" in out2
