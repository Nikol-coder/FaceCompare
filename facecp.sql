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

 Date: 14/01/2024 23:52:38
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
  `age` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `flag` double(1, 0) UNSIGNED NOT NULL,
  PRIMARY KEY (`picid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pictable
-- ----------------------------
INSERT INTO `pictable` VALUES (1, 1, '彤彤', '5', '四川省成都市郫筒街道', '5000', 0);
INSERT INTO `pictable` VALUES (2, 1, '果果', '4', '天津市武清区\r\n杨村街道  ', '4200', 1);
INSERT INTO `pictable` VALUES (3, 2, '红红', '9', '上海市徐汇区凌云街道 ', '7642', 1);
INSERT INTO `pictable` VALUES (4, 3, '绿绿', '6', '河北省邢台市北大街街道', '4563', 1);
INSERT INTO `pictable` VALUES (5, 4, '泡泡', '7', '河南省郑州市融创街道', '7961', 1);
INSERT INTO `pictable` VALUES (6, 6, '果果', '9', '北京市怀柔区怀北镇', '4399', 1);
INSERT INTO `pictable` VALUES (7, 6, '妮妮', '3', '四川省绵阳市绵阳街道', '7456', 2);
INSERT INTO `pictable` VALUES (8, 2, '跳跳', '7', '山东省德州市电锯街区', '6532', 1);

-- ----------------------------
-- Table structure for usertable
-- ----------------------------
DROP TABLE IF EXISTS `usertable`;
CREATE TABLE `usertable`  (
  `userid` double(255, 0) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
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
INSERT INTO `usertable` VALUES (6, '蜀道山', '48 48 48 52 53 54 55 56 57 58 ', '辽宁省', '147852369');
INSERT INTO `usertable` VALUES (7, '魔法披风', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '上海', '14756');

-- ----------------------------
-- Table structure for videotable
-- ----------------------------
DROP TABLE IF EXISTS `videotable`;
CREATE TABLE `videotable`  (
  `videoid` double(255, 0) NOT NULL AUTO_INCREMENT,
  `time` date NOT NULL COMMENT '失踪时间',
  `place` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '失踪地点',
  PRIMARY KEY (`videoid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of videotable
-- ----------------------------
INSERT INTO `videotable` VALUES (1, '2023-12-14', '北京市怀柔区');
INSERT INTO `videotable` VALUES (2, '2023-11-09', '上海市');
INSERT INTO `videotable` VALUES (3, '2023-12-15', '黑龙江省');
INSERT INTO `videotable` VALUES (6, '2023-01-06', '四川省');
INSERT INTO `videotable` VALUES (7, '2023-10-01', '浙江省');

SET FOREIGN_KEY_CHECKS = 1;
