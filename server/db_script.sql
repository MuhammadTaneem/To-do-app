-- CREATE TABLE "user" (
--     id SERIAL4 PRIMARY KEY,
--     first_name VARCHAR,
--     last_name VARCHAR,
--     password VARCHAR,
--     address VARCHAR,
--     email VARCHAR
-- );

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
    author INTEGER REFERENCES "user" (id),
    token VARCHAR,
    expire TIMESTAMP,
    used BOOLEAN DEFAULT FALSE
);


-- user_token_table = Table(
--     "user_token",  mapper_registry.metadata,
--     Column('id', Integer, primary_key=True),
--     Column('author', Integer, ForeignKey('user.id')),
--     Column('reset_token', String),
--     Column('expire', DateTime),
--     Column('used', Boolean, default=False)
-- )



CREATE TABLE "page" (
    id SERIAL4 PRIMARY KEY,
    author INTEGER REFERENCES "user" (id),
    parent_page_id INTEGER DEFAULT 0,
    page_name VARCHAR,
    page_description VARCHAR,
    color VARCHAR,
    create_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
    last_edit TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE "task" (
    id SERIAL PRIMARY KEY,
    author INTEGER REFERENCES "user" (id),
    page_id INTEGER REFERENCES page (id),
    task_name VARCHAR,
    task_description VARCHAR,
    status VARCHAR,
    create_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
    last_edit TIMESTAMP WITH TIME ZONE DEFAULT now()
);