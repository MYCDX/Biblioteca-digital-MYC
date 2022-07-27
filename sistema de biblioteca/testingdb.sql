-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-07-2022 a las 21:13:35
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `testingdb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `accountss`
--

CREATE TABLE `accountss` (
  `id` int(11) NOT NULL,
  `fullname` varchar(200) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `accountss`
--

INSERT INTO `accountss` (`id`, `fullname`, `username`, `password`, `email`) VALUES
(34, 'lili dias perez', 'lili', 'lili', 'lili@gmail.com'),
(35, 'Ciro Isaias Quispe Navarro ', 'ciro', 'ciro', 'Navarrociro23072002@gmail.com'),
(36, 'Diaz Lujan, Petrov Anthony', 'diaz', 'diaz', 'diazlujan@gmai.com'),
(37, 'Tintaya Quispe, Evelun Lizzet', 'tintaya', 'tintaya', 'tintayaquispe@gmail.com'),
(38, 'Ito Quispe, Nataly Tania', 'ito', 'ito', 'itoquispe@gmail.com'),
(39, 'Danfer Alex Coyla Frores', 'danfer', 'danfer', 'danfer@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lib`
--

CREATE TABLE `lib` (
  `id_libro` int(11) NOT NULL,
  `libro` varchar(100) NOT NULL,
  `fecha` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `lib`
--

INSERT INTO `lib` (`id_libro`, `libro`, `fecha`) VALUES
(39, 'estadistica 1', '2022-07-25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `id` int(35) NOT NULL,
  `libros` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`id`, `libros`) VALUES
(1, 'informatica I'),
(2, 'introduccion a la informatica '),
(3, 'NFT'),
(4, 'introduccion a la computacion'),
(5, 'estadistica I'),
(6, 'estadistica 2'),
(7, 'estadistica'),
(8, 'estadistica inferencial');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos`
--

CREATE TABLE `prestamos` (
  `id` int(20) NOT NULL,
  `fecha_prestamo_libro` date NOT NULL,
  `fecha_entrga_libro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programacion`
--

CREATE TABLE `programacion` (
  `id_lib_usu` int(20) NOT NULL,
  `nom_lib_usu` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seemestre`
--

CREATE TABLE `seemestre` (
  `id_semes` int(10) NOT NULL,
  `semeste` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `accountss`
--
ALTER TABLE `accountss`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `lib`
--
ALTER TABLE `lib`
  ADD PRIMARY KEY (`id_libro`);

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `programacion`
--
ALTER TABLE `programacion`
  ADD PRIMARY KEY (`id_lib_usu`);

--
-- Indices de la tabla `seemestre`
--
ALTER TABLE `seemestre`
  ADD PRIMARY KEY (`id_semes`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `accountss`
--
ALTER TABLE `accountss`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT de la tabla `lib`
--
ALTER TABLE `lib`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id` int(35) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `programacion`
--
ALTER TABLE `programacion`
  MODIFY `id_lib_usu` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `seemestre`
--
ALTER TABLE `seemestre`
  MODIFY `id_semes` int(10) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
