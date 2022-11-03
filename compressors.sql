-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Хост: localhost:3306
-- Время создания: Ноя 03 2022 г., 20:50
-- Версия сервера: 10.3.32-MariaDB-cll-lve
-- Версия PHP: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `mtk_compressor`
--

-- --------------------------------------------------------

--
-- Структура таблицы `compressors`
--

CREATE TABLE `compressors` (
  `id` int(7) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `date_reg` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `date_edit` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Просто так';

--
-- Дамп данных таблицы `compressors`
--

INSERT INTO `compressors` (`id`, `name`, `email`, `date_reg`, `date_edit`) VALUES
(1, 'dali', 'dali@mail.com', '2022-04-10 15:01:02', '2022-04-17 15:01:40'),
(2, 'comprag', 'comprag@mail.ru', '2022-04-22 15:01:02', '2022-04-09 15:01:40'),
(3, 'remeza', 'remeza@mail.ru', '2022-04-20 15:03:12', '2022-04-09 15:03:51'),
(4, 'berg', 'dali@mail.com', '2022-04-11 15:01:02', '2022-04-28 15:01:40'),
(5, 'bort', 'bort@mail.com', '2022-04-11 15:01:02', '2022-04-28 15:01:40'),
(6, '34t3dr', 'fcfgcgfc@hkbyuh.by', '2022-10-10 20:58:58', '2022-10-17 20:58:58'),
(7, '34t3dr', 'fcfgcgfc@hkbyuh.by', '2022-10-10 20:58:58', '2022-10-17 20:58:58');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `compressors`
--
ALTER TABLE `compressors`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Add` (`id`,`name`),
  ADD UNIQUE KEY `565` (`id`),
  ADD KEY `email` (`email`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `compressors`
--
ALTER TABLE `compressors`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
