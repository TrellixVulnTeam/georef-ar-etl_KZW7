CREATE OR REPLACE FUNCTION get_municipality(code_bahra TEXT, OUT result TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
  SELECT m.in1
  INTO result
  FROM ign_municipios m, ign_bahra b
  WHERE st_contains(m.geom, b.geom)
        AND b.cod_bahra = code_bahra;
  EXCEPTION WHEN OTHERS
    THEN
      result := SQLERRM;
END;
$$;


CREATE OR REPLACE FUNCTION update_entities_data()
  RETURNS BOOLEAN
STRICT
LANGUAGE plpgsql
AS $$
BEGIN
  IF (
      SELECT count(table_name)
      FROM information_schema.tables
      WHERE table_schema = 'public'
           AND table_name IN (
             'ign_pais_tmp',
             'ign_provincias_tmp',
             'ign_departamentos_tmp',
             'ign_municipios_tmp',
             'ign_bahra_tmp'
           )
  ) = 5
  THEN
    DROP TABLE IF EXISTS ign_pais CASCADE;
    DROP TABLE IF EXISTS ign_provincias CASCADE;
    DROP TABLE IF EXISTS ign_departamentos CASCADE;
    DROP TABLE IF EXISTS ign_municipios CASCADE;
    DROP TABLE IF EXISTS ign_bahra CASCADE;

    ALTER TABLE IF EXISTS ign_pais_tmp RENAME TO ign_pais;
    ALTER TABLE IF EXISTS ign_provincias_tmp RENAME TO ign_provincias;
    ALTER TABLE IF EXISTS ign_departamentos_tmp RENAME TO ign_departamentos;
    ALTER TABLE IF EXISTS ign_municipios_tmp RENAME TO ign_municipios;
    ALTER TABLE IF EXISTS ign_bahra_tmp RENAME TO ign_bahra;

    ALTER INDEX IF EXISTS ign_pais_tmp_geom_geom_idx RENAME TO ign_pais_geom_geom_idx;
    ALTER INDEX IF EXISTS ign_provincias_tmp_geom_geom_idx RENAME TO ign_provincias_geom_geom_idx;
    ALTER INDEX IF EXISTS ign_departamentos_tmp_geom_geom_idx RENAME TO ign_departamentos_geom_geom_idx;
    ALTER INDEX IF EXISTS ign_municipios_tmp_geom_geom_idx RENAME TO ign_municipios_geom_geom_idx;
    ALTER INDEX IF EXISTS ign_bahra_tmp_geom_geom_idx RENAME TO ign_bahra_geom_geom_idx;
    RETURN TRUE;
  ELSE
    RETURN FALSE;
  END IF;
  EXCEPTION WHEN OTHERS
  THEN
    RAISE NOTICE 'Se produjo el siguiente error: % (%)', SQLERRM, SQLSTATE;
    RETURN FALSE;
END
$$;


CREATE OR REPLACE FUNCTION get_percentage_intersection_state(geom_entity GEOMETRY, code_state VARCHAR)
   RETURNS FLOAT
STRICT
LANGUAGE plpgsql
AS $$
 DECLARE
  result FLOAT;
BEGIN
  SELECT
    round((st_area(st_intersection(t2.geom, geom_entity)) / st_area(t2.geom))::NUMERIC, 6) INTO result
  FROM (
    SELECT p.nam, p.geom
    FROM ign_provincias p
    WHERE p.in1 = code_state
  ) t2;
  RETURN result;
END
$$;