

CREATE DATABASE lianjiadata DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE lianjiadata
CREATE TABLE `lianjiadata` (
  `id` int identity,

  `title` text,

  `description` text,

  `link` text ,

) ENGINE=MyISAM DEFAULT CHARSET=utf8;

 CREATE TABLE lianjiahistory(id INT UNSIGNED AUTO_INCREMENT,link text,title text,decription text,PRIMARY KEY ( `id` )) ENGINE=MyISAM DEFAULT CHARSET=utf8;


CREATE TABLE lianjiahistory(id INT UNSIGNED AUTO_INCREMENT,title text,door_model text,size int,direction text,strike_price int, deal_date text,deal_duration int,community text, PRIMARY KEY ( `id` )) ENGINE=MyISAM DEFAULT CHARSET=utf8;
