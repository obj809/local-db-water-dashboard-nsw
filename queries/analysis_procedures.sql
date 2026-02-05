-- queries/analysis_procedures.sql
-- Stored procedures for calculating dam analysis metrics
-- Run this file to create/update the procedures and scheduled event

DELIMITER //

-- =============================================================================
-- Procedure: calculate_specific_dam_analysis
-- Calculates rolling averages for each dam individually
-- =============================================================================
DROP PROCEDURE IF EXISTS calculate_specific_dam_analysis//

CREATE PROCEDURE calculate_specific_dam_analysis()
BEGIN
    DECLARE v_analysis_date DATE;

    -- Analysis date is the last day of the previous month
    SET v_analysis_date = LAST_DAY(DATE_SUB(CURDATE(), INTERVAL 1 MONTH));

    INSERT INTO specific_dam_analysis (
        dam_id,
        analysis_date,
        avg_storage_volume_12_months,
        avg_storage_volume_5_years,
        avg_storage_volume_10_years,
        avg_percentage_full_12_months,
        avg_percentage_full_5_years,
        avg_percentage_full_10_years,
        avg_storage_inflow_12_months,
        avg_storage_inflow_5_years,
        avg_storage_inflow_10_years,
        avg_storage_release_12_months,
        avg_storage_release_5_years,
        avg_storage_release_10_years
    )
    SELECT
        d.dam_id,
        v_analysis_date,
        -- 12 month averages
        (SELECT ROUND(AVG(r.storage_volume), 3)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 12 MONTH)),
        -- 5 year averages
        (SELECT ROUND(AVG(r.storage_volume), 3)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 5 YEAR)),
        -- 10 year averages
        (SELECT ROUND(AVG(r.storage_volume), 3)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 10 YEAR)),
        -- percentage_full
        (SELECT ROUND(AVG(r.percentage_full), 2)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 12 MONTH)),
        (SELECT ROUND(AVG(r.percentage_full), 2)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 5 YEAR)),
        (SELECT ROUND(AVG(r.percentage_full), 2)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 10 YEAR)),
        -- storage_inflow
        (SELECT ROUND(AVG(r.storage_inflow), 3)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 12 MONTH)),
        (SELECT ROUND(AVG(r.storage_inflow), 3)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 5 YEAR)),
        (SELECT ROUND(AVG(r.storage_inflow), 3)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 10 YEAR)),
        -- storage_release
        (SELECT ROUND(AVG(r.storage_release), 3)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 12 MONTH)),
        (SELECT ROUND(AVG(r.storage_release), 3)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 5 YEAR)),
        (SELECT ROUND(AVG(r.storage_release), 3)
         FROM dam_resources r
         WHERE r.dam_id = d.dam_id
         AND r.date > DATE_SUB(v_analysis_date, INTERVAL 10 YEAR))
    FROM dams d
    ON DUPLICATE KEY UPDATE
        avg_storage_volume_12_months = VALUES(avg_storage_volume_12_months),
        avg_storage_volume_5_years = VALUES(avg_storage_volume_5_years),
        avg_storage_volume_10_years = VALUES(avg_storage_volume_10_years),
        avg_percentage_full_12_months = VALUES(avg_percentage_full_12_months),
        avg_percentage_full_5_years = VALUES(avg_percentage_full_5_years),
        avg_percentage_full_10_years = VALUES(avg_percentage_full_10_years),
        avg_storage_inflow_12_months = VALUES(avg_storage_inflow_12_months),
        avg_storage_inflow_5_years = VALUES(avg_storage_inflow_5_years),
        avg_storage_inflow_10_years = VALUES(avg_storage_inflow_10_years),
        avg_storage_release_12_months = VALUES(avg_storage_release_12_months),
        avg_storage_release_5_years = VALUES(avg_storage_release_5_years),
        avg_storage_release_10_years = VALUES(avg_storage_release_10_years);

    SELECT CONCAT('specific_dam_analysis: inserted/updated ', ROW_COUNT(), ' rows for ', v_analysis_date) AS result;
END//


-- =============================================================================
-- Procedure: calculate_overall_dam_analysis
-- Calculates system-wide rolling averages across all dams
-- =============================================================================
DROP PROCEDURE IF EXISTS calculate_overall_dam_analysis//

CREATE PROCEDURE calculate_overall_dam_analysis()
BEGIN
    DECLARE v_analysis_date DATE;

    -- Analysis date is the last day of the previous month
    SET v_analysis_date = LAST_DAY(DATE_SUB(CURDATE(), INTERVAL 1 MONTH));

    INSERT INTO overall_dam_analysis (
        analysis_date,
        avg_storage_volume_12_months,
        avg_storage_volume_5_years,
        avg_storage_volume_10_years,
        avg_percentage_full_12_months,
        avg_percentage_full_5_years,
        avg_percentage_full_10_years,
        avg_storage_inflow_12_months,
        avg_storage_inflow_5_years,
        avg_storage_inflow_10_years,
        avg_storage_release_12_months,
        avg_storage_release_5_years,
        avg_storage_release_10_years
    )
    SELECT
        v_analysis_date,
        -- 12 month averages
        (SELECT ROUND(AVG(r.storage_volume), 3)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 12 MONTH)),
        -- 5 year averages
        (SELECT ROUND(AVG(r.storage_volume), 3)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 5 YEAR)),
        -- 10 year averages
        (SELECT ROUND(AVG(r.storage_volume), 3)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 10 YEAR)),
        -- percentage_full
        (SELECT ROUND(AVG(r.percentage_full), 2)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 12 MONTH)),
        (SELECT ROUND(AVG(r.percentage_full), 2)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 5 YEAR)),
        (SELECT ROUND(AVG(r.percentage_full), 2)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 10 YEAR)),
        -- storage_inflow
        (SELECT ROUND(AVG(r.storage_inflow), 3)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 12 MONTH)),
        (SELECT ROUND(AVG(r.storage_inflow), 3)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 5 YEAR)),
        (SELECT ROUND(AVG(r.storage_inflow), 3)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 10 YEAR)),
        -- storage_release
        (SELECT ROUND(AVG(r.storage_release), 3)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 12 MONTH)),
        (SELECT ROUND(AVG(r.storage_release), 3)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 5 YEAR)),
        (SELECT ROUND(AVG(r.storage_release), 3)
         FROM dam_resources r
         WHERE r.date > DATE_SUB(v_analysis_date, INTERVAL 10 YEAR))
    ON DUPLICATE KEY UPDATE
        avg_storage_volume_12_months = VALUES(avg_storage_volume_12_months),
        avg_storage_volume_5_years = VALUES(avg_storage_volume_5_years),
        avg_storage_volume_10_years = VALUES(avg_storage_volume_10_years),
        avg_percentage_full_12_months = VALUES(avg_percentage_full_12_months),
        avg_percentage_full_5_years = VALUES(avg_percentage_full_5_years),
        avg_percentage_full_10_years = VALUES(avg_percentage_full_10_years),
        avg_storage_inflow_12_months = VALUES(avg_storage_inflow_12_months),
        avg_storage_inflow_5_years = VALUES(avg_storage_inflow_5_years),
        avg_storage_inflow_10_years = VALUES(avg_storage_inflow_10_years),
        avg_storage_release_12_months = VALUES(avg_storage_release_12_months),
        avg_storage_release_5_years = VALUES(avg_storage_release_5_years),
        avg_storage_release_10_years = VALUES(avg_storage_release_10_years);

    SELECT CONCAT('overall_dam_analysis: inserted/updated 1 row for ', v_analysis_date) AS result;
END//


-- =============================================================================
-- Procedure: calculate_dam_analysis
-- Main entry point - calls both specific and overall analysis
-- Use this for manual triggers: CALL calculate_dam_analysis();
-- =============================================================================
DROP PROCEDURE IF EXISTS calculate_dam_analysis//

CREATE PROCEDURE calculate_dam_analysis()
BEGIN
    CALL calculate_specific_dam_analysis();
    CALL calculate_overall_dam_analysis();
    SELECT 'Dam analysis calculation complete' AS status;
END//

DELIMITER ;


-- =============================================================================
-- Event: monthly_dam_analysis
-- Runs on the 1st of each month at 12:00 PM
-- =============================================================================

-- Enable the event scheduler (requires SUPER privilege or event_scheduler=ON in my.cnf)
SET GLOBAL event_scheduler = ON;

-- Drop existing event if it exists
DROP EVENT IF EXISTS monthly_dam_analysis;

-- Create the scheduled event
CREATE EVENT monthly_dam_analysis
ON SCHEDULE EVERY 1 MONTH
STARTS '2026-03-01 12:00:00'
ON COMPLETION PRESERVE
ENABLE
COMMENT 'Monthly calculation of dam analysis metrics'
DO
    CALL calculate_dam_analysis();
