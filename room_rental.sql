-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 12, 2021 at 10:17 AM
-- Server version: 8.0.27-0ubuntu0.20.04.1
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `room_rental`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` varchar(20) DEFAULT NULL,
  `admin_password` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `admin_password`) VALUES
('admin@gmail.com', 'admin@123');

-- --------------------------------------------------------

--
-- Table structure for table `flat_types`
--

CREATE TABLE `flat_types` (
  `flat_id` varchar(25) DEFAULT NULL,
  `flat_name` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `flat_types`
--

INSERT INTO `flat_types` (`flat_id`, `flat_name`) VALUES
('flat1636261637218448', '1 BHK'),
('flat16362616419350414', '2 BHK'),
('flat1636261646000407', '3 BHK');

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `order_id` varchar(30) NOT NULL,
  `room_id` varchar(30) DEFAULT NULL,
  `user_id` varchar(30) DEFAULT NULL,
  `joining_date` varchar(20) DEFAULT NULL,
  `booking_date` varchar(20) DEFAULT NULL,
  `leaving_date` varchar(20) DEFAULT NULL,
  `trxn_id` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `history`
--

INSERT INTO `history` (`order_id`, `room_id`, `user_id`, `joining_date`, `booking_date`, `leaving_date`, `trxn_id`) VALUES
('order16365593716164472', 'room16363025225972493', 'user16363040256597939', '18-11-2021', '10-11-2021', '18-06-2022', 'dfnjskffdjmfdgjfd'),
('order16365596831568065', 'room16363025225972493', 'user16363040256597939', '24-11-2021', '10-11-2021', '24-06-2022', 'dfnjskffdjmfdgjfd');

-- --------------------------------------------------------

--
-- Table structure for table `room_types`
--

CREATE TABLE `room_types` (
  `flat_id` varchar(25) DEFAULT NULL,
  `room_id` varchar(25) DEFAULT NULL,
  `room_desc` varchar(500) DEFAULT NULL,
  `room_img` varchar(1000) DEFAULT NULL,
  `room_price` int DEFAULT NULL,
  `room_add` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `room_types`
--

INSERT INTO `room_types` (`flat_id`, `room_id`, `room_desc`, `room_img`, `room_price`, `room_add`) VALUES
('flat1636261637218448', 'room16363025225972493', 'jnm', '9249_U53Gnvy.png', 534, 'jn'),
('flat16362616419350414', 'room1636606116807153', 'this isnsdm', 'IMG_20210813_111917.jpg', 7838, 'jdffjwnj'),
('flat16362616419350414', 'room16366061714819489', 'fgdnjn', '9249 (1).png', 678, 'jnjnlj');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` varchar(30) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `createdAt` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `name`, `email`, `mobile`, `password`, `status`, `createdAt`) VALUES
('user16363040256597939', 'Abhsihek', 'akaushal451@gmail.com', '810322', 'Abhi@123', 0, '16363040256598072'),
('user1636304058152915', 'Abhsihek', 'akaushal451@gmail.com', '810322', 'Abhi@123', 0, '16363040581529286'),
('user16363040817495918', 'Abhsihek', 'akaushal451@gmail.com', '810322', 'Abhi@123', 0, '1636304081749603'),
('user16364731911131406', 'Aman', 'aman@gmail.com', '35894584', 'Aman@123', 0, '16364731911131835'),
('user16364732937812412', 'anshul', 'anshul@gmail.com', '', 'Anshul@123', 0, '16364732937812648'),
('user16364733557548337', 'gagan', 'gagan@gmail.com', '39435345', 'Gagan@123', 0, '16364733557548425'),
('user16364734527705503', 'aaksh', 'akash@gmail.com', '34852', 'Aakash@123', 0, '16364734527705617');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`order_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
