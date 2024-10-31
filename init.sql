CREATE DATABASE backend_app;

CREATE DATABASE public_api_data;

\connect public_api_data;

CREATE TABLE IF NOT EXISTS record_metadata (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255),
    mongo_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
