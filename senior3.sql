CREATE DATABASE IF NOT EXISTS phy_senior3;
USE phy_senior3;

DROP TABLE IF EXISTS knowledge_relation;
DROP TABLE IF EXISTS knowledge_point;

CREATE TABLE knowledge_point (
    kp_id VARCHAR(20) PRIMARY KEY,
    subject_code VARCHAR(20),
    stage_code VARCHAR(20),
    grade_code VARCHAR(20),
    term_code VARCHAR(20),
    code_path VARCHAR(255),
    code VARCHAR(50),
    name VARCHAR(100),
    description VARCHAR(255),
    is_core TINYINT,
    is_extend TINYINT,
    is_olympics TINYINT,
    difficulty DECIMAL(3,2),
    parent_id VARCHAR(20)
);

CREATE TABLE knowledge_relation (
    from_kp_id VARCHAR(20),
    to_kp_id VARCHAR(20),
    relation_type VARCHAR(20),
    weight DECIMAL(3,2)
);

-- 知识点表插入（第一章 分子动理论）✅
-- 章节 CH01 (4核心+0扩展+0奥赛)
INSERT INTO knowledge_point (kp_id, subject_code, stage_code, grade_code, term_code, code_path, code, name, description, is_core, is_extend, is_olympics, difficulty, parent_id) 
VALUES 
('2401000000', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2', 'CH01', '分子动理论', '分子动理论基本框架', 1, 0, 0, 0.60, NULL);

-- 小节 CH01.SEC01 (3核心+1扩展+1奥赛)
INSERT INTO knowledge_point (kp_id, subject_code, stage_code, grade_code, term_code, code_path, code, name, description, is_core, is_extend, is_olympics, difficulty, parent_id) 
VALUES 
('2401010000', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01', '分子动理论的基本内容', '分子模型与统计规律', 1, 0, 0, 0.65, '2401000000'),

('2401010100', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01', '分子热运动与扩散现象', '布朗运动与分子热运动的实验验证', 1, 0, 0, 0.70, '2401010000'),
('2401010200', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP02', '分子间相互作用力', '分子力曲线与势能变化分析', 1, 0, 1, 0.85, '2401010000'),
('2401010300', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP03', '理想气体分子模型', '理想气体假设与真实气体修正（扩展）', 0, 1, 0, 0.75, '2401010000'),

('2401010101', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01.Q01', '正确', '液体中悬浮微粒的布朗运动是作无规则运动的液体分子撞击微粒而引起的', 0, 0, 0, 1, '2401010100'),
('2401010102', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01.Q02', '错误', '布朗运动是悬浮在液体中固体颗粒内分子的无规则运动', 0, 0, 0, 1, '2401010100'),
('2401010103', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01.Q03', '正确', '液体中悬浮的微粒的无规则运动称为布朗运动', 0, 0, 0, 1, '2401010100'),
('2401010104', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01.Q04', '错误', '液体分子的无规则运动称为布朗运动', 0, 0, 0, 1, '2401010100'),
('2401010105', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01.Q05', '错误', '布朗运动是由于液体各部分的温度不同而引起的', 0, 0, 0, 1, '2401010100'),
('2401010106', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01.Q06', '正确', '布朗运动是由液体分子从各个方向对悬浮粒子撞击作用的不平衡引起的', 0, 0, 0, 1, '2401010100'),
('2401010107', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01.Q07', '正确', '扩散是指不同物质能够彼此进入对方', 0, 0, 0, 1, '2401010100'),
('2401010108', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01.Q08', '正确', '扩散的一个应用是在生产半导体器件时，向纯净半导体材料中渗入其他元素', 0, 0, 0, 1, '2401010100'),
('2401010109', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC01.KP01.Q09', '错误', '扩散是化学反应的结果', 0, 0, 0, 1, '2401010100');

-- 小节 CH01.SEC02 (1核心+1扩展+0奥赛)
INSERT INTO knowledge_point (kp_id, subject_code, stage_code, grade_code, term_code, code_path, code, name, description, is_core, is_extend, is_olympics, difficulty, parent_id) 
VALUES 
('2401020000', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC02', '油膜法实验', '单分子油膜法测量分子直径', 1, 0, 0, 0.60, '2401000000'),
('2401020100', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC02.KP01', '实验误差分析', '系统误差与偶然误差的定量修正（扩展）', 0, 1, 0, 0.80, '2401020000');

-- 小节 CH01.SEC03 (2核心+0扩展+1奥赛)
INSERT INTO knowledge_point (kp_id, subject_code, stage_code, grade_code, term_code, code_path, code, name, description, is_core, is_extend, is_olympics, difficulty, parent_id) 
VALUES 
('2401030000', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC03', '分子速率分布', '麦克斯韦速率分布律', 1, 0, 0, 0.75, '2401000000'),
('2401030100', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC03.KP01', '统计规律与涨落现象', '大数定律在热力学中的应用', 1, 0, 1, 0.90, '2401030000');

-- 小节 CH01.SEC04 (2核心+1扩展+0奥赛)
INSERT INTO knowledge_point (kp_id, subject_code, stage_code, grade_code, term_code, code_path, code, name, description, is_core, is_extend, is_olympics, difficulty, parent_id) 
VALUES 
('2401040000', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC04', '分子动能与势能', '内能的微观解释', 1, 0, 0, 0.70, '2401000000'),
('2401040100', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC04.KP01', '分子势能曲线分析', '势能极小值与稳定平衡', 1, 0, 0, 0.80, '2401040000'),
('2401040200', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', 'PHYSICS/SENIOR/GRADE_3/TERM_2/CH01', 'CH01.SEC04.KP02', '热力学温度与分子动能关系', '理想气体温度公式推导（扩展）', 0, 1, 0, 0.85, '2401040000');

-- 知识图谱关系插入
-- 章节包含小节
INSERT INTO knowledge_relation (from_kp_id, to_kp_id, relation_type, weight) 
VALUES 
('2401000000', '2401010000', 'contains', 1.0),
('2401000000', '2401020000', 'contains', 1.0),
('2401000000', '2401030000', 'contains', 1.0),
('2401000000', '2401040000', 'contains', 1.0);

-- 小节包含知识点
INSERT INTO knowledge_relation (from_kp_id, to_kp_id, relation_type, weight) 
VALUES 
('2401010000', '2401010100', 'contains', 1.0),
('2401010000', '2401010200', 'contains', 1.0),
('2401010000', '2401010300', 'contains', 1.0),
('2401020000', '2401020100', 'contains', 1.0),
('2401030000', '2401030100', 'contains', 1.0),
('2401040000', '2401040100', 'contains', 1.0),
('2401040000', '2401040200', 'contains', 1.0);

-- 知识点包含问题
INSERT INTO knowledge_relation (from_kp_id, to_kp_id, relation_type, weight) 
VALUES 
('2401010100', '2401010101', 'contains', 1.0),
('2401010100', '2401010102', 'contains', 1.0),
('2401010100', '2401010103', 'contains', 1.0),
('2401010100', '2401010104', 'contains', 1.0),
('2401010100', '2401010105', 'contains', 1.0),
('2401010100', '2401010106', 'contains', 1.0),
('2401010100', '2401010107', 'contains', 1.0),
('2401010100', '2401010108', 'contains', 1.0),
('2401010100', '2401010109', 'contains', 1.0);

-- 知识点间关联关系
INSERT INTO knowledge_relation (from_kp_id, to_kp_id, relation_type, weight) 
VALUES 
-- 油膜法实验依赖分子模型
('2401020000', '2401010300', 'requires', 0.9),
-- 速率分布依赖分子动能
('2401030000', '2401040100', 'relates', 0.8),
-- 奥赛知识点关联跨章节（示例：分子力与后续核力关联）
('2401010200', '2505010300', 'relates', 0.7);  -- 假设第五章原子核的核力知识点为25050103



SELECT * FROM knowledge_point;
SELECT * FROM knowledge_relation;