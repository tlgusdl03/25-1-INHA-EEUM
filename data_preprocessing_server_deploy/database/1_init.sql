-- 확장 설치 (TimescaleDB 확장)
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 장소 테이블
CREATE TABLE IF NOT EXISTS locations(
  location_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  coordinates TEXT not NULL,
  uri TEXT NOT NULL
);

-- IoT 기기 테이블
CREATE TABLE IF NOT EXISTS iot_devices(
  device_id SERIAL PRIMARY KEY,
  location_id INTEGER REFERENCES locations(location_id),
  status TEXT,
  is_connected BOOLEAN,
  last_sent_at TIMESTAMP
);

-- 센서 테이블
CREATE TABLE IF NOT EXISTS sensors (
  sensor_id SERIAL PRIMARY KEY,
  device_id INTEGER REFERENCES iot_devices(device_id),
  sensor_type TEXT,
  status TEXT,
  interval_ms BIGINT,
  priority INT,
  measured_at TIMESTAMP
);

-- 센서 데이터 테이블
CREATE TABLE IF NOT EXISTS sensor_datas(
  location_id INTEGER REFERENCES locations(location_id),
  collected_at TIMESTAMP NOT NULL,
  temperature NUMERIC(8,2),
  humidity NUMERIC(8,2),
  tvoc NUMERIC(8,2),
  noise NUMERIC(8,2),
  pm10 NUMERIC(8,2),
  pm2_5 NUMERIC(8,2)
);

-- 점수 데이터 테이블
CREATE TABLE IF NOT EXISTS scores (
  score_id SERIAL PRIMARY KEY,
  location_id INTEGER REFERENCES locations(location_id),
  total_score NUMERIC(5,2),
  cai_score NUMERIC(5,2),
  discomfort_score NUMERIC(5,2),
  noise_score NUMERIC(5,2),
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports(
  report_id SERIAL PRIMARY KEY,
  location_id INTEGER REFERENCES locations(location_id),
  created_at TIMESTAMP,
  content TEXT
);

CREATE TABLE IF NOT EXISTS feedbacks (
  feedback_id SERIAL PRIMARY KEY,
  location_id INTEGER REFERENCES locations(location_id),
  created_at TIMESTAMP,
  satisfaction_score INT,
  used_for_training BOOLEAN
);

-- sensor_datas를 하이퍼테이블로 전환
SELECT create_hypertable('sensor_datas', 'collected_at', if_not_exists => TRUE);
