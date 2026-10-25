CREATE TABLE IF NOT EXISTS users (
    id    INTEGER PRIMARY KEY,
    name  TEXT    NOT NULL,
    email TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS couriers (
    id                     INTEGER PRIMARY KEY,
    name                   TEXT    NOT NULL,
    phone                  TEXT    NOT NULL,
    vehicle                TEXT    NOT NULL,
    departure_date         TEXT    NOT NULL,
    expected_delivery_date TEXT    NOT NULL,
    capacity_kg            REAL    NOT NULL,
    is_available           INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS packages (
    id             INTEGER PRIMARY KEY,
    category       TEXT    NOT NULL,
    departure_date TEXT    NOT NULL,
    arrival_date   TEXT    NOT NULL,
    weight         REAL    NOT NULL,
    status         TEXT    NOT NULL,
    sender_id      INTEGER,
    recipient_id   INTEGER,
    courier_id     INTEGER,
    FOREIGN KEY (sender_id)    REFERENCES users(id),
    FOREIGN KEY (recipient_id) REFERENCES users(id),
    FOREIGN KEY (courier_id)   REFERENCES couriers(id)
);