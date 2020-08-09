SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `project` ;
CREATE SCHEMA IF NOT EXISTS `project` DEFAULT CHARACTER SET latin1 ;
USE `project` ;

-- -----------------------------------------------------
-- Table `project`.`assessment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project`.`assessment` ;

CREATE TABLE IF NOT EXISTS `project`.`assessment` (
  `id` INT(1) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `project`.`client`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project`.`client` ;

CREATE TABLE IF NOT EXISTS `project`.`client` (
  `idclient` VARCHAR(15) NOT NULL,
  `age` VARCHAR(45) NOT NULL,
  `gender` VARCHAR(45) NOT NULL,
  `education` VARCHAR(45) NOT NULL,
  `unemployed` VARCHAR(45) NOT NULL,
  `date` DATETIME NOT NULL,
  PRIMARY KEY (`idclient`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `project`.`staff`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project`.`staff` ;

CREATE TABLE IF NOT EXISTS `project`.`staff` (
  `idstaff` INT(2) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `role` ENUM('staff','admin') NOT NULL DEFAULT 'staff',
  PRIMARY KEY (`idstaff`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `project`.`vocation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project`.`vocation` ;

CREATE TABLE IF NOT EXISTS `project`.`vocation` (
  `id` INT(1) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `project`.`client_took_test`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project`.`client_took_test` ;

CREATE TABLE IF NOT EXISTS `project`.`client_took_test` (
  `id` INT(100) NOT NULL AUTO_INCREMENT,
  `idstaff` INT(2) NOT NULL,
  `idclient` VARCHAR(15) NOT NULL,
  `ass_id` INT(1) NOT NULL,
  `voc_id` INT(1) NOT NULL,
  `mskill` INT(2) NULL DEFAULT NULL,
  `pskill` INT(2) NULL DEFAULT NULL,
  `sskill` INT(2) NULL DEFAULT NULL,
  `pf` VARCHAR(45) NULL DEFAULT NULL,
  `total` INT(2) NULL DEFAULT NULL,
  `date` DATETIME NULL DEFAULT NULL,
  `aoi` VARCHAR(999) NULL DEFAULT NULL,
  `sa` VARCHAR(45) NULL DEFAULT NULL,
  `form` VARCHAR(999) NULL DEFAULT NULL,
  `sig` LONGTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_client_took_test_assessment_idx` (`ass_id` ASC),
  INDEX `fk_client_took_test_vocation1_idx` (`voc_id` ASC),
  INDEX `fk_client_took_test_client1_idx` (`idclient` ASC),
  INDEX `fk_client_took_test_staff1_idx` (`idstaff` ASC),
  CONSTRAINT `fk_client_took_test_assessment`
    FOREIGN KEY (`ass_id`)
    REFERENCES `project`.`assessment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_client_took_test_client1`
    FOREIGN KEY (`idclient`)
    REFERENCES `project`.`client` (`idclient`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_client_took_test_staff1`
    FOREIGN KEY (`idstaff`)
    REFERENCES `project`.`staff` (`idstaff`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_client_took_test_vocation1`
    FOREIGN KEY (`voc_id`)
    REFERENCES `project`.`vocation` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 90
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `project`.`pointdesc`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project`.`pointdesc` ;

CREATE TABLE IF NOT EXISTS `project`.`pointdesc` (
  `idname` VARCHAR(100) NOT NULL,
  `point` INT(1) NOT NULL,
  `description` VARCHAR(999) NOT NULL,
  PRIMARY KEY (`idname`, `point`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `project`.`client_has_point`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `project`.`client_has_point` ;

CREATE TABLE IF NOT EXISTS `project`.`client_has_point` (
  `idclient` VARCHAR(15) NOT NULL,
  `idname` VARCHAR(100) NOT NULL,
  `point` INT(1) NOT NULL,
  `test_no` INT(9) NOT NULL,
  PRIMARY KEY (`idclient`, `idname`, `point`, `test_no`),
  INDEX `fk_client_has_point_pointdesc1_idx` (`idname` ASC, `point` ASC),
  INDEX `fk_client_has_point_client_took_test1_idx` (`idclient` ASC),
  CONSTRAINT `fk_client_has_point_client_took_test1`
    FOREIGN KEY (`idclient`)
    REFERENCES `project`.`client_took_test` (`idclient`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_client_has_point_pointdesc1`
    FOREIGN KEY (`idname` , `point`)
    REFERENCES `project`.`pointdesc` (`idname` , `point`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `project`.`assessment`
-- -----------------------------------------------------
START TRANSACTION;
USE `project`;
INSERT INTO `project`.`assessment` (`id`, `name`) VALUES (1, 'New Assessment');
INSERT INTO `project`.`assessment` (`id`, `name`) VALUES (2, '3rd Month Assessment');

COMMIT;


-- -----------------------------------------------------
-- Data for table `project`.`staff`
-- -----------------------------------------------------
START TRANSACTION;
USE `project`;
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (1, 'Jayson Sudhasan', 'admin', 'admin');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (2, 'Bee See Roei', 'admin', 'admin');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (3, 'Li Zhong Ying', 'staff', 'staff');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (4, 'Cherie Choo Hui Ying', 'staff', 'staff');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (5, 'Evon Tze Wei Ping', 'staff', 'staff');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (6, 'Tan Hooi Chien Joylyn', 'staff', 'staff');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (7, 'Teh Chiu Ling', 'staff', 'staff');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (8, 'Cai Meizhen', 'staff', 'staff');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (9, 'Geraldine Tay Shu Ning', 'staff', 'staff');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (10, 'Jasper Tan Yingjun', 'staff', 'staff');
INSERT INTO `project`.`staff` (`idstaff`, `name`, `password`, `role`) VALUES (11, 'Catherine Tan Mui Moi', 'staff', 'staff');

COMMIT;


-- -----------------------------------------------------
-- Data for table `project`.`vocation`
-- -----------------------------------------------------
START TRANSACTION;
USE `project`;
INSERT INTO `project`.`vocation` (`id`, `name`) VALUES (1, 'Receptionist');
INSERT INTO `project`.`vocation` (`id`, `name`) VALUES (2, 'Retail');
INSERT INTO `project`.`vocation` (`id`, `name`) VALUES (3, 'F&B');
INSERT INTO `project`.`vocation` (`id`, `name`) VALUES (4, 'Cleaning');

COMMIT;


-- -----------------------------------------------------
-- Data for table `project`.`pointdesc`
-- -----------------------------------------------------
START TRANSACTION;
USE `project`;
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ac', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ac', 1, 'Poor attention span, requires > 4 prompts to maintain focus on task performance throughout assessment');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ac', 2, 'Fair attention span, requires 3-4 prompts to maintain focus on task performance throughout assessment');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ac', 3, 'Fair attention span, requires <= 2 prompts to maintain focus on task performance throughout assessment');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ac', 4, 'Good attention span, maintains focus on task performance throughout assessment without any prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('afbc', 1, 'Has certification of \"Fit for Open Employment\" from doctor');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('afbc', 2, 'Duration of training program is from minimum 1 month up to maximum 6 months. 1 month training probation at the start of the program. Duration of training program and probation will be reviewed if deemed beneficial by Occupational Therapist');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('afbc', 3, '$4.00 per hour of training incentives upon passing probation. NO TRAINING INCENTIVES will be provided during probation period. If you are found unsuitable, you will be further assessed by occupational therapist for a follow up plan. All training incentives must be claimed within 1 month of notification. You will not be able to claim your incentives after 1 month of last call contact from staff.');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('afbc', 4, '2 way trips of transport reimbursement on training days if eligible');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('afbc', 5, 'To attend monthly support group or other respective groups as scheuled by Occupational Therapist');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('afbc', 6, 'To follow up treatment with psychiatrist and comply with prescribed medications. You will be asked to withdraw from the training program if not compliant with medications and treatment follow up.');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('atd', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('atd', 1, 'Unable to accomplish the task in accurate and thorough manner. Product is of poor quality, most steps of task are done carelessly');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('atd', 2, 'Unable to accomplish the task in accurate and thorough manner. Product is of poor quality, some steps of task are done carelessly');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('atd', 3, 'Able to accomplish the task in accurate and thorough manner most of the time. Product is of acceptable quality, occasionally missing out some work details');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('atd', 4, 'Consistently able to accomplish the task in accurate and thorough manner. Product is of good quality, pays attention to fine work details');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('balance', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('balance', 1, 'Severe stabilizing skill that results in loss of balance and/or requires assistive devices/therapist intervention\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('balance', 2, 'Ineffective stabilizing skill to maintain various postures (standing, bending, squatting, stair climbing) whilst performing the tasks with loss of balance OR refuses to perform tasks in fear of loss of balance');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('balance', 3, 'Able to maintain various postures (standing, bending, squatting, stair climbing) with minimal form of support (leaning, using wall/floor, handrail) whilst performing the tasks but no evidence loss of balance\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('balance', 4, 'Consistently able to maintain various postures (standing, bending, squatting, stair climbing) whilst performing the tasks with no evidence loss of balance\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('bp', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('bp', 1, 'Ineffective body distance from task objects with moderate to severe awkward body positioning. May cause danger to the person or therapist intervention. Close supervision is needed to ensure safety. ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('bp', 2, 'Ineffective body distance from task obejcts with mild to moderate awkward body positioning. Disrupts task performance, increased clumsiness but safety may be compromised and prompt(s) is needed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('bp', 3, 'Able to maintain effective body distance from task objects with mild awkward body positioning. May disrupt task performance but safety is not compromised ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('bp', 4, 'Consistently able to maintain effective body distance from task objects without evidence of awkward body positioning');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('cas', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('cas', 1, 'Unclear and inaudible speech OR does not speak at all ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('cas', 2, 'Produces clear and audible speech sometimes. Displays loud volume, and/or slurring and/or mumbling speech which cannot be understood and requires further clarification. ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('cas', 3, 'Produces clear and audible speech most of the time. Displays loud volume, and/or slight slurring and/ or mumbling speech which can be understood with careful attention\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('cas', 4, 'Consistently produces clear and audible speech of appropriate volume\r\n\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ec', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ec', 1, 'Displays staring/fleeting/no eye contact but able to correct self with >4 prompts OR unable to correct self despite prompts given ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ec', 2, 'Displays staring/fleeting/no eye contact but able to correct self with 3-4 prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ec', 3, 'Displays staring/fleeting/no eye contact but able to correct self with <= 2 prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ec', 4, 'Consistently displays appropriate eye contact');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('fi', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('fi', 1, 'Requires > 4 prompts to perform task as instructed or unable to follow instructions at all');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('fi', 2, 'Requires 3-4  prompts to perform task as instructed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('fi', 3, 'Requires <= 2 prompts to perform task as instructed ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('fi', 4, 'Consistently able to perform task as instructed without any prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ft', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ft', 1, 'Unable to accept the mistake/problem/feedback despite therapist intervention and display negative behaviour and/or affect. May leave tasks incomplete');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ft', 2, 'Able to accept mistake/problem/feedback after therapist intervention and display negative behaviour and/or affect');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ft', 3, 'Able to accept mistake/problem/feedback and continue with tasks but displays negative behaviour and/or affect');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ft', 4, 'Able to accept mistake/problem/feedback appropriately at all the times');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('g', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('g', 1, 'Displays sexually suggestive/offensive behaviour ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('g', 2, 'Displays restlesssness/repetitive gesture/too much gesticulating but able to correct self with 3-4 prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('g', 3, 'Displays restlesssness/repetitive gesture/too much gesticulating but able to correct self with <= 2 prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('g', 4, 'Consistently displays appropriate gesture');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('inw', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('inw', 1, 'Requires > 4 prompts to move on to the next step and/or task OR unable to initiate the step/task at all');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('inw', 2, 'Requires 3-4 prompts to move on to the next step and/or task');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('inw', 3, 'Requires <= 2 prompts to move on to the next step and/or task ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('inw', 4, 'Consistently able to move on to the next step and/or task without any prompts ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('mc', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('mc', 1, 'Minimal responses and/or irrelevant responses most of the time. Difficult to engage in meaningful conversation\r\n\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('mc', 2, 'Does not allow turn taking and/or interrupt abruptly. Response can be irrelevant sometimes\r\n\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('mc', 3, 'Able to converse relevantly but shows delay in turn taking\r\n\r\n\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('mc', 4, 'Consistently able to converse relevantly and spontaneously\r\n\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('oa', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('oa', 1, 'Able to perform in a logical and efficient manner with > 4  prompts and/or leave the task >4 times to retrieve the items in a single task');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('oa', 2, 'Able to perform in a logical and efficient manner with 3-4 prompts and/or leave the task 3-4 times to retrieve the items in a single task');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('oa', 3, 'Able to perform in a logical and efficient manner with <= 2 prompts and/or leave the task <= 2 times to retrieve the items in a single task');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('oa', 4, 'Consistently able to perform in a logical and efficient manner with all the items needed close at hand to facilitate ease of performance for the tasks ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('pe', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('pe', 1, 'Consistently displays any physical symptoms such as giddiness/SOB/pain etc which require therapist intervention and result in incomplete assessment');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('pe', 2, '>= 3 breaks are required throughout assessment.  Most of the time appears fatigue, frequently need to sit down or show any physical symptoms such as giddiness/SOB/pain etc');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('pe', 3, '1-2 breaks are required throughout assessment.  Sometimes appears fatigue or may occasionally need to sit down');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('pe', 4, 'No breaks required throughout assessment');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ps', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ps', 1, 'Requires > 4 prompts to identify/recognise mistakes/problems that may arise and/or rectify it OR unable to identify or recognise mistakes/problems that may arise and requires therapist intervention to totally rectify it.\r ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ps', 2, 'Requires 3-4 prompts to identify/recognise mistakes/problems that may arise and/or rectify it');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ps', 3, 'Requires <= 2 prompts to identify/recognise mistakes/problems that may arise and/or rectify it.');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('ps', 4, 'Consistently able to identify/recognise mistakes/problems and rectify it without any prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('retail', 1, 'Has certification of \"Fit for Open Employment\" from doctor');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('retail', 2, 'Duration of training program is from minimum 1 month up to maximum 6 months. 1 month training probation at the start of the program. Duration of training program and probation will be reviewed if deemed beneficial by Occupational Therapist');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('retail', 3, '$3.00 per hour of training incentives upon passing probation. NO TRAINING INCENTIVES will be provided during probation period. If you are found unsuitable, you will be further assessed by occupational therapist for a follow up plan. All training incentives must be claimed within 1 month of notification. You will not be able to claim your incentives after 1 month of last call contact from staff.');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('retail', 4, '2 way trips of transport reimbursement on training days if eligible');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('retail', 5, 'To attend monthly support group or other respective groups as scheuled by Occupational Therapist');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('retail', 6, 'To follow up treatment with psychiatrist and comply with prescribed medications. You will be asked to withdraw from the training program if not compliant with medications and treatment follow up.');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sc', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sc', 1, 'Seek clarification with irrelevant and/or repeated questions most of the time or not asking question to clarify although situation warrants');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sc', 2, 'Seek clarification with irrelevant and/or repeated questions sometimes');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sc', 3, 'Seek clarification with relevant and different excessive or fewer number of questions ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sc', 4, 'Seek clarification with relevant and appropriate number of questions when necessary');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sd', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sd', 1, 'Displays too far or close social distancing but able to correct self with > 4 prompts OR unable to correct self despite therapist intervention');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sd', 2, 'Displays too far or close social distancing but able to correct self with 3-4 prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sd', 3, 'Displays too far or close social distancing but able to correct self with <= 2 prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('sd', 4, 'Consistently displays appropriate social distance ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('strength', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('strength', 1, 'Unable to carry 3 KG of object and moving/ambulating from one place to another place');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('strength', 2, 'Able to carry 3 KG of object (more than half of arm length) without moving/ambulating from one place to another place');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('strength', 3, 'Able to carry 3 KG of object from one place to another place (within room distance) with evidence of increased physical effort');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('strength', 4, 'Able to carry 3 KG of object from one place to another place (room to room distance) without evidence of increased physical effort');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tm', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tm', 1, 'Completes tasks > 15 minutes post allocated time');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tm', 2, 'Completes tasks <= 15 minutes post allocated time');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tm', 3, 'Completes tasks by allocated time');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tm', 4, 'Completes tasks before allocated time ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tot', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tot', 1, 'Requires > 4 prompts to terminate the step and/or task OR unable to terminate step/task at all ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tot', 2, 'Requires 3-4 prompts to terminate the step and/or task');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tot', 3, 'Requires <= 2 prompts to terminate the step and/or task ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('tot', 4, 'Consistently able to terminate the step and/or task without any prompts');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('usb', 0, 'Not assessed');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('usb', 1, 'Displays undesirable social behavior (impulsiveness, offensive, bizarre, aggressive, uncooperativeness) that causes the need for termination of assessment ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('usb', 2, 'Displays undesirable social behavior (impulsiveness, offensive, bizarre, aggressive, uncooperativeness). Not able to complete assessment despite prompts/breaks given\r \r ');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('usb', 3, 'Displays undesirable social behavior (impulsiveness/offensive/ bizarre/ aggressive/uncooperativeness). Able to complete the assessment with or without prompts/breaks given\r\n\r\n');
INSERT INTO `project`.`pointdesc` (`idname`, `point`, `description`) VALUES ('usb', 4, 'No undesirable social behavior (impulsiveness/offensive/bizarre/ aggressive/ uncooperativeness) displayed throughout the assessment ');

COMMIT;

