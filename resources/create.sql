CREATE TABLE IF NOT EXISTS modbus
(
    id          BIGSERIAL PRIMARY KEY,
    server_num  SMALLINT NOT NULL,
    reg_addr    INTEGER NOT NULL,
    value       REAL NOT NULL
);
