-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dart
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `corp_exception`
--

DROP TABLE IF EXISTS `corp_exception`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corp_exception` (
  `status` text,
  `message` text,
  `corp_code` text,
  `corp_name` text,
  `corp_name_eng` text,
  `stock_name` text,
  `corp_exceptioncol` text,
  `ceo_nm` text,
  `corp_cls` text,
  `jurir_no` text,
  `bizr_no` text,
  `adres` text,
  `hm_url` text,
  `ir_url` text,
  `phn_no` text,
  `fax_no` text,
  `induty_code` text,
  `est_dt` text,
  `acc_mt` text,
  `excel_1` longtext,
  `excel_2` longtext,
  `excel_3` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corp_exception`
--

LOCK TABLES `corp_exception` WRITE;
/*!40000 ALTER TABLE `corp_exception` DISABLE KEYS */;
INSERT INTO `corp_exception` VALUES ('000','정상','01170962','그레이트리치과기유한공사','Great Rich Technologies Limited','GRT','900290','주영남','K','','1798794','Room 01, 21F, Prosper Commercial Building, 9 Yin Chong Street, Kowloon, Hong Kong','','','85236458129','','64992','20120911','06',NULL,NULL,NULL),('000','정상','01139266','로스웰인터내셔널유한회사','ROTHWELL INTERNATIONAL CO., LIMITED','로스웰','900260','저우샹동','K','','2034342','Unit 402, 4th Floor, Fairmont House, No. 8 Cotton Tree Drive, Admiralty Hong Kong','www.rothwell.com.cn','rothwell.tech','86-514-876387','','64992','20140205','12',NULL,NULL,NULL),('000','정상','01107665','차이나크리스탈신소재홀딩스','China Crystal New Material Holdings Co.,  Ltd.','크리스탈신소재','900250','다이중치우 (DAI ZHONG QIU)','K','','BS-266537','Artemis House, 75 Fort Street, George Town, P.O. Box 31493, Grand Cayman KY1-1206 Cayman Islands','www.crystalnewmaterial.com','http://crystalnewmaterial.com','86-510-68171266','','64992','20120223','12',NULL,NULL,NULL),('000','정상','01236286','컬러레이홀딩스','Coloray International Investment Co., Limited','컬러레이','900310','줘중비아오','K','','1979772','Connaught Place, Central, Hong Kong Suite 3201, Jardine house 1','www.coloray.co.kr','','02	-2088-8526','02-714-8527','649','20131014','12',NULL,NULL,NULL),('000','정상','01169434','오가닉티코스메틱스홀딩스컴퍼니리미티드','ORGANIC TEA COSMETICS HOLDINGS COMPANY LIMITED','오가닉티코스메틱','900300','채정망','K','','42651','11 Wing Wo Street, Central, HONG KONG Unit 1, 9/F, Wo Hing Commercial Building','','','86-599-8508611','','64992','20121127','12',NULL,NULL,NULL),('000','정상','00781202','애머릿지코퍼레이션','Ameridge Corporation','애머릿지','900100','Thomas Park','K','','845223','222 S Harbor Blvd. STE 820,830,  Anaheim, CA 92805 -','ameridgecorp.com','http://www.newpridecorporation.com/','1-310-631-7000','02-2052-2121','452','19780501','12',NULL,NULL,NULL),('000','정상','01328639','윙입푸드홀딩스','WING YIP FOOD HOLDINGS GROUP LIMITED','윙입푸드','900340','왕현도','K','','46295','UNIT B, 17/F, UNITED CENTRE, 95 QUEENSWAY, ADMIRALTY, HK -','wingyip-food.com','','86-760-23215457','86-760-23211889','64992','20150424','12',NULL,NULL,NULL),('000','정상','01041828','주식회사 제이티씨','JTC Inc.','JTC','950170','구철모','K','','3200-01-006914','(160-0017) 도쿄도 신주쿠구 사몬쵸 2-6 와코빌딩 6F -','www.groupjtc.com/korean/','http://www.groupjtc.com/korean/ir/','02-785-9101','02-2661-9103','471','19940317','02',NULL,NULL,NULL),('000','정상','01160512','헝셩그룹유한회사','HENG SHENG HOLDING GROUP COMPANY LIMITED','헝셩그룹','900270','후이만킷','K','0000000000000','530657','ROOM 6, 3F., Lladro Centre, 72-80 Hoi Yuen Road, Kwun Tong, Kowloon, Hong Kong','www.hengsheng.co.kr/','','02-2125-5058','8659585225118','64992','19951114','12',NULL,NULL,NULL),('000','정상','00799070','이스트아시아홀딩스인베스트먼트리미티드','East Asia Holdings Investment Limited','이스트아시아홀딩스','900110','정강위, 정소영','K','9999990000014','5091880500007098','Kowloon, Hong Kong Unit 912, 9/F., Two Harbourfront, 22 Tak Fung Street, Hunghom','www.qiuzhi.com','','852-3189-0100','','64992','20090722','12',NULL,NULL,NULL);
/*!40000 ALTER TABLE `corp_exception` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-21 22:49:09
