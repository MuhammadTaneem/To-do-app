

CREATE TABLE "user" (
    id SERIAL4 PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    password VARCHAR,
    address VARCHAR,
    email VARCHAR,
    active BOOLEAN DEFAULT FALSE
);

CREATE TABLE "user_token" (
    id SERIAL PRIMARY KEY,
    author INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
    token VARCHAR,
    expire TIMESTAMP,
    used BOOLEAN DEFAULT FALSE
);

CREATE TABLE "page" (
    id SERIAL4 PRIMARY KEY,
    author INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
    parent_page_id INTEGER DEFAULT 0,
    page_name VARCHAR DEFAULT 'Unnamed',
    page_description VARCHAR,
    color VARCHAR,
    create_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
    last_edit TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    author INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
    page_id INTEGER REFERENCES page (id) ON DELETE CASCADE,
    task_name VARCHAR DEFAULT 'Unnamed',
    task_description VARCHAR,
    status VARCHAR,
    create_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_edit TIMESTAMP WITH TIME ZONE
);
