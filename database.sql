CREATE TABLE IF NOT EXISTS urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255) UNIQUE NOT NULL,
    created_at date NOT NULL
);


CREATE TABLE IF NOT EXISTS url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    status_code integer,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at date,
    url_id bigint REFERENCES urls (id)
);
