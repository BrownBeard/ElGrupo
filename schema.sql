DROP TABLE IF EXISTS `answers`;
CREATE TABLE `answers` (
  `a_id` int(10) unsigned NOT NULL auto_increment,
  `q_id` int(10) unsigned NOT NULL,
  `answer` varchar(64) NOT NULL,
  `correct` tinyint(1) NOT NULL,
  PRIMARY KEY  (`a_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `facts`;
CREATE TABLE `facts` (
  `f_id` int(10) unsigned NOT NULL auto_increment,
  `g_id` int(10) unsigned NOT NULL,
  `fact` varchar(512) NOT NULL,
  PRIMARY KEY  (`f_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `games`;
CREATE TABLE `games` (
  `g_id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(64) NOT NULL,
  `filename` varchar(64) NOT NULL,
  PRIMARY KEY  (`g_id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `filename` (`filename`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `questions`;
CREATE TABLE `questions` (
  `q_id` int(10) unsigned NOT NULL auto_increment,
  `g_id` int(10) unsigned NOT NULL,
  `question` varchar(128) NOT NULL,
  PRIMARY KEY  (`q_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;
