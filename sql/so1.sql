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
);;

INSERT INTO knowledge_point (kp_id, subject_code, category1_code, category2_code, code, name, description, parent_id)
VALUES
('01010601000000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH01', '动量守恒定律', '', NULL),
('01010601010000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH01.SEC01', '动量', '', '01010601000000'),
('01010601020000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH01.SEC02', '动量定理', '', '01010601000000'),
('01010601030000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH01.SEC03', '动量守恒定律', '', '01010601000000'),
('01010601040000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH01.SEC04', '实验：验证动量守恒定律', '', '01010601000000'),
('01010601050000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH01.SEC05', '弹性碰撞和非弹性碰撞', '', '01010601000000'),
('01010601060000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH01.SEC06', '反冲现象  火箭', '', '01010601000000');

INSERT INTO knowledge_point (kp_id, subject_code, category1_code, category2_code, code, name, description, parent_id)
VALUES
('01010602000000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH02', '机械振动', '', NULL),
('01010602010000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH02.SEC01', '简谐运动', '', '01010602000000'),
('01010602020000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH02.SEC02', '简谐运动的描述', '', '01010602000000'),
('01010602030000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH02.SEC03', '简谐运动的回复力和能量', '', '01010602000000'),
('01010602040000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH02.SEC04', '单摆', '', '01010602000000'),
('01010602050000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH02.SEC05', '实验：用单摆测量重力加速度', '', '01010602000000'),
('01010602060000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH02.SEC06', '受迫振动  共振', '', '01010602000000');

INSERT INTO knowledge_point (kp_id, subject_code, category1_code, category2_code, code, name, description, parent_id)
VALUES
('01010603000000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH03', '机械波', '', NULL),
('01010603010000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH03.SEC01', '波的形成', '', '01010603000000'),
('01010603020000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH03.SEC02', '波的描述', '', '01010603000000'),
('01010603030000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH03.SEC03', '波的反射、折射和衍射', '', '01010603000000'),
('01010603040000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH03.SEC04', '波的干涉', '', '01010603000000'),
('01010603050000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH03.SEC05', '多普勒效应', '', '01010603000000');

INSERT INTO knowledge_point (kp_id, subject_code, category1_code, category2_code, code, name, description, parent_id)
VALUES
('01010604000000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH04', '光', '', NULL),
('01010604010000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH04.SEC01', '光的折射', '', '01010604000000'),
('01010604020000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH04.SEC02', '全反射', '', '01010604000000'),
('01010604030000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH04.SEC03', '光的干涉', '', '01010604000000'),
('01010604040000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH04.SEC04', '实验：用双缝干涉测量光的波长', '', '01010604000000'),
('01010604050000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH04.SEC05', '光的衍射', '', '01010604000000'),
('01010604060000', 'PHYSICS', 'SENIOR', 'TERM_6', 'CH04.SEC06', '光的偏振  激光', '', '01010604000000');

