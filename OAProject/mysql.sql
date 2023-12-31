--
-- Create model Income
--
CREATE TABLE `OAUser_income` (`iId` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `iType` varchar(30) NOT NULL, `iMoney` numeric(10, 2) NOT NULL, `iRemark` varchar(55) NOT NULL, `iTime` date NOT NULL);
--
-- Create model Pay
--
CREATE TABLE `OAUser_pay` (`pId` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `pType` varchar(30) NOT NULL, `pMoney` numeric(10, 2) NOT NULL, `pRemark` varchar(55) NOT NULL, `pTime` date NOT NULL);
--
-- Create model Users
--
CREATE TABLE `OAUser_users` (`uid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `uname` varchar(30) NOT NULL, `upwd` varchar(30) NOT NULL UNIQUE, `usex` varchar(30) NOT NULL, `uemail` varchar(254) NOT NULL, `utel` bigint NOT NULL);
