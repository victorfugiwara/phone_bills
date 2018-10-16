DROP TABLE IF EXISTS phone_call;
DROP TABLE IF EXISTS phone_bill;

CREATE TABLE phone_call (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type INTEGER NOT NULL,
  started TIMESTAMP,
  finished TIMESTAMP,
  call_id INTEGER,
  source TEXT,
  destination TEXT,
  price REAL
);
