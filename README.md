# Introduction

(wip)

This is a CLI tool which creates services from data structures. A variety of databases and services are supported. For example, if you want a gRPC service with postgres, then you supply the cli tool with an .sql file with a "create table xyz" inside the schematics folder. The tool will then generate a basic application with some CRUD routes. Tests included.

## Pre-usage

If I haven't uploaded snoozelib to pypi yet(lack of confidense in project quality), then you need to build snoozelib first. In snoozelib directory:

> poetry build

## Usage

1. Open a terminal and cd to the directory you want to work in
2. In your terminal: snoozebox init
3. Make a directory inside the schematics folder. E.g.: "example"
4. Make a .sql file inside the newly created directory. E.g.: "person.sql"
5. Write a "create table" sequence. E.g.:
    > CREATE TABLE IF NOT EXISTS person(
    > 	id SERIAL NOT NULL,
    > 	name VARCHAR(255) NOT NULL
    > );
6. CD back to the main directory. The same directory where you can see "schematics", "services", "snoozefile.toml" and "docker-compose.yml"
7. In your terminal: snoozebox append
8. Make your choices
9. Done


## Requirements

Poetry: https://python-poetry.org/

Docker: https://www.docker.com/

### Requirements Depending On Tech Choices

Postgres libaries. Check: https://www.psycopg.org/install/

## Acknowledgements

Snoozelib is *very* primitive.
