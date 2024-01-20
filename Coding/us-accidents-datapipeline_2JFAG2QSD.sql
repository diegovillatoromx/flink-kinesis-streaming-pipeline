%flink.ssql

/* Opción 'IF NOT EXISTS' puede usarse para proteger el esquema existente */
DROP TABLE IF EXISTS us_accidents_stream;

CREATE TABLE us_accidents_stream (
  `ID` VARCHAR(50), 
  `Severity` BIGINT, 
  `Start_Time` TIMESTAMP(3), 
  `End_Time` TIMESTAMP(3), 
  `Start_Lat` VARCHAR(50), 
  `Start_Lng` VARCHAR(50), 
  `End_Lat` VARCHAR(50), 
  `End_Lng` VARCHAR(50), 
  `Distance(mi)` VARCHAR(50), 
  `Description` VARCHAR(500), 
  `Number` VARCHAR(50), 
  `Street` VARCHAR(50), 
  `Side` VARCHAR(50), 
  `City` VARCHAR(50), 
  `County` VARCHAR(50), 
  `State` VARCHAR(50), 
  `Zipcode` VARCHAR(50), 
  `Country` VARCHAR(50), 
  `Timezone` VARCHAR(50), 
  `Airport_Code` VARCHAR(50), 
  `Weather_Timestamp` TIMESTAMP(3), 
  `Temperature(F)` VARCHAR(50), 
  `Wind_Chill(F)` VARCHAR(50), 
  `Humidity(%)` VARCHAR(50), 
  `Pressure(in)` VARCHAR(50), 
  `Visibility(mi)` VARCHAR(50), 
  `Wind_Direction` STRING, 
  `Wind_Speed(mph)` VARCHAR(50), 
  `Precipitation(in)` VARCHAR(50), 
  `Weather_Condition` VARCHAR(50), 
  `Amenity` VARCHAR(50), 
  `Bump` BOOLEAN, 
  `Crossing` BOOLEAN, 
  `Give_Way` BOOLEAN, 
  `Junction` BOOLEAN, 
  `No_Exit` BOOLEAN, 
  `Railway` BOOLEAN, 
  `Roundabout` BOOLEAN, 
  `Station` BOOLEAN, 
  `Stop` BOOLEAN, 
  `Traffic_Calming` BOOLEAN, 
  `Traffic_Signal` BOOLEAN, 
  `Turning_Loop` BOOLEAN, 
  `Sunrise_Sunset` VARCHAR(50), 
  `Civil_Twilight` VARCHAR(50), 
  `Nautical_Twilight` VARCHAR(50), 
  `Astronomical_Twilight` VARCHAR(50),
  `Txn_Timestamp` TIMESTAMP(3),
  WATERMARK FOR Txn_Timestamp AS Txn_Timestamp - INTERVAL '5' SECOND  
)
PARTITIONED BY (Severity)
WITH (
  'connector' = 'kinesis',
  'stream' = 'us-accidents-data-stream-1',
  'aws.region' = 'us-east-1',
  'scan.stream.initpos' = 'LATEST',
  'format' = 'json',
  'json.timestamp-format.standard' = 'ISO-8601'
);

/* Opción 'IF NOT EXISTS' puede usarse para proteger el esquema existente */
DROP TABLE IF EXISTS us_accidents_stream_1_results;

CREATE TABLE us_accidents_stream_1_results (
  `ID` VARCHAR(50), 
  `Severity` BIGINT, 
  `City` VARCHAR(50), 
  `County` VARCHAR(50), 
  `Txn_Timestamp` TIMESTAMP(3)
)
PARTITIONED BY (Severity)
WITH (
  'connector' = 'kinesis',
  'stream' = 'us-accidents-data-stream-2',
  'aws.region' = 'us-east-1',
  'format' = 'json',
  'json.timestamp-format.standard' = 'ISO-8601'
);

INSERT INTO us_accidents_stream_1_results
SELECT ID, Severity, City, County, Txn_Timestamp
FROM us_accidents_stream WHERE Severity > 2;

