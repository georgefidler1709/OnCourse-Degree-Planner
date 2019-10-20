#!/bin/sh
db='university.db'

sqlite3 $db < schema.sql
sqlite3 $db < setup_enums.sql

