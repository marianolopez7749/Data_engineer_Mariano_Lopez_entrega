-- marianolopez7749_coderhouse.races_1 definition

-- Drop table

-- DROP TABLE marianolopez7749_coderhouse.races_1;

--DROP TABLE marianolopez7749_coderhouse.races_1;
CREATE TABLE IF NOT EXISTS marianolopez7749_coderhouse.races_1
(
	raceid INTEGER NOT NULL  ENCODE az64
	,"year" INTEGER NOT NULL  ENCODE az64
	,round INTEGER NOT NULL  ENCODE az64
	,circuitid INTEGER NOT NULL  ENCODE az64
	,name VARCHAR(256) NOT NULL  ENCODE lzo
	,date DATE NOT NULL  ENCODE az64
	,"time" TIME WITHOUT TIME ZONE NOT NULL  ENCODE az64
	,url VARCHAR(256)   ENCODE lzo
	,fp1_date DATE   ENCODE az64
	,fp1_time TIME WITHOUT TIME ZONE   ENCODE az64
	,fp2_date DATE   ENCODE az64
	,fp2_time TIME WITHOUT TIME ZONE   ENCODE az64
	,fp3_date DATE   ENCODE az64
	,fp3_time TIME WITHOUT TIME ZONE   ENCODE az64
	,quali_date DATE   ENCODE az64
	,quali_time TIME WITHOUT TIME ZONE   ENCODE az64
	,sprint_date DATE   ENCODE az64
	,sprint_time TIME WITHOUT TIME ZONE   ENCODE az64
)
DISTSTYLE AUTO
;
ALTER TABLE marianolopez7749_coderhouse.races_1 owner to marianolopez7749_coderhouse;