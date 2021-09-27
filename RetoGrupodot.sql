-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema reto_grupodot
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema reto_grupodot
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `reto_grupodot` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `reto_grupodot` ;

-- -----------------------------------------------------
-- Table `reto_grupodot`.`Socio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reto_grupodot`.`Socio` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_Socio` VARCHAR(255) NOT NULL,
  `Tasa_interes` DOUBLE NOT NULL,
  `Monto_Max` DOUBLE NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `reto_grupodot`.`Prestamo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `reto_grupodot`.`Prestamo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idSocio_id` INT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  `cuota_mensual` DOUBLE NOT NULL,
  `pago_futuro` DOUBLE NOT NULL,
  `tasa_interes_m` DOUBLE NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `prestamo_idSocio_id` (`idSocio_id` ASC) VISIBLE,
  CONSTRAINT `Prestamo_ibfk_1`
    FOREIGN KEY (`idSocio_id`)
    REFERENCES `reto_grupodot`.`Socio` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
