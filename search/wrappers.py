# -*- coding: utf-8 -*-

from search.models import *
import json
import psycopg2
import requests


class PostgresWrapper:
    def search_address(self, address):
        connection = psycopg2.connect(
            dbname="georef", user="postgres", password="postgres")
        parts = address.split(',')
        with connection.cursor() as cursor:
            query = "SELECT tipo_camino || ' ' || nombre_completo || ', ' \
                        || localidad || ', ' || provincia AS addr \
                        FROM nombre_calles "
            if len(parts) > 1:
                query += "WHERE nombre_completo ILIKE '%(road)s%%' \
                        AND localidad ILIKE '%%%(locality)s%%'" % {
                            'road': parts[0].strip(),
                            'locality': parts[1].strip()}
            else:
                query += "WHERE nombre_completo ILIKE '%s%%'" % (address)
            query += " LIMIT 10"
            cursor.execute(query)
            results = cursor.fetchall()
        
        return json.dumps([row[0] for row in results])
