/*
Navicat MySQL Data Transfer

Source Server         : 本地服务器
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : spider

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2019-01-21 13:59:16
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for cellbank_failed_arc_url
-- ----------------------------
DROP TABLE IF EXISTS `cellbank_failed_arc_url`;
CREATE TABLE `cellbank_failed_arc_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of cellbank_failed_arc_url
-- ----------------------------
INSERT INTO `cellbank_failed_arc_url` VALUES ('1', 'http://cellbank.snu.ac.kr//english/sub/catalog.php?s_cellid=363&page=detail_info&CatNo=60&sb_find=&qry_str=&sb_div=&cb_patent=&cb_distrib=');
