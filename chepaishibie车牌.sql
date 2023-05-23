/*
Navicat MySQL Data Transfer

Source Server         : fsfx
Source Server Version : 50712
Source Host           : localhost:3306
Source Database       : chepaishibie

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2023-05-12 15:40:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for addchepai_data
-- ----------------------------
DROP TABLE IF EXISTS `addchepai_data`;
CREATE TABLE `addchepai_data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `plate` text COMMENT '人员姓名',
  `enable_time` datetime DEFAULT NULL COMMENT 'base64格式图片',
  `overdue_time` datetime DEFAULT NULL,
  `status` text COMMENT '下发标志 1 已下发  0 未下发',
  `token` text,
  `xinagmu_no` text COMMENT '项目编号',
  `shexiangji_no` text,
  PRIMARY KEY (`id`),
  KEY `index_renlianji_no_and_idcard` (`shexiangji_no`(255)),
  KEY `index_renlianji_no_and_status` (`status`(255),`shexiangji_no`(255)),
  KEY `index_id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for delchepai_data
-- ----------------------------
DROP TABLE IF EXISTS `delchepai_data`;
CREATE TABLE `delchepai_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token` text,
  `plate` varchar(255) DEFAULT NULL,
  `xiangmu_no` text,
  `status` text,
  `shexiangji` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=35126 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for projectcorp
-- ----------------------------
DROP TABLE IF EXISTS `projectcorp`;
CREATE TABLE `projectcorp` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `token` text,
  `corp_name` varchar(255) DEFAULT NULL,
  `corp_code` varchar(255) DEFAULT NULL,
  `entry_time` varchar(255) DEFAULT NULL,
  `corp_type` varchar(255) DEFAULT NULL,
  `projectNo` text COMMENT '项目编号',
  `corpCode` text COMMENT '统一社会信用代码，如果无统一社会信用代码，则用组织机构代码',
  `corpName` text COMMENT '企业名称',
  `corpType` text COMMENT '参建类型。参考参建单位类型字典表',
  `entryTime` text COMMENT '进场时间。格式yyyy-MM-ddHH:mm:ss',
  `exitTime` text COMMENT '退场时间。格式yyyy-MM-ddHH:mm:ss',
  `bankCode` text COMMENT '银行代码。参考银行代码字典表',
  `bankName` text COMMENT '银行支行名称',
  `bankNumber` text COMMENT '银行卡号。需要使用AES加密',
  `bankLinkNumber` text COMMENT '银行联号',
  `bank_code` varchar(255) DEFAULT NULL,
  `bank_link_number` varchar(255) DEFAULT NULL,
  `bank_name` varchar(255) DEFAULT NULL,
  `bank_number` varchar(255) DEFAULT NULL,
  `exit_time` varchar(255) DEFAULT NULL,
  `project_no` varchar(255) DEFAULT NULL,
  `pm_code` text,
  `source_area_code` varchar(255) DEFAULT NULL,
  `worker_amount` text,
  `zb_date` varchar(100) DEFAULT NULL,
  `zb_quxian` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_token` (`token`(255))
) ENGINE=InnoDB AUTO_INCREMENT=1684 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for projectworker
-- ----------------------------
DROP TABLE IF EXISTS `projectworker`;
CREATE TABLE `projectworker` (
  `work_unit` text,
  `token` text,
  `worker_name` text,
  `id_card_number` text,
  `team_name` text,
  `team_no` varchar(30) CHARACTER SET utf8mb4 DEFAULT NULL,
  `date` text,
  `is_push` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '0',
  `is_add_project_worker` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '0',
  `is_worker_entry_exit` varchar(255) CHARACTER SET utf8mb4 DEFAULT '0',
  `is_team_push` varchar(255) CHARACTER SET utf8mb4 DEFAULT '0',
  `type` text,
  `corp_name` text,
  `manage_type` varchar(255) DEFAULT NULL,
  `corp_type` varchar(255) DEFAULT NULL,
  `work_type` text,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `start_date` text,
  `work_date` text,
  `expiry_date` text,
  `joined_time` text,
  `corp_code` text,
  `cell_phone` text,
  `work_role` text,
  `culture_level_type` text,
  `address` text,
  `positive_Id_card_image` varchar(255) DEFAULT NULL,
  `negative_Id_card_image` varchar(255) DEFAULT NULL,
  `contractor_corp_code` text,
  `politics_type` text,
  `gender` text,
  `grant_org` text,
  `nation` text,
  `is_team_leader` text,
  `head_image` longtext,
  `id_card_type` text,
  `is_card` text,
  `marital_status` text,
  `negativeidcard_image` text,
  `has_bad_medical_history` text,
  `has_buy_insurance` text,
  `pay_roll_bank_card_number` varchar(55) DEFAULT NULL,
  `pay_roll_bank_name` text,
  `pay_roll_top_bank_code` text,
  `positiveidcard_image` text,
  `recent_head_image` text,
  `specialty` text,
  `urgent_link_man` text,
  `urgent_link_man_phone` text,
  `bank_link_number` text,
  `post_projectwork_status` text,
  `post_work_status` text,
  PRIMARY KEY (`id`),
  KEY `index_token` (`token`(255)),
  KEY `index_id_card_number` (`id_card_number`(255)),
  KEY `index_token_id_card_number` (`token`(255),`id_card_number`(255)),
  KEY `index_id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=75662 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `token` text,
  `is_push` varchar(255) CHARACTER SET utf8mb4 DEFAULT '0',
  `name` text,
  `project_no` text,
  `user` text,
  `provider` text,
  `pass` text,
  `info` text,
  `leixing` text COMMENT '类型 1 管理员  2 操作员',
  `corp_code` varchar(255) DEFAULT NULL,
  `corp_name` text,
  `source_area_code` varchar(255) DEFAULT NULL,
  `builder_licenses` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `team_no` text,
  `empower` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=662 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for workerattendance
-- ----------------------------
DROP TABLE IF EXISTS `workerattendance`;
CREATE TABLE `workerattendance` (
  `token` text,
  `is_push` varchar(255) DEFAULT '0',
  `source_area_code` varchar(255) DEFAULT '1',
  `name` text,
  `id_card_number` text,
  `id_card_type` text,
  `date` text COMMENT '刷卡时间，yyyy-MM-ddHH:mm:ss',
  `direction` text COMMENT '刷卡进出方向。参考工人考勤方向字典表',
  `image` longtext COMMENT '刷卡近照。Base64字符串，不超过50KB',
  `channel` text COMMENT '进出标志',
  `dataList` text COMMENT '考勤列表。JSON数组，数组长度不超过20',
  `projectNo` text COMMENT '项目编号',
  `teamNo` text COMMENT '班组编号',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `attendType` text COMMENT '通行方式。参考工人通行方式字典表',
  `lng` text COMMENT 'WGS84经度',
  `lat` text COMMENT 'WGS84纬度',
  `temperature` text COMMENT '工人体温，35-99 范围数字，最长支持两位小数',
  `attend_type` text,
  `data_list` text,
  `project_no` text,
  `team_no` text,
  `poststatus` text,
  `provider` text,
  `last_date` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8631 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for workerattendance_history
-- ----------------------------
DROP TABLE IF EXISTS `workerattendance_history`;
CREATE TABLE `workerattendance_history` (
  `token` text,
  `is_push` varchar(6) DEFAULT '0',
  `source_area_code` varchar(255) DEFAULT '1',
  `name` text,
  `id_card_number` text,
  `id_card_type` text,
  `date` text COMMENT '刷卡时间，yyyy-MM-ddHH:mm:ss',
  `direction` text COMMENT '刷卡进出方向。参考工人考勤方向字典表',
  `image` longtext COMMENT '刷卡近照。Base64字符串，不超过50KB',
  `channel` text COMMENT '进出标志',
  `dataList` text COMMENT '考勤列表。JSON数组，数组长度不超过20',
  `projectNo` text COMMENT '项目编号',
  `teamNo` text COMMENT '班组编号',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `attendType` text COMMENT '通行方式。参考工人通行方式字典表',
  `lng` text COMMENT 'WGS84经度',
  `lat` text COMMENT 'WGS84纬度',
  `temperature` text COMMENT '工人体温，35-99 范围数字，最长支持两位小数',
  `attend_type` text,
  `data_list` text,
  `project_no` text,
  `team_no` text,
  `poststatus` text,
  `provider` text,
  `last_date` text,
  PRIMARY KEY (`id`),
  KEY `index_token` (`token`(255)),
  KEY `index_id_card_number` (`id_card_number`(255)),
  KEY `index_token_and_id_card_number` (`token`(255),`id_card_number`(255)),
  KEY `index_id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for xiangmu_renlianji_guanlian
-- ----------------------------
DROP TABLE IF EXISTS `xiangmu_renlianji_guanlian`;
CREATE TABLE `xiangmu_renlianji_guanlian` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `xiangmu_no` text COMMENT '项目编号',
  `renlianji_no` text COMMENT '人脸机编号',
  `xiangmu_name` text,
  `renlianji_last_time` text COMMENT '人脸机最后更新时间',
  `renlianji_name` text COMMENT '人脸机名称',
  `direction` text,
  `lat` text,
  `lng` text,
  `source_area_code` text,
  `reboot` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1852 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for xiangmu_table
-- ----------------------------
DROP TABLE IF EXISTS `xiangmu_table`;
CREATE TABLE `xiangmu_table` (
  `name` text,
  `token` varchar(255) DEFAULT NULL,
  `provider` varchar(255) DEFAULT NULL,
  `project_no` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `area_code` varchar(255) DEFAULT NULL,
  `az_name` text,
  `supplier_name` text,
  `builder_license_umm` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `complete_date` date DEFAULT NULL,
  `contractor_corp_code` varchar(255) DEFAULT NULL,
  `contractor_corp_name` varchar(255) DEFAULT NULL,
  `corp_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `function_num` varchar(3) DEFAULT NULL,
  `jl_name` varchar(255) DEFAULT NULL,
  `jl_phone` varchar(255) DEFAULT NULL,
  `jlcorp_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '',
  `jlcorp_name` varchar(255) DEFAULT NULL,
  `kf_area_code` text,
  `prj_name` text,
  `prj_size` varchar(2) DEFAULT NULL,
  `prj_status` varchar(255) DEFAULT NULL,
  `prmanager` varchar(255) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_push` varchar(255) DEFAULT '0',
  `property_num` varchar(3) DEFAULT NULL,
  `prphone` varchar(255) DEFAULT NULL,
  `register_date` datetime DEFAULT NULL,
  `smj_name` varchar(255) DEFAULT NULL,
  `smj_phone` varchar(255) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `is_corp_push` varchar(5) DEFAULT '0',
  `corp_code` varchar(255) DEFAULT NULL,
  `invest` varchar(255) DEFAULT NULL,
  `building_area` varchar(255) DEFAULT NULL,
  `az_Phone` varchar(255) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `uptede_type` text,
  `zb_date` text,
  `zb_quxian` text,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1599 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
