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
