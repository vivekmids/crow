CREATE TABLE crow (
    rowid SERIAL,
    device_id VARCHAR(100),
    cam_id VARCHAR(100),
    date_time timestamp,
    detected_animals VARCHAR(1000),
    deterrent_type VARCHAR(100),
    soundfile_name VARCHAR(1000),
    key_name VARCHAR(1000),
    bucket_name VARCHAR(1000),
    updated BOOLEAN,
    found_something BOOLEAN
);