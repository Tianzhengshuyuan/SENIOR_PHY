CREATE DATABASE IF NOT EXISTS phy_senior3;
USE phy_senior3;

DROP TABLE IF EXISTS knowledge_relation;
DROP TABLE IF EXISTS knowledge_point;

CREATE TABLE knowledge_point (
    kp_id VARCHAR(20) PRIMARY KEY,
    subject_code VARCHAR(20),
    category1_code VARCHAR(20),
    category2_code VARCHAR(20),
    code VARCHAR(50),
    name VARCHAR(200),
    description VARCHAR(200),
    parent_id VARCHAR(20)
);

CREATE TABLE knowledge_relation (
    from_kp_id VARCHAR(20),
    to_kp_id VARCHAR(20),
    relation_type VARCHAR(20),
    weight DECIMAL(3,2)
);