DROP TABLE IF EXISTS CardUsageHistory;
DROP TABLE IF EXISTS TransactionHistory;

CREATE TABLE CustomerAccount (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    RegistrationDate DATE NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,
    SSN VARCHAR(20) NOT NULL,
    AccountNumber VARCHAR(20) NOT NULL UNIQUE,
    Balance DECIMAL(15, 2) DEFAULT 0
);

CREATE TABLE TransactionHistory (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    AccountNumber VARCHAR(20) NOT NULL,
    TransactionType ENUM('입금', '출금') NOT NULL,
    TransactionDate DATE NOT NULL,
    TransactionTime TIME NOT NULL,
    Amount DECIMAL(15, 2) NOT NULL,
    Description VARCHAR(255)
);

CREATE TABLE CardUsageHistory (
    CardUsageID INT AUTO_INCREMENT PRIMARY KEY,
    AccountNumber VARCHAR(20) NOT NULL,
    UsageDate DATE NOT NULL,
    UsageTime TIME NOT NULL,
    Amount DECIMAL(15, 2) NOT NULL,
    MerchantName VARCHAR(100) NOT NULL
);

INSERT INTO CustomerAccount (Name, RegistrationDate, PhoneNumber, SSN, AccountNumber, Balance)
VALUES
('김유나', '2023-01-15', '010-1234-5678', '901010-1234567', 'ACC001', 0),
('이민호', '2023-02-20', '010-2345-6789', '910210-2345678', 'ACC002', 0),
('박지훈', '2023-03-10', '010-3456-7890', '920310-3456789', 'ACC003', 0),
('최수영', '2023-04-05', '010-4567-8901', '930405-4567890', 'ACC004', 0),
('정호석', '2023-05-25', '010-5678-9012', '940525-5678901', 'ACC005', 0);

INSERT INTO TransactionHistory (AccountNumber, TransactionType, TransactionDate, TransactionTime, Amount, Description)
VALUES
('ACC001', '입금', '2024-08-01', '10:15:00', 500000, '월급 입금'),
('ACC001', '출금', '2024-08-02', '14:20:00', 100000, 'ATM 출금'),
('ACC001', '입금', '2024-08-03', '09:10:00', 200000, '프리랜스 작업비'),
('ACC001', '출금', '2024-08-04', '12:30:00', 50000, '식료품 구매'),
('ACC001', '입금', '2024-08-05', '16:45:00', 150000, '선물 돈'),
('ACC001', '출금', '2024-08-06', '19:00:00', 70000, '레스토랑 결제'),
('ACC002', '입금', '2024-08-01', '08:30:00', 300000, '프로젝트 입금'),
('ACC002', '출금', '2024-08-02', '11:00:00', 50000, '주유소 결제'),
('ACC002', '입금', '2024-08-03', '13:25:00', 200000, '보너스 지급'),
('ACC002', '출금', '2024-08-04', '17:15:00', 60000, '의류 매장 결제'),
('ACC002', '입금', '2024-08-05', '15:00:00', 250000, '프리랜스 작업비'),
('ACC002', '출금', '2024-08-06', '20:45:00', 80000, '저녁 식사 결제'),
('ACC003', '입금', '2024-08-01', '07:00:00', 450000, '월급 입금'),
('ACC003', '출금', '2024-08-02', '09:30:00', 120000, '슈퍼마켓 결제'),
('ACC003', '입금', '2024-08-03', '10:45:00', 300000, '컨설팅 비용'),
('ACC003', '출금', '2024-08-04', '18:10:00', 150000, '전자 제품 구매'),
('ACC003', '입금', '2024-08-05', '14:30:00', 200000, '저축 이체'),
('ACC003', '출금', '2024-08-06', '21:00:00', 90000, '공과금 납부'),
('ACC004', '입금', '2024-08-01', '11:00:00', 350000, '월급 입금'),
('ACC004', '출금', '2024-08-02', '12:30:00', 50000, 'ATM 출금'),
('ACC004', '입금', '2024-08-03', '14:45:00', 250000, '투자 수익'),
('ACC004', '출금', '2024-08-04', '16:30:00', 60000, '서점 결제'),
('ACC004', '입금', '2024-08-05', '18:20:00', 300000, '선물 돈'),
('ACC004', '출금', '2024-08-06', '19:50:00', 70000, '영화관 결제'),
('ACC005', '입금', '2024-08-01', '08:00:00', 400000, '월급 입금'),
('ACC005', '출금', '2024-08-02', '10:20:00', 200000, '가전제품 구매'),
('ACC005', '입금', '2024-08-03', '11:15:00', 100000, '부업 수익'),
('ACC005', '출금', '2024-08-04', '13:40:00', 80000, '식료품 구매'),
('ACC005', '입금', '2024-08-05', '09:00:00', 500000, '프리랜스 프로젝트'),
('ACC005', '출금', '2024-08-06', '17:45:00', 30000, '선물 구매'),
('ACC001', '입금', '2024-08-07', '09:10:00', 150000, '파트타임 일'),
('ACC001', '출금', '2024-08-08', '14:00:00', 200000, '보험료 납부'),
('ACC001', '입금', '2024-08-09', '11:20:00', 250000, '컨설팅 비용'),
('ACC001', '출금', '2024-08-10', '15:30:00', 50000, '오락비 지출'),
('ACC002', '입금', '2024-08-07', '10:00:00', 100000, '프리랜스 작업비'),
('ACC002', '출금', '2024-08-08', '13:30:00', 30000, '커피숍 결제'),
('ACC002', '입금', '2024-08-09', '16:10:00', 200000, '프로젝트 입금'),
('ACC002', '출금', '2024-08-10', '18:25:00', 60000, '의류 매장 결제'),
('ACC003', '입금', '2024-08-07', '07:30:00', 250000, '컨설팅 비용'),
('ACC003', '출금', '2024-08-08', '09:45:00', 70000, '공과금 납부'),
('ACC003', '입금', '2024-08-09', '13:15:00', 400000, '월급 입금'),
('ACC003', '출금', '2024-08-10', '17:30:00', 200000, '집세 납부'),
('ACC004', '입금', '2024-08-07', '11:10:00', 200000, '보너스 지급'),
('ACC004', '출금', '2024-08-08', '14:15:00', 100000, 'ATM 출금'),
('ACC004', '입금', '2024-08-09', '12:20:00', 150000, '선물 돈'),
('ACC004', '출금', '2024-08-10', '19:45:00', 50000, '선물 구매'),
('ACC005', '입금', '2024-08-07', '09:50:00', 300000, '프리랜스 작업비'),
('ACC005', '출금', '2024-08-08', '15:25:00', 50000, '연료 구매'),
('ACC005', '입금', '2024-08-09', '18:10:00', 100000, '온라인 판매 수익'),
('ACC005', '출금', '2024-08-10', '16:40:00', 75000, '레스토랑 결제');

INSERT INTO CardUsageHistory (AccountNumber, UsageDate, UsageTime, Amount, MerchantName)
VALUES
('ACC001', '2024-08-01', '13:45:00', 75000, '레스토랑 A'),
('ACC002', '2024-08-02', '16:30:00', 120000, '전자제품 매장'),
('ACC001', '2024-08-03', '10:00:00', 55000, '서점'),
('ACC002', '2024-08-04', '18:25:00', 30000, '카페 B'),
('ACC003', '2024-08-05', '12:15:00', 150000, '의류 매장'),
('ACC003', '2024-08-06', '19:00:00', 45000, '편의점'),
('ACC001', '2024-08-07', '14:20:00', 70000, '영화관'),
('ACC003', '2024-08-08', '09:40:00', 95000, '레스토랑 B'),
('ACC004', '2024-08-09', '17:30:00', 200000, '가구 매장'),
('ACC004', '2024-08-10', '11:10:00', 30000, '카페 C'),
('ACC004', '2024-08-11', '15:50:00', 85000, '슈퍼마켓'),
('ACC004', '2024-08-12', '18:45:00', 120000, '서점'),
('ACC005', '2024-08-13', '10:30:00', 40000, '편의점'),
('ACC005', '2024-08-14', '16:00:00', 200000, '백화점'),
('ACC005', '2024-08-15', '19:20:00', 30000, '카페 D'),
('ACC005', '2024-08-16', '13:50:00', 60000, '영화관'),
('ACC001', '2024-08-17', '09:00:00', 90000, '식당'),
('ACC001', '2024-08-18', '12:30:00', 110000, '서점'),
('ACC001', '2024-08-19', '18:00:00', 80000, '헬스장'),
('ACC001', '2024-08-20', '14:25:00', 75000, '카페 E'),
('ACC002', '2024-08-21', '11:15:00', 50000, '편의점'),
('ACC002', '2024-08-22', '15:40:00', 150000, '전자제품 매장'),
('ACC002', '2024-08-23', '19:30:00', 20000, '식당'),
('ACC002', '2024-08-24', '13:10:00', 30000, '카페 F'),
('ACC003', '2024-08-25', '10:50:00', 100000, '서점'),
('ACC003', '2024-08-26', '16:45:00', 75000, '레스토랑 C'),
('ACC003', '2024-08-27', '12:20:00', 60000, '헬스장'),
('ACC004', '2024-08-28', '18:15:00', 95000, '식료품점'),
('ACC004', '2024-08-29', '14:35:00', 85000, '슈퍼마켓'),
('ACC005', '2024-08-30', '20:00:00', 100000, '가전제품 매장');

 -- 3 ~ 5
SELECT Name, RegistrationDate, AccountNumber
FROM CustomerAccount
ORDER BY RegistrationDate ASC;

SELECT Name, RegistrationDate, AccountNumber
FROM CustomerAccount
WHERE MONTH(RegistrationDate) BETWEEN 1 AND 3;

SELECT AccountNumber, SUM(Amount) AS TotalCardUsage
FROM CardUsageHistory
GROUP BY AccountNumber;

 -- 6 ~ 8 
SELECT SUM(cu.Amount) AS Total
FROM CardUsageHistory cu
JOIN CustomerAccount ca ON cu.AccountNumber = ca.AccountNumber
WHERE ca.Name = '김유나';

SELECT SUM(cu.Amount) AS Total
FROM CardUsageHistory cu
JOIN CustomerAccount ca ON cu.AccountNumber = ca.AccountNumber
WHERE ca.Name = '김유나'
  AND cu.UsageDate BETWEEN '2024-08-01' AND '2024-08-17';
  
SELECT AccountNumber, UsageDate, UsageTime, Amount, MerchantName
FROM CardUsageHistory
WHERE Amount >= 150000;

 -- 9 ~ 10
 SELECT AccountNumber, UsageDate, UsageTime, Amount, MerchantName
FROM CardUsageHistory
WHERE MONTH(UsageDate) = 8
ORDER BY Amount DESC;

INSERT INTO TransactionHistory (AccountNumber, TransactionType, TransactionDate, TransactionTime, Amount, Description)
SELECT AccountNumber, '출금', '2024-08-31', '18:00:00', TotalCardUsage, '8월 카드값 출금'
FROM (
    SELECT AccountNumber, SUM(Amount) AS TotalCardUsage
    FROM CardUsageHistory
    WHERE MONTH(UsageDate) = 8
    GROUP BY AccountNumber
) AS August;

SELECT * FROM TransactionHistory;

 -- 11
 
SELECT AccountNumber, UsageDate, UsageTime, Amount, MerchantName
FROM CardUsageHistory
WHERE MONTH(UsageDate) = 8
ORDER BY Amount DESC;

INSERT INTO TransactionHistory (AccountNumber, TransactionType, TransactionDate, TransactionTime, Amount, Description)
SELECT AccountNumber, '출금', '2024-08-31', '18:00:00', TotalCardUsage, '8월 카드값 출금'
FROM (
    SELECT AccountNumber, SUM(Amount) AS TotalCardUsage
    FROM CardUsageHistory
    WHERE MONTH(UsageDate) = 8
    GROUP BY AccountNumber
) AS August;

SELECT * FROM TransactionHistory;