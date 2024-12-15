
# Database Sql
- create `test_db` database
- create `task` table
- create `clue` table
- create `user` table


## Sql

```
-- create `test_db` database

CREATE DATABASE test_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for clue
-- ----------------------------
DROP TABLE IF EXISTS `clue`;
CREATE TABLE `clue`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `clue_id` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '线索id',
  `rule_id` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '策略id',
  `clue_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '线索类型(消息 message, 账号 user, 群组 chat)',
  `document_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '线索ES文档ID',
  `status` int(11) NOT NULL COMMENT '线索状态',
  `clue_detail` json NOT NULL COMMENT '线索详情',
  `mention_elements` json NOT NULL COMMENT '提及要素',
  `origin_create_time` datetime(0) NOT NULL COMMENT '线索产生时间',
  `update_time` datetime(0) NOT NULL COMMENT '更新时间',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  `remarks` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `is_favorite` int(11) UNSIGNED ZEROFILL NOT NULL COMMENT '是否收藏（未收藏 0， 已收藏 1）',
  `topic` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '对应rule中的topic',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '线索表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of clue
-- ----------------------------
INSERT INTO `clue` VALUES (763, 'f49b835e77', 'f3023be8b2', 'message', '-1001788561127_863964', 0, '{\"date\": \"2023-07-20 10:21:01\", \"text\": \"打开Mysql\"}', '{}', '2023-10-11 16:29:26', '2023-10-11 16:29:26', '2023-10-11 16:29:26', '', 00000000000, 'topic_demo');
INSERT INTO `clue` VALUES (764, 'ace2777597', 'f3023be8b2', 'message', '-1001369709666_1573441', 0, '{\"date\": \"2023-07-21 14:23:01\", \"text\": \"关闭Mysql\"}', '{}', '2023-10-11 16:29:26', '2023-10-11 16:29:26', '2023-10-11 16:29:26', '', 00000000000, 'topic_demo');

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `task_id` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务id',
  `task_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务名称',
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务来源',
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务类型',
  `status` int(1) NOT NULL COMMENT '任务状态(-1 全部, 0 进行中, 1 已完成)',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `owner_user_id` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务创建人id',
  `responsible_user_id` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务负责人id',
  `start_time` datetime(0) NOT NULL COMMENT '任务开始时间',
  `end_time` datetime(0) NOT NULL COMMENT '任务结束时间',
  `update_time` datetime(0) NOT NULL COMMENT '更新时间',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '任务表' ROW_FORMAT = Dynamic;


INSERT INTO `task` VALUES (2, '71c3f191ed', '测试任务2', '', 'daily', 0, NULL, '63deddaa23', '63deddaa23', '2023-11-15 16:30:07', '2023-11-15 16:30:07', '2023-11-15 16:30:07', '2023-11-15 16:30:07');


-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户id',
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `nick_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '昵称',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话',
  `is_admin` int(11) NOT NULL COMMENT '是否是管理员(0 普通用户, 1 管理员)',
  `is_active` int(11) NOT NULL COMMENT '是否活跃(0 不活跃, 1 活跃)',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `update_time` datetime(0) NOT NULL COMMENT '更新时间',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  `remarks` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 176 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (6, 'a7c2aa3a80', 'root', '$2b$12$yF1XcaizU09hJydcDa5weO3AQq/vtXybNZJjFMltudOqHtjr6XmcC', NULL, 'root@example.com', NULL, 1, 1, NULL, '2023-07-25 20:41:01', '2023-07-25 20:41:01', NULL);

```





