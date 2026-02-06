# ************************************************************
# Sequel Ace SQL dump
# Versione 20096
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# Host: localhost (MySQL 9.5.0)
# Database: GestioneSpese
# Tempo Di Generazione: 2026-02-06 16:30:40 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump della tabella budget
# ------------------------------------------------------------

DROP TABLE IF EXISTS `budget`;

CREATE TABLE `budget` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `mese` char(7) NOT NULL,
  `categoria_id` int unsigned NOT NULL,
  `importo` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_budget` (`mese`,`categoria_id`),
  KEY `fk_budget_categoria` (`categoria_id`),
  CONSTRAINT `fk_budget_categoria` FOREIGN KEY (`categoria_id`) REFERENCES `categorie` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_budget_importo` CHECK ((`importo` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `budget` WRITE;
/*!40000 ALTER TABLE `budget` DISABLE KEYS */;

INSERT INTO `budget` (`id`, `mese`, `categoria_id`, `importo`)
VALUES
	(1,'2026-02',1,50.00),
	(4,'2026-02',11,60.00),
	(5,'2026-02',15,150.00),
	(6,'2026-02',16,150.00),
	(7,'2026-02',17,100.00),
	(8,'2026-02',22,150.00);

/*!40000 ALTER TABLE `budget` ENABLE KEYS */;
UNLOCK TABLES;


# Dump della tabella categorie
# ------------------------------------------------------------

DROP TABLE IF EXISTS `categorie`;

CREATE TABLE `categorie` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_categoria_nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `categorie` WRITE;
/*!40000 ALTER TABLE `categorie` DISABLE KEYS */;

INSERT INTO `categorie` (`id`, `nome`)
VALUES
	(15,'abbigliamento'),
	(1,'Alimentari'),
	(17,'cartoleria'),
	(14,'Istruzione'),
	(22,'musica'),
	(18,'passatempo'),
	(13,'Salute'),
	(16,'shopping'),
	(11,'Svago'),
	(2,'Trasporti');

/*!40000 ALTER TABLE `categorie` ENABLE KEYS */;
UNLOCK TABLES;


# Dump della tabella spese
# ------------------------------------------------------------

DROP TABLE IF EXISTS `spese`;

CREATE TABLE `spese` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `data` date NOT NULL,
  `importo` decimal(10,2) NOT NULL,
  `categoria_id` int unsigned NOT NULL,
  `descrizione` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_spese_categoria` (`categoria_id`),
  CONSTRAINT `fk_spese_categoria` FOREIGN KEY (`categoria_id`) REFERENCES `categorie` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_importo` CHECK ((`importo` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `spese` WRITE;
/*!40000 ALTER TABLE `spese` DISABLE KEYS */;

INSERT INTO `spese` (`id`, `data`, `importo`, `categoria_id`, `descrizione`)
VALUES
	(1,'2026-02-01',10.00,1,'pane'),
	(2,'2026-02-01',5.00,1,NULL),
	(3,'2026-02-01',30.00,1,NULL),
	(4,'2026-02-01',45.00,11,'cinema'),
	(5,'2026-02-01',40.00,14,'Libro universitario'),
	(6,'2026-02-02',60.00,15,'acquisto maglietta'),
	(7,'2026-02-02',60.00,16,'acquisto maglietta'),
	(8,'2026-02-02',49.99,17,'acquisto diario'),
	(9,'2026-02-02',60.00,18,'nuoto'),
	(10,'2026-02-02',99.00,18,'nuoto'),
	(11,'2026-02-06',50.00,22,'microfono');

/*!40000 ALTER TABLE `spese` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
