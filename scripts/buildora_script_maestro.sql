-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: buildora_db
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `administracion_detalle`
--

DROP TABLE IF EXISTS `administracion_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administracion_detalle` (
  `id_administracion_detalle` int NOT NULL AUTO_INCREMENT,
  `id_administracion` int NOT NULL,
  `categoria` enum('personal_tecnico','personal_administrativo','ocupacional','dotacion_oficina','equipos','caja_menor','garantias','impuestos') COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `valor_unitario` decimal(16,2) NOT NULL DEFAULT '0.00',
  `dedicacion` decimal(8,4) NOT NULL DEFAULT '1.0000',
  `dias_proyectados` decimal(10,2) NOT NULL DEFAULT '0.00',
  `valor_total` decimal(16,2) NOT NULL DEFAULT '0.00',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_administracion_detalle`),
  KEY `idx_admin_detalle_admin` (`id_administracion`),
  KEY `idx_admin_detalle_categoria` (`categoria`),
  CONSTRAINT `fk_administracion_detalle` FOREIGN KEY (`id_administracion`) REFERENCES `administracion_presupuesto` (`id_administracion`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_admin_det_cantidad` CHECK ((`cantidad` >= 0)),
  CONSTRAINT `chk_admin_det_dedicacion` CHECK ((`dedicacion` >= 0)),
  CONSTRAINT `chk_admin_det_dias` CHECK ((`dias_proyectados` >= 0)),
  CONSTRAINT `chk_admin_det_total` CHECK ((`valor_total` >= 0)),
  CONSTRAINT `chk_admin_det_valor_unitario` CHECK ((`valor_unitario` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administracion_detalle`
--

LOCK TABLES `administracion_detalle` WRITE;
/*!40000 ALTER TABLE `administracion_detalle` DISABLE KEYS */;
/*!40000 ALTER TABLE `administracion_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administracion_presupuesto`
--

DROP TABLE IF EXISTS `administracion_presupuesto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administracion_presupuesto` (
  `id_administracion` int NOT NULL AUTO_INCREMENT,
  `id_presupuesto` int NOT NULL,
  `total_personal_tecnico` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_personal_administrativo` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_ocupacional` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_dotacion_oficina` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_equipos` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_caja_menor` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_garantias` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_impuestos` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_administracion` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_administracion` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_administracion`),
  UNIQUE KEY `uq_administracion_presupuesto` (`id_presupuesto`),
  KEY `idx_admin_presupuesto` (`id_presupuesto`),
  CONSTRAINT `fk_administracion_presupuesto` FOREIGN KEY (`id_presupuesto`) REFERENCES `presupuestos` (`id_presupuesto`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administracion_presupuesto`
--

LOCK TABLES `administracion_presupuesto` WRITE;
/*!40000 ALTER TABLE `administracion_presupuesto` DISABLE KEYS */;
/*!40000 ALTER TABLE `administracion_presupuesto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aiu_presupuesto`
--

DROP TABLE IF EXISTS `aiu_presupuesto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aiu_presupuesto` (
  `id_aiu` int NOT NULL AUTO_INCREMENT,
  `id_presupuesto` int NOT NULL,
  `costo_directo_total` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_administracion` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_administracion` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `total_imprevistos` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_imprevistos` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `total_utilidad` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_utilidad` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `iva_utilidad` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_iva_utilidad` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `total_aiu` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_total_aiu` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `valor_total_presupuesto` decimal(16,2) NOT NULL DEFAULT '0.00',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_aiu`),
  UNIQUE KEY `uq_aiu_presupuesto` (`id_presupuesto`),
  KEY `idx_aiu_presupuesto` (`id_presupuesto`),
  CONSTRAINT `fk_aiu_presupuesto` FOREIGN KEY (`id_presupuesto`) REFERENCES `presupuestos` (`id_presupuesto`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_aiu_costo_directo` CHECK ((`costo_directo_total` >= 0)),
  CONSTRAINT `chk_aiu_presupuesto_total` CHECK ((`valor_total_presupuesto` >= 0)),
  CONSTRAINT `chk_aiu_total` CHECK ((`total_aiu` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aiu_presupuesto`
--

LOCK TABLES `aiu_presupuesto` WRITE;
/*!40000 ALTER TABLE `aiu_presupuesto` DISABLE KEYS */;
/*!40000 ALTER TABLE `aiu_presupuesto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apu_herramientas`
--

DROP TABLE IF EXISTS `apu_herramientas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apu_herramientas` (
  `id_apu_herramienta` int NOT NULL AUTO_INCREMENT,
  `id_apu` int NOT NULL,
  `id_herramienta` int NOT NULL,
  `nombre_herramienta` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad_herramienta` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cantidad` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `valor_unitario` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `subtotal` decimal(14,2) NOT NULL DEFAULT '0.00',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_apu_herramienta`),
  KEY `idx_apu_herramientas_apu` (`id_apu`),
  KEY `idx_apu_herramientas_catalogo` (`id_herramienta`),
  CONSTRAINT `fk_apu_herramientas_apu` FOREIGN KEY (`id_apu`) REFERENCES `apus` (`id_apu`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_apu_herramientas_catalogo` FOREIGN KEY (`id_herramienta`) REFERENCES `herramientas` (`id_herramienta`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_apu_he_cantidad` CHECK ((`cantidad` >= 0)),
  CONSTRAINT `chk_apu_he_subtotal` CHECK ((`subtotal` >= 0)),
  CONSTRAINT `chk_apu_he_valor` CHECK ((`valor_unitario` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apu_herramientas`
--

LOCK TABLES `apu_herramientas` WRITE;
/*!40000 ALTER TABLE `apu_herramientas` DISABLE KEYS */;
/*!40000 ALTER TABLE `apu_herramientas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apu_mano_obra`
--

DROP TABLE IF EXISTS `apu_mano_obra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apu_mano_obra` (
  `id_apu_mano_obra` int NOT NULL AUTO_INCREMENT,
  `id_apu` int NOT NULL,
  `id_mano_obra` int NOT NULL,
  `nombre_cargo` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad_mano_obra` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cantidad` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `valor_unitario` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `subtotal` decimal(14,2) NOT NULL DEFAULT '0.00',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_apu_mano_obra`),
  KEY `idx_apu_mano_obra_apu` (`id_apu`),
  KEY `idx_apu_mano_obra_catalogo` (`id_mano_obra`),
  CONSTRAINT `fk_apu_mano_obra_apu` FOREIGN KEY (`id_apu`) REFERENCES `apus` (`id_apu`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_apu_mano_obra_catalogo` FOREIGN KEY (`id_mano_obra`) REFERENCES `mano_obra` (`id_mano_obra`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_apu_mo_cantidad` CHECK ((`cantidad` >= 0)),
  CONSTRAINT `chk_apu_mo_subtotal` CHECK ((`subtotal` >= 0)),
  CONSTRAINT `chk_apu_mo_valor` CHECK ((`valor_unitario` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apu_mano_obra`
--

LOCK TABLES `apu_mano_obra` WRITE;
/*!40000 ALTER TABLE `apu_mano_obra` DISABLE KEYS */;
/*!40000 ALTER TABLE `apu_mano_obra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apu_materiales`
--

DROP TABLE IF EXISTS `apu_materiales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apu_materiales` (
  `id_apu_material` int NOT NULL AUTO_INCREMENT,
  `id_apu` int NOT NULL,
  `id_material` int NOT NULL,
  `descripcion_material` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad_material` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cantidad` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `valor_unitario` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `subtotal` decimal(14,2) NOT NULL DEFAULT '0.00',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_apu_material`),
  KEY `idx_apu_materiales_apu` (`id_apu`),
  KEY `idx_apu_materiales_material` (`id_material`),
  CONSTRAINT `fk_apu_materiales_apu` FOREIGN KEY (`id_apu`) REFERENCES `apus` (`id_apu`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_apu_materiales_material` FOREIGN KEY (`id_material`) REFERENCES `materiales` (`id_material`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_apu_material_cantidad` CHECK ((`cantidad` >= 0)),
  CONSTRAINT `chk_apu_material_subtotal` CHECK ((`subtotal` >= 0)),
  CONSTRAINT `chk_apu_material_valor` CHECK ((`valor_unitario` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apu_materiales`
--

LOCK TABLES `apu_materiales` WRITE;
/*!40000 ALTER TABLE `apu_materiales` DISABLE KEYS */;
/*!40000 ALTER TABLE `apu_materiales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apus`
--

DROP TABLE IF EXISTS `apus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apus` (
  `id_apu` int NOT NULL AUTO_INCREMENT,
  `id_unidad` int NOT NULL,
  `codigo_apu` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad_base` decimal(14,4) NOT NULL DEFAULT '1.0000',
  `subtotal_materiales` decimal(14,2) NOT NULL DEFAULT '0.00',
  `subtotal_mano_obra` decimal(14,2) NOT NULL DEFAULT '0.00',
  `subtotal_herramientas` decimal(14,2) NOT NULL DEFAULT '0.00',
  `costo_directo_total` decimal(14,2) NOT NULL DEFAULT '0.00',
  `porcentaje_materiales` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_mano_obra` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_herramientas` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_apu`),
  UNIQUE KEY `codigo_apu` (`codigo_apu`),
  KEY `fk_apus_unidad` (`id_unidad`),
  KEY `idx_apus_codigo` (`codigo_apu`),
  KEY `idx_apus_descripcion` (`descripcion`),
  CONSTRAINT `fk_apus_unidad` FOREIGN KEY (`id_unidad`) REFERENCES `unidades_medida` (`id_unidad`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_apu_cantidad_base` CHECK ((`cantidad_base` > 0)),
  CONSTRAINT `chk_apu_costo_total` CHECK ((`costo_directo_total` >= 0)),
  CONSTRAINT `chk_apu_subtotal_herramientas` CHECK ((`subtotal_herramientas` >= 0)),
  CONSTRAINT `chk_apu_subtotal_mano_obra` CHECK ((`subtotal_mano_obra` >= 0)),
  CONSTRAINT `chk_apu_subtotal_materiales` CHECK ((`subtotal_materiales` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apus`
--

LOCK TABLES `apus` WRITE;
/*!40000 ALTER TABLE `apus` DISABLE KEYS */;
/*!40000 ALTER TABLE `apus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias_herramientas`
--

DROP TABLE IF EXISTS `categorias_herramientas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias_herramientas` (
  `id_categoria_herramienta` int NOT NULL AUTO_INCREMENT,
  `nombre_categoria` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  PRIMARY KEY (`id_categoria_herramienta`),
  UNIQUE KEY `nombre_categoria` (`nombre_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias_herramientas`
--

LOCK TABLES `categorias_herramientas` WRITE;
/*!40000 ALTER TABLE `categorias_herramientas` DISABLE KEYS */;
INSERT INTO `categorias_herramientas` VALUES (1,'Herramienta manual',NULL,'activo'),(2,'Herramienta eléctrica',NULL,'activo'),(3,'Herramienta menor',NULL,'activo'),(4,'Elemento de seguridad',NULL,'activo'),(5,'Equipo auxiliar',NULL,'activo');
/*!40000 ALTER TABLE `categorias_herramientas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias_materiales`
--

DROP TABLE IF EXISTS `categorias_materiales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias_materiales` (
  `id_categoria_material` int NOT NULL AUTO_INCREMENT,
  `nombre_categoria` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  PRIMARY KEY (`id_categoria_material`),
  UNIQUE KEY `nombre_categoria` (`nombre_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias_materiales`
--

LOCK TABLES `categorias_materiales` WRITE;
/*!40000 ALTER TABLE `categorias_materiales` DISABLE KEYS */;
INSERT INTO `categorias_materiales` VALUES (1,'Impermeabilizantes',NULL,'activo'),(2,'Pinturas',NULL,'activo'),(3,'Limpieza',NULL,'activo'),(4,'Concretos',NULL,'activo'),(5,'Cubiertas',NULL,'activo'),(6,'Mampostería',NULL,'activo'),(7,'Protección',NULL,'activo'),(8,'Enchapes',NULL,'activo'),(9,'Herramientas consumibles de obra',NULL,'activo');
/*!40000 ALTER TABLE `categorias_materiales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `tipo_cliente` enum('persona_natural','empresa_privada','entidad_publica') COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_cliente` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL,
  `identificacion` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `correo` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ciudad` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `herramientas`
--

DROP TABLE IF EXISTS `herramientas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `herramientas` (
  `id_herramienta` int NOT NULL AUTO_INCREMENT,
  `id_categoria_herramienta` int DEFAULT NULL,
  `id_unidad` int DEFAULT NULL,
  `codigo_herramienta` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_herramienta` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL,
  `valor_comercial` decimal(14,2) NOT NULL DEFAULT '0.00',
  `rendimiento` decimal(14,4) NOT NULL DEFAULT '1.0000',
  `numero_herramientas_obra` decimal(10,2) NOT NULL DEFAULT '1.00',
  `valor_hora` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `valor_por_obra` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_herramienta`),
  UNIQUE KEY `codigo_herramienta` (`codigo_herramienta`),
  KEY `fk_herramientas_categoria` (`id_categoria_herramienta`),
  KEY `fk_herramientas_unidad` (`id_unidad`),
  CONSTRAINT `fk_herramientas_categoria` FOREIGN KEY (`id_categoria_herramienta`) REFERENCES `categorias_herramientas` (`id_categoria_herramienta`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_herramientas_unidad` FOREIGN KEY (`id_unidad`) REFERENCES `unidades_medida` (`id_unidad`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_herramienta_numero` CHECK ((`numero_herramientas_obra` >= 0)),
  CONSTRAINT `chk_herramienta_rendimiento` CHECK ((`rendimiento` > 0)),
  CONSTRAINT `chk_herramienta_valor` CHECK ((`valor_comercial` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `herramientas`
--

LOCK TABLES `herramientas` WRITE;
/*!40000 ALTER TABLE `herramientas` DISABLE KEYS */;
/*!40000 ALTER TABLE `herramientas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imprevistos_detalle`
--

DROP TABLE IF EXISTS `imprevistos_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imprevistos_detalle` (
  `id_imprevisto_detalle` int NOT NULL AUTO_INCREMENT,
  `id_imprevisto` int NOT NULL,
  `id_capitulo` int DEFAULT NULL,
  `id_nivel_riesgo` int DEFAULT NULL,
  `tipo_imprevisto` enum('mano_obra_inactividad','incremento_materiales','riesgo_actividad','administracion') COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero_trabajadores` decimal(10,2) NOT NULL DEFAULT '0.00',
  `dias_inactividad` decimal(10,2) NOT NULL DEFAULT '0.00',
  `valor_dia_laboral` decimal(16,2) NOT NULL DEFAULT '0.00',
  `costo_base` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_aplicado` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `valor_total` decimal(16,2) NOT NULL DEFAULT '0.00',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_imprevisto_detalle`),
  KEY `idx_imprevisto_detalle_imprevisto` (`id_imprevisto`),
  KEY `idx_imprevisto_detalle_capitulo` (`id_capitulo`),
  KEY `idx_imprevisto_detalle_riesgo` (`id_nivel_riesgo`),
  CONSTRAINT `fk_imprevisto_detalle` FOREIGN KEY (`id_imprevisto`) REFERENCES `imprevistos_presupuesto` (`id_imprevisto`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_imprevisto_detalle_capitulo` FOREIGN KEY (`id_capitulo`) REFERENCES `presupuesto_capitulos` (`id_capitulo`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_imprevisto_detalle_riesgo` FOREIGN KEY (`id_nivel_riesgo`) REFERENCES `niveles_riesgo` (`id_nivel_riesgo`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_imp_costo_base` CHECK ((`costo_base` >= 0)),
  CONSTRAINT `chk_imp_dias` CHECK ((`dias_inactividad` >= 0)),
  CONSTRAINT `chk_imp_porcentaje` CHECK ((`porcentaje_aplicado` >= 0)),
  CONSTRAINT `chk_imp_total` CHECK ((`valor_total` >= 0)),
  CONSTRAINT `chk_imp_trabajadores` CHECK ((`numero_trabajadores` >= 0)),
  CONSTRAINT `chk_imp_valor_dia` CHECK ((`valor_dia_laboral` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imprevistos_detalle`
--

LOCK TABLES `imprevistos_detalle` WRITE;
/*!40000 ALTER TABLE `imprevistos_detalle` DISABLE KEYS */;
/*!40000 ALTER TABLE `imprevistos_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imprevistos_presupuesto`
--

DROP TABLE IF EXISTS `imprevistos_presupuesto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imprevistos_presupuesto` (
  `id_imprevisto` int NOT NULL AUTO_INCREMENT,
  `id_presupuesto` int NOT NULL,
  `total_imprevisto_mano_obra` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_imprevisto_materiales` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_imprevisto_riesgo` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_imprevisto_administracion` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_imprevistos` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_imprevistos` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_imprevisto`),
  UNIQUE KEY `uq_imprevistos_presupuesto` (`id_presupuesto`),
  KEY `idx_imprevisto_presupuesto` (`id_presupuesto`),
  CONSTRAINT `fk_imprevistos_presupuesto` FOREIGN KEY (`id_presupuesto`) REFERENCES `presupuestos` (`id_presupuesto`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imprevistos_presupuesto`
--

LOCK TABLES `imprevistos_presupuesto` WRITE;
/*!40000 ALTER TABLE `imprevistos_presupuesto` DISABLE KEYS */;
/*!40000 ALTER TABLE `imprevistos_presupuesto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mano_obra`
--

DROP TABLE IF EXISTS `mano_obra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mano_obra` (
  `id_mano_obra` int NOT NULL AUTO_INCREMENT,
  `id_parametro` int NOT NULL,
  `codigo_mano_obra` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_cargo` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad_smmlv` decimal(10,4) NOT NULL DEFAULT '1.0000',
  `tipo_contratacion` enum('prestacion_servicios','contrato_completo') COLLATE utf8mb4_unicode_ci NOT NULL,
  `salario_base` decimal(14,2) NOT NULL DEFAULT '0.00',
  `auxilio_transporte` decimal(14,2) NOT NULL DEFAULT '0.00',
  `salud` decimal(14,2) NOT NULL DEFAULT '0.00',
  `pension` decimal(14,2) NOT NULL DEFAULT '0.00',
  `arl` decimal(14,2) NOT NULL DEFAULT '0.00',
  `parafiscales` decimal(14,2) NOT NULL DEFAULT '0.00',
  `prima` decimal(14,2) NOT NULL DEFAULT '0.00',
  `cesantias` decimal(14,2) NOT NULL DEFAULT '0.00',
  `intereses_cesantias` decimal(14,2) NOT NULL DEFAULT '0.00',
  `total_contratacion` decimal(14,2) NOT NULL DEFAULT '0.00',
  `porcentaje_prestacional` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `dedicacion` decimal(8,4) NOT NULL DEFAULT '1.0000',
  `costo_dia` decimal(14,2) NOT NULL DEFAULT '0.00',
  `dias_proyectados` decimal(10,2) NOT NULL DEFAULT '0.00',
  `numero_trabajadores` decimal(10,2) NOT NULL DEFAULT '1.00',
  `valor_total` decimal(14,2) NOT NULL DEFAULT '0.00',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_mano_obra`),
  UNIQUE KEY `codigo_mano_obra` (`codigo_mano_obra`),
  KEY `fk_mano_obra_parametros` (`id_parametro`),
  CONSTRAINT `fk_mano_obra_parametros` FOREIGN KEY (`id_parametro`) REFERENCES `parametros_generales` (`id_parametro`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_mano_obra_dedicacion` CHECK ((`dedicacion` >= 0)),
  CONSTRAINT `chk_mano_obra_smmlv` CHECK ((`cantidad_smmlv` >= 0)),
  CONSTRAINT `chk_mano_obra_trabajadores` CHECK ((`numero_trabajadores` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mano_obra`
--

LOCK TABLES `mano_obra` WRITE;
/*!40000 ALTER TABLE `mano_obra` DISABLE KEYS */;
/*!40000 ALTER TABLE `mano_obra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materiales`
--

DROP TABLE IF EXISTS `materiales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materiales` (
  `id_material` int NOT NULL AUTO_INCREMENT,
  `id_categoria_material` int DEFAULT NULL,
  `id_unidad` int NOT NULL,
  `codigo_material` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `valor_comercial_empaque` decimal(14,2) NOT NULL DEFAULT '0.00',
  `cantidad_por_empaque` decimal(14,4) NOT NULL DEFAULT '1.0000',
  `precio_por_unidad` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `rendimiento` decimal(14,4) NOT NULL DEFAULT '1.0000',
  `unidad_cotizacion` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `valor_por_unidad_cotizacion` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_desperdicio` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `valor_desperdicio` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `valor_total` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_material`),
  UNIQUE KEY `codigo_material` (`codigo_material`),
  KEY `fk_materiales_categoria` (`id_categoria_material`),
  KEY `fk_materiales_unidad` (`id_unidad`),
  CONSTRAINT `fk_materiales_categoria` FOREIGN KEY (`id_categoria_material`) REFERENCES `categorias_materiales` (`id_categoria_material`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_materiales_unidad` FOREIGN KEY (`id_unidad`) REFERENCES `unidades_medida` (`id_unidad`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_material_cantidad_empaque` CHECK ((`cantidad_por_empaque` > 0)),
  CONSTRAINT `chk_material_desperdicio` CHECK ((`porcentaje_desperdicio` >= 0)),
  CONSTRAINT `chk_material_rendimiento` CHECK ((`rendimiento` > 0)),
  CONSTRAINT `chk_material_valor_comercial` CHECK ((`valor_comercial_empaque` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materiales`
--

LOCK TABLES `materiales` WRITE;
/*!40000 ALTER TABLE `materiales` DISABLE KEYS */;
/*!40000 ALTER TABLE `materiales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `niveles_riesgo`
--

DROP TABLE IF EXISTS `niveles_riesgo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `niveles_riesgo` (
  `id_nivel_riesgo` int NOT NULL AUTO_INCREMENT,
  `codigo_riesgo` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_riesgo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `porcentaje_riesgo` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  PRIMARY KEY (`id_nivel_riesgo`),
  UNIQUE KEY `codigo_riesgo` (`codigo_riesgo`),
  CONSTRAINT `chk_nivel_riesgo_porcentaje` CHECK ((`porcentaje_riesgo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `niveles_riesgo`
--

LOCK TABLES `niveles_riesgo` WRITE;
/*!40000 ALTER TABLE `niveles_riesgo` DISABLE KEYS */;
INSERT INTO `niveles_riesgo` VALUES (1,'R0','Riesgo 0',0.0000,'Nulo nivel de imprevistos por actividad concreta','activo'),(2,'RI','Riesgo I',0.0100,'Bajo nivel de imprevistos por actividad concreta','activo'),(3,'RII','Riesgo II',0.0300,'Nivel intermedio de imprevistos por actividad concreta','activo'),(4,'RIII','Riesgo III',0.0500,'Alto nivel de imprevistos por actividad concreta','activo'),(5,'RIV','Riesgo IV',0.0700,'Muy alto nivel de imprevistos por actividad concreta','activo');
/*!40000 ALTER TABLE `niveles_riesgo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parametros_generales`
--

DROP TABLE IF EXISTS `parametros_generales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parametros_generales` (
  `id_parametro` int NOT NULL AUTO_INCREMENT,
  `nombre_version` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `smmlv` decimal(14,2) NOT NULL,
  `auxilio_transporte` decimal(14,2) NOT NULL DEFAULT '0.00',
  `porcentaje_salud` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_pension` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_arl` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_parafiscales` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_prima` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_cesantias` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_intereses_cesantias` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_iva` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_retefuente` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `porcentaje_renta` decimal(6,4) NOT NULL DEFAULT '0.0000',
  `vigente_desde` date NOT NULL,
  `vigente_hasta` date DEFAULT NULL,
  `es_actual` tinyint(1) NOT NULL DEFAULT '1',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_parametro`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parametros_generales`
--

LOCK TABLES `parametros_generales` WRITE;
/*!40000 ALTER TABLE `parametros_generales` DISABLE KEYS */;
INSERT INTO `parametros_generales` VALUES (1,'Parámetros base 2026',1300000.00,162000.00,0.0850,0.1200,0.0696,0.0900,0.0833,0.0833,0.0100,0.1900,0.0200,0.3500,'2026-01-01',NULL,1,'activo','2026-06-06 14:59:38','2026-06-06 14:59:38');
/*!40000 ALTER TABLE `parametros_generales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presupuesto_capitulos`
--

DROP TABLE IF EXISTS `presupuesto_capitulos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presupuesto_capitulos` (
  `id_capitulo` int NOT NULL AUTO_INCREMENT,
  `id_presupuesto` int NOT NULL,
  `codigo_capitulo` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_capitulo` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `orden` int NOT NULL DEFAULT '1',
  `costo_total_capitulo` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_participacion` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_capitulo`),
  UNIQUE KEY `uq_capitulo_presupuesto_codigo` (`id_presupuesto`,`codigo_capitulo`),
  KEY `idx_capitulos_presupuesto` (`id_presupuesto`),
  KEY `idx_capitulos_codigo` (`codigo_capitulo`),
  CONSTRAINT `fk_capitulos_presupuesto` FOREIGN KEY (`id_presupuesto`) REFERENCES `presupuestos` (`id_presupuesto`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_capitulo_costo` CHECK ((`costo_total_capitulo` >= 0)),
  CONSTRAINT `chk_capitulo_orden` CHECK ((`orden` > 0)),
  CONSTRAINT `chk_capitulo_porcentaje` CHECK ((`porcentaje_participacion` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presupuesto_capitulos`
--

LOCK TABLES `presupuesto_capitulos` WRITE;
/*!40000 ALTER TABLE `presupuesto_capitulos` DISABLE KEYS */;
/*!40000 ALTER TABLE `presupuesto_capitulos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presupuesto_item_herramientas_hist`
--

DROP TABLE IF EXISTS `presupuesto_item_herramientas_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presupuesto_item_herramientas_hist` (
  `id_item_herramienta_hist` int NOT NULL AUTO_INCREMENT,
  `id_item` int NOT NULL,
  `id_herramienta` int DEFAULT NULL,
  `codigo_herramienta` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nombre_herramienta` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad_herramienta` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cantidad` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `valor_unitario` decimal(16,4) NOT NULL DEFAULT '0.0000',
  `subtotal` decimal(16,2) NOT NULL DEFAULT '0.00',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_item_herramienta_hist`),
  KEY `fk_item_he_hist_herramienta` (`id_herramienta`),
  KEY `idx_item_he_hist_item` (`id_item`),
  CONSTRAINT `fk_item_he_hist_herramienta` FOREIGN KEY (`id_herramienta`) REFERENCES `herramientas` (`id_herramienta`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_item_he_hist_item` FOREIGN KEY (`id_item`) REFERENCES `presupuesto_items` (`id_item`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_item_he_hist_cantidad` CHECK ((`cantidad` >= 0)),
  CONSTRAINT `chk_item_he_hist_subtotal` CHECK ((`subtotal` >= 0)),
  CONSTRAINT `chk_item_he_hist_valor` CHECK ((`valor_unitario` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presupuesto_item_herramientas_hist`
--

LOCK TABLES `presupuesto_item_herramientas_hist` WRITE;
/*!40000 ALTER TABLE `presupuesto_item_herramientas_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `presupuesto_item_herramientas_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presupuesto_item_mano_obra_hist`
--

DROP TABLE IF EXISTS `presupuesto_item_mano_obra_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presupuesto_item_mano_obra_hist` (
  `id_item_mano_obra_hist` int NOT NULL AUTO_INCREMENT,
  `id_item` int NOT NULL,
  `id_mano_obra` int DEFAULT NULL,
  `codigo_mano_obra` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nombre_cargo` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad_mano_obra` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cantidad` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `valor_unitario` decimal(16,4) NOT NULL DEFAULT '0.0000',
  `subtotal` decimal(16,2) NOT NULL DEFAULT '0.00',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_item_mano_obra_hist`),
  KEY `fk_item_mo_hist_mano_obra` (`id_mano_obra`),
  KEY `idx_item_mo_hist_item` (`id_item`),
  CONSTRAINT `fk_item_mo_hist_item` FOREIGN KEY (`id_item`) REFERENCES `presupuesto_items` (`id_item`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_item_mo_hist_mano_obra` FOREIGN KEY (`id_mano_obra`) REFERENCES `mano_obra` (`id_mano_obra`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_item_mo_hist_cantidad` CHECK ((`cantidad` >= 0)),
  CONSTRAINT `chk_item_mo_hist_subtotal` CHECK ((`subtotal` >= 0)),
  CONSTRAINT `chk_item_mo_hist_valor` CHECK ((`valor_unitario` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presupuesto_item_mano_obra_hist`
--

LOCK TABLES `presupuesto_item_mano_obra_hist` WRITE;
/*!40000 ALTER TABLE `presupuesto_item_mano_obra_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `presupuesto_item_mano_obra_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presupuesto_item_materiales_hist`
--

DROP TABLE IF EXISTS `presupuesto_item_materiales_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presupuesto_item_materiales_hist` (
  `id_item_material_hist` int NOT NULL AUTO_INCREMENT,
  `id_item` int NOT NULL,
  `id_material` int DEFAULT NULL,
  `codigo_material` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion_material` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad_material` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cantidad` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `valor_unitario` decimal(16,4) NOT NULL DEFAULT '0.0000',
  `subtotal` decimal(16,2) NOT NULL DEFAULT '0.00',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_item_material_hist`),
  KEY `fk_item_material_hist_material` (`id_material`),
  KEY `idx_item_material_hist_item` (`id_item`),
  CONSTRAINT `fk_item_material_hist_item` FOREIGN KEY (`id_item`) REFERENCES `presupuesto_items` (`id_item`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_item_material_hist_material` FOREIGN KEY (`id_material`) REFERENCES `materiales` (`id_material`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_item_material_hist_cantidad` CHECK ((`cantidad` >= 0)),
  CONSTRAINT `chk_item_material_hist_subtotal` CHECK ((`subtotal` >= 0)),
  CONSTRAINT `chk_item_material_hist_valor` CHECK ((`valor_unitario` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presupuesto_item_materiales_hist`
--

LOCK TABLES `presupuesto_item_materiales_hist` WRITE;
/*!40000 ALTER TABLE `presupuesto_item_materiales_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `presupuesto_item_materiales_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presupuesto_items`
--

DROP TABLE IF EXISTS `presupuesto_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presupuesto_items` (
  `id_item` int NOT NULL AUTO_INCREMENT,
  `id_capitulo` int NOT NULL,
  `id_apu` int NOT NULL,
  `codigo_item` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion_item` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad_item` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad` decimal(14,4) NOT NULL DEFAULT '0.0000',
  `costo_unitario_historico` decimal(16,2) NOT NULL DEFAULT '0.00',
  `costo_total_item` decimal(16,2) NOT NULL DEFAULT '0.00',
  `codigo_apu_historico` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion_apu_historica` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unidad_apu_historica` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subtotal_materiales_historico` decimal(16,2) NOT NULL DEFAULT '0.00',
  `subtotal_mano_obra_historico` decimal(16,2) NOT NULL DEFAULT '0.00',
  `subtotal_herramientas_historico` decimal(16,2) NOT NULL DEFAULT '0.00',
  `orden` int NOT NULL DEFAULT '1',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_item`),
  UNIQUE KEY `uq_item_capitulo_codigo` (`id_capitulo`,`codigo_item`),
  KEY `idx_items_capitulo` (`id_capitulo`),
  KEY `idx_items_apu` (`id_apu`),
  KEY `idx_items_codigo` (`codigo_item`),
  CONSTRAINT `fk_items_apu` FOREIGN KEY (`id_apu`) REFERENCES `apus` (`id_apu`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_items_capitulo` FOREIGN KEY (`id_capitulo`) REFERENCES `presupuesto_capitulos` (`id_capitulo`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_item_cantidad` CHECK ((`cantidad` >= 0)),
  CONSTRAINT `chk_item_costo_total` CHECK ((`costo_total_item` >= 0)),
  CONSTRAINT `chk_item_costo_unitario` CHECK ((`costo_unitario_historico` >= 0)),
  CONSTRAINT `chk_item_orden` CHECK ((`orden` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presupuesto_items`
--

LOCK TABLES `presupuesto_items` WRITE;
/*!40000 ALTER TABLE `presupuesto_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `presupuesto_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presupuestos`
--

DROP TABLE IF EXISTS `presupuestos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presupuestos` (
  `id_presupuesto` int NOT NULL AUTO_INCREMENT,
  `id_proyecto` int NOT NULL,
  `id_usuario_creador` int NOT NULL,
  `codigo_presupuesto` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_presupuesto` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `fecha_presupuesto` date NOT NULL,
  `costo_directo_total` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_administracion` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_imprevistos` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_utilidad` decimal(16,2) NOT NULL DEFAULT '0.00',
  `iva_utilidad` decimal(16,2) NOT NULL DEFAULT '0.00',
  `valor_total_presupuesto` decimal(16,2) NOT NULL DEFAULT '0.00',
  `estado` enum('borrador','activo','cerrado','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'borrador',
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_presupuesto`),
  UNIQUE KEY `codigo_presupuesto` (`codigo_presupuesto`),
  UNIQUE KEY `uq_presupuesto_proyecto` (`id_proyecto`),
  KEY `fk_presupuestos_usuario` (`id_usuario_creador`),
  KEY `idx_presupuestos_proyecto` (`id_proyecto`),
  KEY `idx_presupuestos_codigo` (`codigo_presupuesto`),
  KEY `idx_presupuestos_estado` (`estado`),
  CONSTRAINT `fk_presupuestos_proyectos` FOREIGN KEY (`id_proyecto`) REFERENCES `proyectos` (`id_proyecto`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_presupuestos_usuario` FOREIGN KEY (`id_usuario_creador`) REFERENCES `usuarios` (`id_usuario`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_presupuesto_costos` CHECK ((`costo_directo_total` >= 0)),
  CONSTRAINT `chk_presupuesto_total` CHECK ((`valor_total_presupuesto` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presupuestos`
--

LOCK TABLES `presupuestos` WRITE;
/*!40000 ALTER TABLE `presupuestos` DISABLE KEYS */;
/*!40000 ALTER TABLE `presupuestos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proyectos`
--

DROP TABLE IF EXISTS `proyectos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proyectos` (
  `id_proyecto` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `codigo_proyecto` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_proyecto` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ubicacion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_proyecto` date DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `estado` enum('activo','inactivo','cerrado') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_proyecto`),
  UNIQUE KEY `codigo_proyecto` (`codigo_proyecto`),
  KEY `fk_proyectos_clientes` (`id_cliente`),
  CONSTRAINT `fk_proyectos_clientes` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proyectos`
--

LOCK TABLES `proyectos` WRITE;
/*!40000 ALTER TABLE `proyectos` DISABLE KEYS */;
/*!40000 ALTER TABLE `proyectos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre_rol` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_rol`),
  UNIQUE KEY `nombre_rol` (`nombre_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Administrador','Usuario con acceso completo al sistema','activo','2026-06-06 14:59:37','2026-06-06 14:59:37'),(2,'Presupuestador','Usuario encargado de elaborar APUs, presupuestos y reportes','activo','2026-06-06 14:59:37','2026-06-06 14:59:37');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidades_medida`
--

DROP TABLE IF EXISTS `unidades_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidades_medida` (
  `id_unidad` int NOT NULL AUTO_INCREMENT,
  `codigo_unidad` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_unidad` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  PRIMARY KEY (`id_unidad`),
  UNIQUE KEY `codigo_unidad` (`codigo_unidad`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_medida`
--

LOCK TABLES `unidades_medida` WRITE;
/*!40000 ALTER TABLE `unidades_medida` DISABLE KEYS */;
INSERT INTO `unidades_medida` VALUES (1,'UN','Unidad',NULL,'activo'),(2,'M2','Metro cuadrado',NULL,'activo'),(3,'M3','Metro cúbico',NULL,'activo'),(4,'ML','Metro lineal',NULL,'activo'),(5,'KG','Kilogramo',NULL,'activo'),(6,'GL','Galón',NULL,'activo'),(7,'LT','Litro',NULL,'activo'),(8,'HR','Hora',NULL,'activo'),(9,'DIA','Día',NULL,'activo');
/*!40000 ALTER TABLE `unidades_medida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `id_rol` int NOT NULL,
  `nombres` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellidos` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usuario` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activo',
  `ultimo_acceso` datetime DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `fk_usuarios_roles` (`id_rol`),
  CONSTRAINT `fk_usuarios_roles` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilidad_presupuesto`
--

DROP TABLE IF EXISTS `utilidad_presupuesto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilidad_presupuesto` (
  `id_utilidad` int NOT NULL AUTO_INCREMENT,
  `id_presupuesto` int NOT NULL,
  `porcentaje_utilidad_operativa` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `utilidad_operativa` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_retefuente` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `valor_retefuente` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_renta` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `valor_renta` decimal(16,2) NOT NULL DEFAULT '0.00',
  `total_utilidad` decimal(16,2) NOT NULL DEFAULT '0.00',
  `porcentaje_iva_utilidad` decimal(8,4) NOT NULL DEFAULT '0.0000',
  `iva_utilidad` decimal(16,2) NOT NULL DEFAULT '0.00',
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_utilidad`),
  UNIQUE KEY `uq_utilidad_presupuesto` (`id_presupuesto`),
  KEY `idx_utilidad_presupuesto` (`id_presupuesto`),
  CONSTRAINT `fk_utilidad_presupuesto` FOREIGN KEY (`id_presupuesto`) REFERENCES `presupuestos` (`id_presupuesto`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_utilidad_iva` CHECK ((`iva_utilidad` >= 0)),
  CONSTRAINT `chk_utilidad_porcentaje` CHECK ((`porcentaje_utilidad_operativa` >= 0)),
  CONSTRAINT `chk_utilidad_total` CHECK ((`total_utilidad` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilidad_presupuesto`
--

LOCK TABLES `utilidad_presupuesto` WRITE;
/*!40000 ALTER TABLE `utilidad_presupuesto` DISABLE KEYS */;
/*!40000 ALTER TABLE `utilidad_presupuesto` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-07  9:05:47
