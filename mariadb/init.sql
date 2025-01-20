CREATE TABLE Users (
  email varchar(255) PRIMARY KEY,
  name varchar(25) NOT NULL,
  last_name varchar(50) NOT NULL,
  hashed_password TEXT NOT NULL
);

CREATE TABLE Posts (
  post_id INT AUTO_INCREMENT PRIMARY KEY,
  title varchar(100) NOT NULL,
  description varchar(1000) NOT NULL,
  post_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_sold BOOLEAN DEFAULT false,
  user_email varchar(255),
  FOREIGN KEY (user_email) REFERENCES Users(email)
);

CREATE TABLE Vehicles (
  license_plate varchar(20) PRIMARY KEY,
  brand varchar(20),
  model varchar(20),
  registration_year INT(4) NOT NULL,
  price DOUBLE,
  observations varchar(1000),
  vehicle_type varchar(25) NOT NULL,
  fuel_type varchar(25) NOT NULL,
  photo LONGBLOB,
  post_id INT,
  FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);