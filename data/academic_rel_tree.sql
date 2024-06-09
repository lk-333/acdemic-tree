/*
 Navicat Premium Data Transfer

 Source Server         : a
 Source Server Type    : MySQL
 Source Server Version : 80200
 Source Host           : localhost:3306
 Source Schema         : academic_rel_tree

 Target Server Type    : MySQL
 Target Server Version : 80200
 File Encoding         : 65001

 Date: 09/06/2024 13:53:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for mentorship
-- ----------------------------
DROP TABLE IF EXISTS `mentorship`;
CREATE TABLE `mentorship`  (
  `mentorship_id` bigint(0) NOT NULL,
  `mentor_id` bigint(0) NULL DEFAULT NULL,
  `mentee_id` bigint(0) NULL DEFAULT NULL,
  `start_date` date NULL DEFAULT NULL,
  `end_date` date NULL DEFAULT NULL,
  PRIMARY KEY (`mentorship_id`) USING BTREE,
  INDEX `mentor_id_key`(`mentor_id`) USING BTREE,
  INDEX `mentee_id_key`(`mentee_id`) USING BTREE,
  CONSTRAINT `mentee_id_key` FOREIGN KEY (`mentee_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `mentor_id_key` FOREIGN KEY (`mentor_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mentorship
-- ----------------------------
INSERT INTO `mentorship` VALUES (333, 111, 222, NULL, NULL);
INSERT INTO `mentorship` VALUES (555, 222, 333, NULL, NULL);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` bigint(0) NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `identity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `real_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `profile_link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (111, '123456', 'StuLiMing', 'admin', '李明', 'https://stuliming.github.io/');
INSERT INTO `user` VALUES (222, '888888', '品爷', 'admin', '吕品', 'www.bilibili.com');
INSERT INTO `user` VALUES (333, '654321', '齐天大圣', 'admin', '侯志一', 'www.pornhub');

SET FOREIGN_KEY_CHECKS = 1;
