-- Enforce foreign keys
PRAGMA foreign_keys = ON;

-- ============================================================
-- Vehicle: one row per car you track
-- ============================================================
CREATE TABLE IF NOT EXISTS Vehicle (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    vin         VARCHAR(17) UNIQUE,           -- 17 alphanumeric chars; UNIQUE prevents duplicates
    year        INTEGER NOT NULL,
    make        TEXT NOT NULL,
    model       TEXT NOT NULL,
    trim        TEXT,
    engineSize  TEXT,                          -- e.g. "2.5L", "5.7L V8"
    nickname    TEXT,
    createdAt   TEXT DEFAULT (datetime('now')),
    updatedAt   TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- ServiceRecord: one row per service visit (the "invoice header")
-- ============================================================
CREATE TABLE IF NOT EXISTS ServiceRecord (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicleId       INTEGER NOT NULL,
    serviceDate     TEXT NOT NULL,             -- ISO 8601 format: "2026-05-26"
    mileage         INTEGER NOT NULL,
    isDiy           INTEGER NOT NULL DEFAULT 1, -- SQLite has no real BOOLEAN; use 0/1
    serviceCenter   TEXT,                       -- nullable; only set if isDiy = 0
    totalCost       INTEGER,                    -- stored in cents to avoid float errors
    notes           TEXT,
    createdAt       TEXT DEFAULT (datetime('now')),
    updatedAt       TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (vehicleId) REFERENCES Vehicle(id) ON DELETE CASCADE
);
-- ============================================================
-- ServiceLineItem: individual services done during a ServiceRecord
-- (the "invoice line items")
-- ============================================================
CREATE TABLE IF NOT EXISTS ServiceLineItem (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    serviceRecordId   INTEGER NOT NULL,
    serviceType       TEXT NOT NULL,            -- e.g. "Oil Change", "Brake Pads"
    productUsed       TEXT,                      -- e.g. "Mobil 1 5W-30 EP"
    quantity          INTEGER DEFAULT 1,
    cost              INTEGER,                   -- cents
    notes             TEXT,
    createdAt         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (serviceRecordId) REFERENCES ServiceRecord(id) ON DELETE CASCADE
);