-- 1. [SELECT] Список всех посылок по дате доставки
SELECT id, category, arrival_date, weight, status
FROM packages
ORDER BY arrival_date;

-- 2. [SELECT] Список доставщиков по дате выезда
SELECT id, name, vehicle, departure_date, expected_delivery_date
FROM couriers
ORDER BY departure_date;

-- 3. [WHERE] Тяжёлые посылки (> 1 кг)
SELECT id, category, weight
FROM packages
WHERE weight > 1.0
ORDER BY weight DESC;

-- 4. [WHERE] Свободные доставщики
SELECT id, name, phone, expected_delivery_date
FROM couriers
WHERE is_available = 1
ORDER BY expected_delivery_date;

-- 5. [JOIN] Посылки с именами отправителя, получателя и курьера
SELECT
    p.id,
    p.category,
    p.arrival_date,
    p.weight,
    s.name AS sender_name,
    r.name AS recipient_name,
    c.name AS courier_name
FROM packages p
LEFT JOIN users   s ON p.sender_id    = s.id
LEFT JOIN users   r ON p.recipient_id = r.id
LEFT JOIN couriers c ON p.courier_id  = c.id
ORDER BY p.id;

-- 6. [JOIN + WHERE] Посылки, назначенные конкретному курьеру
SELECT
    p.id,
    p.category,
    p.arrival_date,
    p.weight,
    u.name AS recipient_name
FROM packages p
JOIN couriers c ON p.courier_id = c.id
JOIN users    u ON p.recipient_id = u.id
WHERE c.id = ?
ORDER BY p.arrival_date;

-- 7. [COUNT] Общее количество посылок
SELECT COUNT(*) AS packages_count
FROM packages;

-- 8. [COUNT] Количество свободных доставщиков
SELECT COUNT(*) AS free_couriers
FROM couriers
WHERE is_available = 1;

-- 9. [GROUP BY] Количество посылок по категориям
SELECT category, COUNT(*) AS total
FROM packages
GROUP BY category
ORDER BY total DESC;

-- 10. [GROUP BY] Количество посылок у каждого курьера
SELECT
    c.name AS courier_name,
    COUNT(p.id) AS packages_count
FROM couriers c
LEFT JOIN packages p ON p.courier_id = c.id
GROUP BY c.id, c.name
ORDER BY packages_count DESC;

-- 11. [GROUP BY + HAVING] Курьеры, у которых больше 1 посылки
SELECT
    c.name AS courier_name,
    COUNT(p.id) AS packages_count
FROM couriers c
JOIN packages p ON p.courier_id = c.id
GROUP BY c.id, c.name
HAVING COUNT(p.id) > 1
ORDER BY packages_count DESC;

-- 12. [Подзапрос + WHERE] Доставщики, у которых есть посылки,
--     но чья загрузка меньше половины грузоподъёмности
SELECT
    c.id,
    c.name,
    c.capacity_kg,
    COALESCE(SUM(p.weight), 0) AS total_weight
FROM couriers c
LEFT JOIN packages p ON p.courier_id = c.id
GROUP BY c.id, c.name, c.capacity_kg
HAVING COALESCE(SUM(p.weight), 0) < c.capacity_kg / 2
ORDER BY c.name;