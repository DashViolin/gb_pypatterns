
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS student;
CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));

DROP TABLE IF EXISTS category;
CREATE TABLE category (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), parent_id INTEGER);

DROP TABLE IF EXISTS course;
CREATE TABLE course (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), category_id INTEGER);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
