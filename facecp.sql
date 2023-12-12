/*
 Navicat Premium Data Transfer

 Source Server         : yezouhua
 Source Server Type    : MySQL
 Source Server Version : 80034
 Source Host           : localhost:3306
 Source Schema         : facecp

 Target Server Type    : MySQL
 Target Server Version : 80034
 File Encoding         : 65001

 Date: 12/12/2023 21:59:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admintable
-- ----------------------------
DROP TABLE IF EXISTS `admintable`;
CREATE TABLE `admintable`  (
  `adminid` double(255, 0) NOT NULL AUTO_INCREMENT,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `adminname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`adminid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admintable
-- ----------------------------

-- ----------------------------
-- Table structure for pictable
-- ----------------------------
DROP TABLE IF EXISTS `pictable`;
CREATE TABLE `pictable`  (
  `picid` double(255, 0) NOT NULL AUTO_INCREMENT,
  `userid` double(255, 0) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `age` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `price` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `flag` binary(255) NOT NULL,
  PRIMARY KEY (`picid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pictable
-- ----------------------------

-- ----------------------------
-- Table structure for usertable
-- ----------------------------
DROP TABLE IF EXISTS `usertable`;
CREATE TABLE `usertable`  (
  `userid` double(255, 0) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `tel` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`userid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of usertable
-- ----------------------------
INSERT INTO `usertable` VALUES (1, '小明', '123', '四川', 'jane@example.com');
INSERT INTO `usertable` VALUES (2, '小红', '789', '北京', '7412');
INSERT INTO `usertable` VALUES (3, 'John', '4563', '河北', 'john@example.com');

-- ----------------------------
-- Table structure for videotable
-- ----------------------------
DROP TABLE IF EXISTS `videotable`;
CREATE TABLE `videotable`  (
  `videoid` double(255, 0) NOT NULL AUTO_INCREMENT,
  `place` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `time` datetime(0) NOT NULL,
  PRIMARY KEY (`videoid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of videotable
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
