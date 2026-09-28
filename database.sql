CREATE TABLE jobs (id INT_INCREMENT PRIMARY KEY, title VARCHAR(255), description TEXT, required_skills TEXT);
CREATE TABLE resumes (id INT AUTO_INCREMENT PRIMERY KEY,file_name VARCHAR(255), raw_text LONGTEXT);
CREATE TABLE rankings (id AUTO_INCREMENT PRIMERY KEY, job_id INT, resume_id INT , score INT , matched_skills TEXT , missing_skills TEXT);