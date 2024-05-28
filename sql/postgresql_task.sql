-- extension is necessary for using both = and && in exclude constraint
CREATE EXTENSION btree_gist;
-- I have separated the fqdns and flags from the requested tables to avoid issues with later alters or deletes
CREATE TABLE domain_fqdn (fqdn_id SERIAL PRIMARY KEY,
                     	  fqdn VARCHAR(100) UNIQUE NOT NULL
                     	  );
CREATE TABLE "domain" (domain_id BIGSERIAL PRIMARY KEY,
                       fqdn_id INT REFERENCES domain_fqdn(fqdn_id) ON DELETE CASCADE,
                       registered_from TIMESTAMP NOT NULL,
                       registered_to TIMESTAMP,
                       CHECK (registered_from < registered_to),
                       EXCLUDE USING gist (fqdn_id WITH =, tsrange(registered_from, registered_to) WITH &&)
                       );
CREATE TABLE domain_flag_name (flag_name_id SERIAL PRIMARY KEY,
                               flag_name VARCHAR(50) UNIQUE NOT NULL
                               );
-- I don't think it is possible to forbid setting 'flagged_to' to the past using constraints
-- as it will cause problems when restoring the database from dump.
-- It could be solved using a custom trigger.
CREATE TABLE domain_flag (domain_flag_id BIGSERIAL PRIMARY KEY,
                          fqdn_id INT REFERENCES domain_fqdn(fqdn_id) ON DELETE CASCADE,
                          flag_name_id INT REFERENCES domain_flag_name(flag_name_id) ON DELETE CASCADE,
                          flagged_from TIMESTAMP NOT NULL,
                          flagged_to TIMESTAMP,
                          CHECK (flagged_from < flagged_to),
                          EXCLUDE USING gist (fqdn_id WITH =, flag_name_id WITH =, tsrange(flagged_from, flagged_to) WITH &&)
                          );
-- I assumed domain flag intervals to be related to domains and not domain registration intervals as it is not clear from the assignment.

-- test data
INSERT INTO domain_fqdn (fqdn) VALUES ('fqdn1'),('fqdn2'),('fqdn3');
INSERT INTO "domain" (fqdn_id, registered_from, registered_to)
	VALUES (1, '2000-01-01 00:00:00', '2000-01-02 00:00:00'),
    	   (1, '2001-01-01 00:00:00', NULL),
    	   (2, '2000-01-01 00:00:00', '2000-01-02 00:00:00'),
           (2, '2000-01-03 00:00:00', '2000-01-04 00:00:00'),
           (2, '2000-01-05 00:00:00', '2000-01-06 00:00:00'),
           (3, '2000-01-01 00:00:00', NULL);

INSERT INTO domain_flag_name (flag_name) VALUES ('EXPIRED'),('OUTZONE'),('DELETE_CANDIDATE');
INSERT INTO domain_flag (fqdn_id, flag_name_id, flagged_from, flagged_to)
	VALUES (1, 3, '2021-01-01 00:00:00', NULL),
    	   (1, 1, '2024-01-01 00:00:00', '2024-05-01 00:00:00'),
           (2, 1, '2000-01-01 00:00:00', '2000-01-02 00:00:00'),
           (2, 2, '2000-01-01 00:00:00', '2000-01-02 00:00:00'),
           (3, 2, '2000-01-01 00:00:00', '2000-01-02 00:00:00'),
           (3, 1, '2024-01-01 00:00:00', NULL);

-- selects
-- 1
SELECT DISTINCT domain_fqdn.fqdn FROM "domain" AS dom
JOIN domain_fqdn ON dom.fqdn_id=domain_fqdn.fqdn_id
JOIN domain_flag ON dom.fqdn_id=domain_flag.fqdn_id
JOIN domain_flag_name ON domain_flag.flag_name_id=domain_flag_name.flag_name_id
WHERE dom.registered_from < CURRENT_TIMESTAMP AND (dom.registered_to IS NULL OR dom.registered_to > CURRENT_TIMESTAMP)
AND domain_flag.flagged_from < CURRENT_TIMESTAMP AND (domain_flag.flagged_to IS NULL OR domain_flag.flagged_to > CURRENT_TIMESTAMP)
AND domain_flag_name.flag_name != 'EXPIRED';

-- 2
SELECT domain_fqdn.fqdn FROM domain_flag
JOIN domain_flag_name ON domain_flag.flag_name_id=domain_flag_name.flag_name_id
JOIN domain_fqdn ON domain_flag.fqdn_id=domain_fqdn.fqdn_id
WHERE domain_flag.flagged_to < CURRENT_TIMESTAMP AND domain_flag_name.flag_name IN ('EXPIRED', 'OUTZONE')
GROUP BY domain_fqdn.fqdn
HAVING COUNT(DISTINCT domain_flag_name.flag_name)=2;