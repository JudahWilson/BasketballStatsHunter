-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: bb
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actionmap`
--

DROP TABLE IF EXISTS `actionmap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `actionmap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(64) NOT NULL,
  `play_map_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `actionmap_fk1` (`play_map_id`),
  CONSTRAINT `actionmap_fk1` FOREIGN KEY (`play_map_id`) REFERENCES `playmap` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coaches`
--

DROP TABLE IF EXISTS `coaches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coaches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `br_id` varchar(10) DEFAULT NULL,
  `first_name` varchar(35) DEFAULT NULL,
  `last_name` varchar(35) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `origin_city` varchar(35) DEFAULT NULL,
  `origin_territory` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `br_id` (`br_id`),
  UNIQUE KEY `br_id_2` (`br_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coachstates`
--

DROP TABLE IF EXISTS `coachstates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coachstates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coach_br_id` varchar(10) DEFAULT NULL,
  `team_br_id` char(3) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `coach_br_id` (`coach_br_id`),
  KEY `fk_team_br_id` (`team_br_id`),
  CONSTRAINT `fk_coach_br_id` FOREIGN KEY (`coach_br_id`) REFERENCES `coaches` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_team_br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `games` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `br_id` varchar(12) DEFAULT NULL,
  `season_br_id` char(8) DEFAULT NULL,
  `home_team_br_id` char(3) DEFAULT NULL,
  `away_team_br_id` char(3) DEFAULT NULL,
  `home_team_points` int(11) DEFAULT NULL,
  `away_team_points` int(11) DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  `attendance` int(11) DEFAULT NULL,
  `duration_minutes` int(11) DEFAULT NULL,
  `arena` varchar(65) DEFAULT NULL,
  `ot` varchar(3) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `inactive_players` text DEFAULT NULL,
  `officials` text DEFAULT NULL,
  `game_duration` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `unique_br_id` (`br_id`),
  KEY `fk_games__home_team_br_id__teams__br_id` (`home_team_br_id`),
  CONSTRAINT `fk_games__home_team_br_id__teams__br_id` FOREIGN KEY (`home_team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1062460 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `playactions`
--

DROP TABLE IF EXISTS `playactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `play_id` int(11) DEFAULT NULL,
  `player_br_id` varchar(9) DEFAULT NULL,
  `team_br_id` varchar(3) DEFAULT NULL,
  `action_code` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_playactions__player_br_id__players__br_id` (`player_br_id`),
  KEY `fk_playactions__team_br_id__teams__br_id` (`team_br_id`),
  CONSTRAINT `fk_playactions__player_br_id__players__br_id` FOREIGN KEY (`player_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_playactions__team_br_id__teams__br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `playergamehalfstats`
--

DROP TABLE IF EXISTS `playergamehalfstats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playergamehalfstats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_br_id` varchar(9) DEFAULT NULL,
  `game_br_id` char(12) DEFAULT NULL,
  `team_br_id` char(3) DEFAULT NULL,
  `half` int(11) DEFAULT NULL,
  `opponent_br_id` char(3) DEFAULT NULL,
  `quarter` int(11) DEFAULT NULL,
  `seconds_played` int(11) DEFAULT NULL,
  `field_goals` int(11) DEFAULT NULL,
  `field_goal_attempts` int(11) DEFAULT NULL,
  `field_goal_percentage` decimal(4,3) DEFAULT NULL,
  `three_pointers` int(11) DEFAULT NULL,
  `three_pointer_attempts` int(11) DEFAULT NULL,
  `three_pointer_percentage` decimal(4,3) DEFAULT NULL,
  `free_throws` int(11) DEFAULT NULL,
  `free_throw_attempts` int(11) DEFAULT NULL,
  `free_throw_percentage` decimal(4,3) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `offensive_rebounds` int(11) DEFAULT NULL,
  `defensive_rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `personal_fouls` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  `plus_minus` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_playergamehalfstats__player_br_id__players__br_id` (`player_br_id`),
  KEY `fk_playergamehalfstats__game_br_id__games__br_id` (`game_br_id`),
  KEY `fk_playergamehalfstats__team_br_id__teams__br_id` (`team_br_id`),
  CONSTRAINT `fk_playergamehalfstats__game_br_id__games__br_id` FOREIGN KEY (`game_br_id`) REFERENCES `games` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_playergamehalfstats__player_br_id__players__br_id` FOREIGN KEY (`player_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_playergamehalfstats__team_br_id__teams__br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7001991 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `playergameovertimestats`
--

DROP TABLE IF EXISTS `playergameovertimestats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playergameovertimestats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_br_id` varchar(9) DEFAULT NULL,
  `game_br_id` char(12) DEFAULT NULL,
  `team_br_id` char(3) DEFAULT NULL,
  `opponent_br_id` char(3) DEFAULT NULL,
  `overtime` int(11) DEFAULT NULL,
  `seconds_played` int(11) DEFAULT NULL,
  `field_goals` int(11) DEFAULT NULL,
  `field_goal_attempts` int(11) DEFAULT NULL,
  `field_goal_percentage` decimal(4,3) DEFAULT NULL,
  `three_pointers` int(11) DEFAULT NULL,
  `three_pointer_attempts` int(11) DEFAULT NULL,
  `three_pointer_percentage` decimal(4,3) DEFAULT NULL,
  `free_throws` int(11) DEFAULT NULL,
  `free_throw_attempts` int(11) DEFAULT NULL,
  `free_throw_percentage` decimal(4,3) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `offensive_rebounds` int(11) DEFAULT NULL,
  `defensive_rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `personal_fouls` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  `plus_minus` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_playergameovertimestats__player_br_id__players__br_id` (`player_br_id`),
  KEY `fk_playergameovertimestats__game_br_id__games__br_id` (`game_br_id`),
  KEY `fk_playergameovertimestats__team_br_id__teams__br_id` (`team_br_id`),
  CONSTRAINT `fk_playergameovertimestats__game_br_id__games__br_id` FOREIGN KEY (`game_br_id`) REFERENCES `games` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_playergameovertimestats__player_br_id__players__br_id` FOREIGN KEY (`player_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_playergameovertimestats__team_br_id__teams__br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=61369 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `playergamequarterstats`
--

DROP TABLE IF EXISTS `playergamequarterstats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playergamequarterstats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_br_id` varchar(9) DEFAULT NULL,
  `game_br_id` char(12) DEFAULT NULL,
  `team_br_id` char(3) DEFAULT NULL,
  `opponent_br_id` char(3) DEFAULT NULL,
  `quarter` int(11) DEFAULT NULL,
  `seconds_played` int(11) DEFAULT NULL,
  `field_goals` int(11) DEFAULT NULL,
  `field_goal_attempts` int(11) DEFAULT NULL,
  `field_goal_percentage` decimal(4,3) DEFAULT NULL,
  `three_pointers` int(11) DEFAULT NULL,
  `three_pointer_attempts` int(11) DEFAULT NULL,
  `three_pointer_percentage` decimal(4,3) DEFAULT NULL,
  `free_throws` int(11) DEFAULT NULL,
  `free_throw_attempts` int(11) DEFAULT NULL,
  `free_throw_percentage` decimal(4,3) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `offensive_rebounds` int(11) DEFAULT NULL,
  `defensive_rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `personal_fouls` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  `plus_minus` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_playergamequarterstats__player_br_id__players__br_id` (`player_br_id`),
  KEY `fk_playergamequarterstats__game_br_id__games__br_id` (`game_br_id`),
  KEY `fk_playergamequarterstats__team_br_id__teams__br_id` (`team_br_id`),
  CONSTRAINT `fk_playergamequarterstats__game_br_id__games__br_id` FOREIGN KEY (`game_br_id`) REFERENCES `games` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_playergamequarterstats__player_br_id__players__br_id` FOREIGN KEY (`player_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_playergamequarterstats__team_br_id__teams__br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21272981 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `playergamestats`
--

DROP TABLE IF EXISTS `playergamestats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playergamestats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_br_id` varchar(9) DEFAULT NULL,
  `game_br_id` char(12) DEFAULT NULL,
  `team_br_id` char(3) DEFAULT NULL,
  `opponent_team_br_id` char(3) DEFAULT NULL,
  `played` tinyint(1) DEFAULT NULL,
  `reason_for_absence` varchar(20) DEFAULT NULL,
  `started` tinyint(1) DEFAULT NULL,
  `seconds_played` int(11) DEFAULT NULL,
  `field_goals` int(11) DEFAULT NULL,
  `field_goal_attempts` int(11) DEFAULT NULL,
  `field_goal_percentage` decimal(4,3) DEFAULT NULL,
  `three_pointers` int(11) DEFAULT NULL,
  `three_pointer_attempts` int(11) DEFAULT NULL,
  `three_pointer_percentage` decimal(4,3) DEFAULT NULL,
  `free_throws` int(11) DEFAULT NULL,
  `free_throw_attempts` int(11) DEFAULT NULL,
  `free_throw_percentage` decimal(4,3) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `offensive_rebounds` int(11) DEFAULT NULL,
  `defensive_rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `personal_fouls` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  `plus_minus` int(11) DEFAULT NULL,
  `true_shooting_percentage` decimal(4,3) DEFAULT NULL,
  `effective_field_goal_percentage` decimal(4,3) DEFAULT NULL,
  `three_point_attempt_rate` decimal(4,3) DEFAULT NULL,
  `free_throw_attempt_rate` decimal(6,3) DEFAULT NULL,
  `offensive_rebound_percentage` decimal(4,3) DEFAULT NULL,
  `defensive_rebound_percentage` decimal(4,3) DEFAULT NULL,
  `total_rebound_percentage` decimal(4,3) DEFAULT NULL,
  `assist_percentage` decimal(4,3) DEFAULT NULL,
  `steal_percentage` decimal(4,3) DEFAULT NULL,
  `block_percentage` decimal(4,3) DEFAULT NULL,
  `turnover_percentage` decimal(4,3) DEFAULT NULL,
  `usage_percentage` decimal(4,3) DEFAULT NULL,
  `offensive_rating` int(11) DEFAULT NULL,
  `defensive_rating` int(11) DEFAULT NULL,
  `box_plus_minus` decimal(4,1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_playergamestats__player_br_id__players__br_id` (`player_br_id`),
  KEY `fk_playergamestats__game_br_id__games__br_id` (`game_br_id`),
  KEY `fk_playergamestats__team_br_id__teams__br_id` (`team_br_id`),
  CONSTRAINT `fk_playergamestats__game_br_id__games__br_id` FOREIGN KEY (`game_br_id`) REFERENCES `games` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_playergamestats__player_br_id__players__br_id` FOREIGN KEY (`player_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_playergamestats__team_br_id__teams__br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9084423 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `players` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `br_id` varchar(9) DEFAULT NULL COMMENT 'TEST',
  `first_name` varchar(35) DEFAULT NULL,
  `last_name` varchar(35) DEFAULT NULL,
  `city` varchar(30) DEFAULT NULL,
  `territory` varchar(30) DEFAULT NULL,
  `country` varchar(30) DEFAULT NULL,
  `full_name` varchar(50) DEFAULT NULL,
  `suffix` varchar(5) DEFAULT NULL,
  `year_start` char(4) DEFAULT NULL,
  `year_end` char(4) DEFAULT NULL,
  `position` char(5) DEFAULT NULL,
  `height_str` char(4) DEFAULT NULL,
  `height_in` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `colleges` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`colleges`)),
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `br_id` (`br_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `playerstates`
--

DROP TABLE IF EXISTS `playerstates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playerstates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_br_id` varchar(9) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  `jersey_no` int(11) DEFAULT NULL,
  `position` varchar(3) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `playloaderrors`
--

DROP TABLE IF EXISTS `playloaderrors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playloaderrors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(200) DEFAULT NULL,
  `quarter` int(11) DEFAULT NULL,
  `time` varchar(7) DEFAULT NULL,
  `html` varchar(300) DEFAULT NULL,
  `error` longtext DEFAULT NULL,
  `traceback` longtext DEFAULT NULL,
  `is_play_not_yet_supported_error` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `playmap`
--

DROP TABLE IF EXISTS `playmap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playmap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content_format` varchar(200) NOT NULL COMMENT 'the structure of the pbp row. \r\n- {FT} resembles feet variable.\r\n- {PL} resembles player variable.\r\n- {TM} resembles team variable.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plays`
--

DROP TABLE IF EXISTS `plays`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plays` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_br_id` varchar(12) DEFAULT NULL,
  `quarter` int(11) DEFAULT NULL,
  `clock_time` char(7) DEFAULT NULL,
  `distance_feet` int(11) DEFAULT NULL,
  `home_score` int(11) NOT NULL,
  `away_score` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_plays__game_br_id__games__br_id` (`game_br_id`),
  CONSTRAINT `fk_plays__game_br_id__games__br_id` FOREIGN KEY (`game_br_id`) REFERENCES `games` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seasons`
--

DROP TABLE IF EXISTS `seasons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seasons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `season_start_year` char(4) DEFAULT NULL,
  `season_end_year` char(4) DEFAULT NULL,
  `league` char(3) DEFAULT NULL,
  `champion` int(11) DEFAULT NULL,
  `mvp` int(11) DEFAULT NULL,
  `roy` int(11) DEFAULT NULL,
  `scoring_leader` int(11) DEFAULT NULL,
  `rebounds_leader` int(11) DEFAULT NULL,
  `assists_leader` int(11) DEFAULT NULL,
  `win_shares_leader` int(11) DEFAULT NULL,
  `br_id` char(8) DEFAULT NULL,
  `active` char(8) DEFAULT NULL,
  `champion_br_id` char(20) DEFAULT NULL,
  `mvp_br_id` char(20) DEFAULT NULL,
  `roy_br_id` char(20) DEFAULT NULL,
  `scoring_leader_br_id` char(20) DEFAULT NULL,
  `rebounding_leader_br_id` char(20) DEFAULT NULL,
  `assists_leader_br_id` char(20) DEFAULT NULL,
  `winshares_leader_br_id` char(20) DEFAULT NULL,
  `scoring_leader_points` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_seasons__champion_br_id__teams__br_id` (`champion_br_id`),
  KEY `fk_seasons__mvp_br_id__players__br_id` (`mvp_br_id`),
  KEY `fk_seasons__roy_br_id__players__br_id` (`roy_br_id`),
  KEY `fk_seasons__scoring_leader_br_id__players__br_id` (`scoring_leader_br_id`),
  KEY `fk_seasons__rebounding_leader_br_id__players__br_id` (`rebounding_leader_br_id`),
  KEY `fk_seasons__assists_leader_br_id__players__br_id` (`assists_leader_br_id`),
  KEY `fk_seasons__winshares_leader_br_id__players__br_id` (`winshares_leader_br_id`),
  CONSTRAINT `fk_seasons__assists_leader_br_id__players__br_id` FOREIGN KEY (`assists_leader_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_seasons__champion_br_id__teams__br_id` FOREIGN KEY (`champion_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_seasons__mvp_br_id__players__br_id` FOREIGN KEY (`mvp_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_seasons__rebounding_leader_br_id__players__br_id` FOREIGN KEY (`rebounding_leader_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_seasons__roy_br_id__players__br_id` FOREIGN KEY (`roy_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_seasons__scoring_leader_br_id__players__br_id` FOREIGN KEY (`scoring_leader_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_seasons__winshares_leader_br_id__players__br_id` FOREIGN KEY (`winshares_leader_br_id`) REFERENCES `players` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teamgamehalfstats`
--

DROP TABLE IF EXISTS `teamgamehalfstats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teamgamehalfstats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `game_br_id` varchar(12) DEFAULT NULL,
  `team_br_id` char(3) DEFAULT NULL,
  `half` int(11) DEFAULT NULL,
  `minutes_played` int(11) DEFAULT NULL,
  `field_goals` int(11) DEFAULT NULL,
  `field_goal_attempts` int(11) DEFAULT NULL,
  `field_goal_percentage` decimal(5,2) DEFAULT NULL,
  `three_pointers` int(11) DEFAULT NULL,
  `three_pointer_attempts` int(11) DEFAULT NULL,
  `three_pointer_percentage` decimal(5,2) DEFAULT NULL,
  `free_throws` int(11) DEFAULT NULL,
  `free_throw_attempts` int(11) DEFAULT NULL,
  `free_throw_percentage` decimal(5,2) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `offensive_rebounds` int(11) DEFAULT NULL,
  `defensive_rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `personal_fouls` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_teamgamehalfstats__game_br_id__games__br_id` (`game_br_id`),
  KEY `fk_teamgamehalfstats__team_br_id__teams__br_id` (`team_br_id`),
  CONSTRAINT `fk_teamgamehalfstats__game_br_id__games__br_id` FOREIGN KEY (`game_br_id`) REFERENCES `games` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_teamgamehalfstats__team_br_id__teams__br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=156093 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teamgameovertimestats`
--

DROP TABLE IF EXISTS `teamgameovertimestats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teamgameovertimestats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `game_br_id` varchar(12) DEFAULT NULL,
  `team_br_id` char(3) DEFAULT NULL,
  `overtime` int(11) DEFAULT NULL,
  `minutes_played` int(11) DEFAULT NULL,
  `field_goals` int(11) DEFAULT NULL,
  `field_goal_attempts` int(11) DEFAULT NULL,
  `field_goal_percentage` decimal(5,2) DEFAULT NULL,
  `three_pointers` int(11) DEFAULT NULL,
  `three_pointer_attempts` int(11) DEFAULT NULL,
  `three_pointer_percentage` decimal(5,2) DEFAULT NULL,
  `free_throws` int(11) DEFAULT NULL,
  `free_throw_attempts` int(11) DEFAULT NULL,
  `free_throw_percentage` decimal(5,2) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `offensive_rebounds` int(11) DEFAULT NULL,
  `defensive_rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `personal_fouls` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_teamgameovertimestats__game_br_id__games__br_id` (`game_br_id`),
  KEY `fk_teamgameovertimestats__team_br_id__teams__br_id` (`team_br_id`),
  CONSTRAINT `fk_teamgameovertimestats__game_br_id__games__br_id` FOREIGN KEY (`game_br_id`) REFERENCES `games` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_teamgameovertimestats__team_br_id__teams__br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4965 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teamgamequarterstats`
--

DROP TABLE IF EXISTS `teamgamequarterstats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teamgamequarterstats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `game_br_id` varchar(12) DEFAULT NULL,
  `team_br_id` char(3) DEFAULT NULL,
  `quarter` int(11) DEFAULT NULL,
  `minutes_played` int(11) DEFAULT NULL,
  `field_goals` int(11) DEFAULT NULL,
  `field_goal_attempts` int(11) DEFAULT NULL,
  `field_goal_percentage` decimal(5,2) DEFAULT NULL,
  `three_pointers` int(11) DEFAULT NULL,
  `three_pointer_attempts` int(11) DEFAULT NULL,
  `three_pointer_percentage` decimal(5,2) DEFAULT NULL,
  `free_throws` int(11) DEFAULT NULL,
  `free_throw_attempts` int(11) DEFAULT NULL,
  `free_throw_percentage` decimal(5,2) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `offensive_rebounds` int(11) DEFAULT NULL,
  `defensive_rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `personal_fouls` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_teamgamequarterstats__game_br_id__games__br_id` (`game_br_id`),
  KEY `fk_teamgamequarterstats__team_br_id__teams__br_id` (`team_br_id`),
  CONSTRAINT `fk_teamgamequarterstats__game_br_id__games__br_id` FOREIGN KEY (`game_br_id`) REFERENCES `games` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_teamgamequarterstats__team_br_id__teams__br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=797921 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teamgamestats`
--

DROP TABLE IF EXISTS `teamgamestats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teamgamestats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `game_br_id` varchar(12) DEFAULT NULL,
  `team_br_id` char(3) DEFAULT NULL,
  `minutes_played` int(11) DEFAULT NULL,
  `field_goals` int(11) DEFAULT NULL,
  `field_goal_attempts` int(11) DEFAULT NULL,
  `field_goal_percentage` decimal(5,2) DEFAULT NULL,
  `three_pointers` int(11) DEFAULT NULL,
  `three_pointer_attempts` int(11) DEFAULT NULL,
  `three_pointer_percentage` decimal(5,2) DEFAULT NULL,
  `free_throws` int(11) DEFAULT NULL,
  `free_throw_attempts` int(11) DEFAULT NULL,
  `free_throw_percentage` decimal(5,2) DEFAULT NULL,
  `rebounds` int(11) DEFAULT NULL,
  `offensive_rebounds` int(11) DEFAULT NULL,
  `defensive_rebounds` int(11) DEFAULT NULL,
  `assists` int(11) DEFAULT NULL,
  `steals` int(11) DEFAULT NULL,
  `blocks` int(11) DEFAULT NULL,
  `turnovers` int(11) DEFAULT NULL,
  `personal_fouls` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL,
  `true_shooting_percentage` decimal(5,2) DEFAULT NULL,
  `effective_field_goal_percentage` decimal(5,2) DEFAULT NULL,
  `three_point_attempt_rate` decimal(4,3) DEFAULT NULL,
  `free_throw_attempt_rate` decimal(4,3) DEFAULT NULL,
  `offensive_rebound_percentage` decimal(5,2) DEFAULT NULL,
  `defensive_rebound_percentage` decimal(5,2) DEFAULT NULL,
  `total_rebound_percentage` decimal(5,2) DEFAULT NULL,
  `assist_percentage` decimal(5,2) DEFAULT NULL,
  `steal_percentage` decimal(5,2) DEFAULT NULL,
  `block_percentage` decimal(5,2) DEFAULT NULL,
  `turnover_percentage` decimal(5,2) DEFAULT NULL,
  `usage_percentage` decimal(5,2) DEFAULT NULL,
  `offensive_rating` int(11) DEFAULT NULL,
  `defensive_rating` int(11) DEFAULT NULL,
  `pace_factor` decimal(4,1) DEFAULT NULL,
  `ft_per_fga` decimal(4,3) DEFAULT NULL,
  `inactive_players` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_teamgamestats__game_br_id__games__br_id` (`game_br_id`),
  KEY `fk_teamgamestats__team_br_id__teams__br_id` (`team_br_id`),
  CONSTRAINT `fk_teamgamestats__game_br_id__games__br_id` FOREIGN KEY (`game_br_id`) REFERENCES `games` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_teamgamestats__team_br_id__teams__br_id` FOREIGN KEY (`team_br_id`) REFERENCES `teams` (`br_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=594058 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `br_id` char(3) DEFAULT NULL,
  `league` char(3) DEFAULT NULL,
  `season_start_year` char(4) DEFAULT NULL,
  `season_end_year` char(4) DEFAULT NULL,
  `location` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `br_id` (`br_id`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `webapp_webuser`
--

DROP TABLE IF EXISTS `webapp_webuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webapp_webuser` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `webapp_webuser_groups`
--

DROP TABLE IF EXISTS `webapp_webuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webapp_webuser_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `webuser_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `webapp_webuser_groups_webuser_id_group_id_cfabc1ce_uniq` (`webuser_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `webapp_webuser_user_permissions`
--

DROP TABLE IF EXISTS `webapp_webuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webapp_webuser_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `webuser_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `webapp_webuser_user_perm_webuser_id_permission_id_895323dc_uniq` (`webuser_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'bb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-22 23:23:39
