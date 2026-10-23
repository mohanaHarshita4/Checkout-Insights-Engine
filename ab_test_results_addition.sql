-- =====================================================
-- A/B TEST RESULTS TABLE
-- Values recomputed directly from the notebook datasets.
-- True p values for all three tests are smaller than
-- DECIMAL(12,10) can store (about 2e-13, 1.2e-72, 7.1e-47),
-- so each is stored as the smallest representable value.
-- =====================================================

USE ecommerce_analytics;

DROP TABLE IF EXISTS ABTestResults;

CREATE TABLE ABTestResults (
    TestID          INT AUTO_INCREMENT PRIMARY KEY,
    TestName        VARCHAR(100) NOT NULL,
    GroupAName      VARCHAR(100) NOT NULL,
    GroupAMetric    DECIMAL(6,4) NOT NULL,
    GroupASize      INT NOT NULL,
    GroupBName      VARCHAR(100) NOT NULL,
    GroupBMetric    DECIMAL(6,4) NOT NULL,
    GroupBSize      INT NOT NULL,
    ChiSquare       DECIMAL(8,2) NOT NULL,
    PValue          DECIMAL(12,10) NOT NULL,
    IsSignificant   BOOLEAN NOT NULL,
    Recommendation  VARCHAR(255),
    DataSource      ENUM('real','simulated') NOT NULL
);

INSERT INTO ABTestResults
    (TestName, GroupAName, GroupAMetric, GroupASize, GroupBName, GroupBMetric, GroupBSize, ChiSquare, PValue, IsSignificant, Recommendation, DataSource)
VALUES
    -- Real Kaggle dataset, 588,101 users, unbalanced 96/4 split
    ('Ad vs PSA Exposure',
     'PSA (control)', 0.0179, 23524,
     'Ad (treatment)', 0.0255, 564577,
     54.01, 0.0000000001, TRUE, 'Ship the change', 'real'),

    ('Guest Checkout vs Forced Signup',
     'Forced signup', 0.4222, 5000,
     'Guest checkout', 0.6026, 5000,
     324.92, 0.0000000001, TRUE, 'Ship the change', 'simulated'),

    ('Short vs Long Checkout Form',
     'Long form', 0.4978, 5000,
     'Short form', 0.6404, 5000,
     206.73, 0.0000000001, TRUE, 'Ship the change', 'simulated');

-- Verify:
-- SELECT * FROM ABTestResults;
