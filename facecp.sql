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

 Date: 05/01/2024 16:40:55
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
) ENGINE = InnoDB AUTO_INCREMENT = 110 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admintable
-- ----------------------------
INSERT INTO `admintable` VALUES (110, '110', '管理员');

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
  `flag` double(1, 0) UNSIGNED NOT NULL,
  PRIMARY KEY (`picid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pictable
-- ----------------------------
INSERT INTO `pictable` VALUES (1, 1, '彤彤', '5', '四川', '5000', 0);
INSERT INTO `pictable` VALUES (2, 1, '果果', '4', '天津', '4200', 1);
INSERT INTO `pictable` VALUES (3, 2, '红红', '9', '上海', '7642', 1);
INSERT INTO `pictable` VALUES (4, 3, '绿绿', '6', '河北', '4563', 1);
INSERT INTO `pictable` VALUES (5, 4, '泡泡', '7', '河南', '7961', 1);

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
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of usertable
-- ----------------------------
INSERT INTO `usertable` VALUES (1, '小明', '123', '四川', '456');
INSERT INTO `usertable` VALUES (2, '小红', '789', '北京', '7412');
INSERT INTO `usertable` VALUES (3, 'John', '4563', '河北', 'john@example.com');
INSERT INTO `usertable` VALUES (4, '乔治', '4 2 3 7 5', '天津', '74125');
INSERT INTO `usertable` VALUES (5, '大龙', '48 54 54 50 53 54 55 56 57 58 ', '广东', '1417');
INSERT INTO `usertable` VALUES (6, '985', '48 48 48 52 53 54 55 56 57 58 ', '西藏', '147852369');

-- ----------------------------
-- Table structure for videotable
-- ----------------------------
DROP TABLE IF EXISTS `videotable`;
CREATE TABLE `videotable`  (
  `videoid` double(255, 0) NOT NULL AUTO_INCREMENT,
  `time` date NOT NULL COMMENT '失踪时间',
  `place` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '失踪地点',
  PRIMARY KEY (`videoid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of videotable
-- ----------------------------
INSERT INTO `videotable` VALUES (1, '2023-12-14', '北京市怀柔区');
INSERT INTO `videotable` VALUES (2, '2023-11-09', '上海市');

SET FOREIGN_KEY_CHECKS = 1;
