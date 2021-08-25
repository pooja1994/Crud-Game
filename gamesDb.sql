CREATE DATABASE `game_database` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `games1` (
  `id` bigint DEFAULT NULL,
  `title` text,
  `platform` text,
  `score` double DEFAULT NULL,
  `genre` text,
  `editors_choice` text,
  KEY `ix_games_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `users` (
  `user_id` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;