-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 07, 2024 at 05:12 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `namkeen`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `profile` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `name`, `email`, `password`, `profile`) VALUES
('b4f2f53d-f79d-4c9c-9', 'KanoSojitra', 'kano@gmail.com', '3eef87363e2ffb31bf490b2dafc2c3c9f7a25662', '02.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` varchar(20) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `product_id` varchar(20) NOT NULL,
  `price` int(10) NOT NULL,
  `qty` int(2) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `id` varchar(20) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `number` varchar(255) NOT NULL,
  `message` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`id`, `user_id`, `name`, `email`, `number`, `message`) VALUES
('', 'e5744934-c578-4bc0-8', 'Niraj Sojitra', 'nirajsojitra11@gmail.com', '06351505351', 'best namkeen');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` varchar(20) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `number` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(255) NOT NULL,
  `address_type` varchar(10) NOT NULL,
  `method` varchar(50) NOT NULL,
  `product_id` varchar(20) NOT NULL,
  `price` int(10) NOT NULL,
  `qty` varchar(2) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(50) NOT NULL,
  `payment_status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `name`, `number`, `email`, `address`, `address_type`, `method`, `product_id`, `price`, `qty`, `date`, `status`, `payment_status`) VALUES
('337a4d36-9931-11ef-b', 'e5744934-c578-4bc0-8', 'Yami', '7865435678', 'nirajsojitra11@gmail.com', 'near bus station, d, hariyasan, India, 360410', 'home', 'cash on delivery', '3e4e132b-ff13-4e0e-a', 60, '2', '2024-11-02', 'canceled', ''),
('1327f87a-9933-11ef-b', 'e5744934-c578-4bc0-8', 'Krish', '6351505351', 'nirajsojitra11@gmail.com', 'near bus station, 1, hariyasan, India, 360410', 'home', 'cash on delivery', 'ab100c3e-35bf-4867-a', 90, '1', '2024-11-02', 'pending', ''),
('132e7392-9933-11ef-b', 'e5744934-c578-4bc0-8', 'Krish', '6351505351', 'nirajsojitra11@gmail.com', 'near bus station, 1, hariyasan, India, 360410', 'home', 'cash on delivery', 'c14733ca-79cb-476a-a', 50, '1', '2024-11-02', 'complete', 'complete'),
('27c763b9-9936-11ef-b', 'e5744934-c578-4bc0-8', 'Niraj Sojitra', '5', 'nirajsojitra11@gmail.com', 'near bus station, 1, hariyasan, India, 360410', 'home', 'cash on delivery', '2df5e190-2d0a-4d45-b', 60, '1', '2024-11-02', 'pending', '');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` varchar(20) NOT NULL,
  `name` varchar(250) NOT NULL,
  `wheight` int(10) NOT NULL,
  `price` int(50) NOT NULL,
  `image` varchar(255) NOT NULL,
  `product_details` varchar(1000) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `wheight`, `price`, `image`, `product_details`, `status`) VALUES
('c14733ca-79cb-476a-a', 'methi khakhra', 200, 50, 'methikhakhra.png', 'Methi Khakhra is a crispy, thin, savory snack made from whole wheat flour and dried fenugreek (methi) leaves. It offers a healthy, flavorful crunch, perfect for light snacking.', 'deactive'),
('37dc033e-6d99-4406-b', 'Masala Khakhra', 200, 50, 'masalakhakhra.png', 'Masala Khakhra is a crunchy, thin Indian snack made from whole wheat flour and spices. It’s roasted to perfection, offering a flavorful, spicy taste perfect for quick, healthy munching.', 'active'),
('b1ac7445-41c0-48a3-9', 'Ratlami Sev', 250, 60, 'ratlami.png', 'Ratlami sev is a spicy, crunchy snack from Ratlam, Madhya Pradesh. Made from gram flour (besan) and flavored with spices like cloves and pepper, it\'s known for its distinct, tangy taste.', 'active'),
('2df5e190-2d0a-4d45-b', 'Tikha Gathiya', 250, 60, 'tikhagathiya.png', 'Tikha gathiya is a spicy, crunchy snack from Gujarat made with gram flour dough, flavored with chili powder and ajwain. It is deep-fried and enjoyed with chutney.', 'active'),
('e043fb0e-d000-48e8-9', 'Fulvadi', 250, 70, 'fulvadi.png', 'Fulvadi is a crunchy, savory Indian snack made from chickpea flour, spices, and sesame seeds. It\'s deep-fried into sticks or rolls and has a spicy, tangy flavor with a crisp texture.', 'active'),
('3e4e132b-ff13-4e0e-a', 'Moli Papdi', 250, 60, 'molipapadi.png', '\r\nMoli papadi is a light, crispy', 'active'),
('7e5dfc19-ea91-404f-8', 'chakkari', 250, 60, 'chakkari.png', 'Chakkari, a traditional Indian sweet, is a delightful treat made from rice flour, jaggery, and coconut, often flavored with cardamom. It’s typically steamed and enjoyed during festivals and celebrations.', 'active'),
('6624918a-94e7-4f78-9', 'Masala Papadi', 250, 60, 'masalapapadi.png', 'Masala papadi is a crispy', 'active'),
('f10d85d1-df00-4a28-b', 'Tumtum', 250, 60, 'tumtum.png', 'Tumtum Gathiya is a delicious Indian snack made from gram flour, seasoned with spices, and fried to a crispy perfection. Enjoy its savory crunch as a delightful accompaniment to tea or coffee.', 'active'),
('24ec65dc-4bfe-4b3e-b', 'Methipuri', 250, 60, 'methipuri.png', 'Methipuri is a delectable Indian snack made from whole wheat flour, stuffed with a spiced mixture of fenugreek leaves and spices, and then deep-fried until golden brown and crispy. Enjoy it with chutney!', 'active'),
('12ec7738-4833-4a3e-b', 'Moli Bundi', 250, 60, 'molibundi.png', 'Moli Bundi is a delightful Indian snack made from gram flour and spices, shaped into crispy, crunchy balls. Perfect for tea time or as a savory treat, it offers a unique taste experience.', 'active'),
('ab100c3e-35bf-4867-a', 'Cholafali', 200, 90, 'cholafali.png', 'Cholafali is a delicious South Indian dish made from a mix of crispy fried lentils, spices, and herbs. Perfect as a snack or appetizer, it’s flavorful and satisfying for all occasions.', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `user_type` varchar(100) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `user_type`) VALUES
('e5744934-c578-4bc0-8', 'Kano Sojitra', 'kano@gmail.com', 'kano', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `id` varchar(20) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `product_id` varchar(20) NOT NULL,
  `price` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wishlist`
--

INSERT INTO `wishlist` (`id`, `user_id`, `product_id`, `price`) VALUES
('28ea56dd-ffd6-4591-b', 'e5744934-c578-4bc0-8', '2df5e190-2d0a-4d45-b', 60),
('058edaa3-41a1-4958-b', 'e5744934-c578-4bc0-8', '37dc033e-6d99-4406-b', 50),
('b9c0774d-9030-4dbf-b', 'e5744934-c578-4bc0-8', '6624918a-94e7-4f78-9', 60);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
