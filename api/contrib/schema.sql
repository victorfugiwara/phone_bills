DROP TABLE IF EXISTS phone_call;
DROP TABLE IF EXISTS phone_bill;

CREATE TABLE phone_call (
  record_id INTEGER PRIMARY KEY AUTOINCREMENT,
  record_type INTEGER NOT NULL,
  record_timestamp TIMESTAMP,
  call_identifier INTEGER,
  origin_number TEXT,
  destination_number TEXT
);

CREATE TABLE phone_bill (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  phone_number TEXT,
  period TEXT
);

CREATE TABLE phone_bill_call (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bill_call_id INTEGER,
  call_identifier INTEGER,
  destination_number TEXT,
  call_start TIMESTAMP,
  call_end TIMESTAMP,
  duration INTEGER,
  price REAL
);
