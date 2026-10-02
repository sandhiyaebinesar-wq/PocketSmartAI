import sqlite3
from pathlib import Path

from Backend.settings import get_settings


def connect_database():
    settings = get_settings()

    database_path = Path(settings.database_path)

    connection = sqlite3.connect(database_path)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = connect_database()

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            planner TEXT NOT NULL,
            request_data TEXT NOT NULL,
            response_data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        );
        """
    )

    connection.commit()
    connection.close()


def find_user(email):
    connection = connect_database()

    user = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email.lower().strip(),)
    ).fetchone()

    connection.close()

    return user


def find_user_by_id(user_id):
    connection = connect_database()

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    connection.close()

    return user


def create_user(email, password_hash):
    connection = connect_database()

    cursor = connection.execute(
        """
        INSERT INTO users(email, password_hash)
        VALUES (?, ?)
        """,
        (email.lower().strip(), password_hash)
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def save_recommendation(
    user_id,
    planner,
    request_data,
    response_data
):
    connection = connect_database()

    cursor = connection.execute(
        """
        INSERT INTO recommendations
        (
            user_id,
            planner,
            request_data,
            response_data
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            planner,
            request_data,
            response_data
        )
    )

    connection.commit()

    recommendation_id = cursor.lastrowid

    connection.close()

    return recommendation_id


def get_history(user_id):
    connection = connect_database()

    rows = connection.execute(
        """
        SELECT *
        FROM recommendations
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return rows