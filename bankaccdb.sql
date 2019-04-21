


CREATE TABLE account(
	username varchar(500),
	dateofbirth varchar(50),
	ssn varchar(15),
	BankBalance int,
	PRIMARY KEY(username)
	
);

CREATE TABLE user(
	username varchar(50),
	password varchar(50),
	PRIMARY KEY(username),
	FOREIGN KEY (username) REFERENCES account(username) ON DELETE CASCADE
);

INSERT INTO `user` (`username`, `password`) VALUES ('aa', 'aa'), ('bb', 'bb');
INSERT INTO `account` (`username`, `dateofbirth`, `ssn`, `BankBalance`) VALUES ('aa', '01/01/2000', '111-111-1111', '4000'), ('bb', '01/01/2001', '111-111-11112', '400');
