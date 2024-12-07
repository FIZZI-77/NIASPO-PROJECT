CREATE TABLE IF NOT EXISTS traffic_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    views INT NOT NULL
);

\copy traffic_data (date, views) FROM '/data/Thecleverprogrammer.csv' DELIMITER ',' CSV HEADER;
