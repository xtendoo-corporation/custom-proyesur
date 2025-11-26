-- =====================================================================
-- SCRIPT DE RECUPERACIÓN DE COSTES DE EMPLEADOS EN LÍNEAS ANALÍTICAS
-- =====================================================================
-- Fecha: 2025-11-26
-- Propósito: Rellenar employee_timesheet_cost con los datos del empleado
-- Nota: En Odoo 18, el campo es hr_employee.hourly_cost (no timesheet_cost)
-- =====================================================================

-- PASO 1: Verificar el estado actual
SELECT
    COUNT(*) as total_lineas,
    COUNT(CASE WHEN employee_id IS NOT NULL THEN 1 END) as lineas_con_empleado,
    COUNT(CASE WHEN employee_timesheet_cost > 0 THEN 1 END) as lineas_con_coste,
    COUNT(CASE WHEN employee_id IS NOT NULL AND (employee_timesheet_cost IS NULL OR employee_timesheet_cost = 0) THEN 1 END) as lineas_sin_coste
FROM account_analytic_line;

-- PASO 2: Ver empleados y sus costes
SELECT
    emp.id,
    emp.name,
    emp.hourly_cost,
    COUNT(aal.id) as num_lineas_timesheet
FROM hr_employee emp
LEFT JOIN account_analytic_line aal ON aal.employee_id = emp.id
GROUP BY emp.id, emp.name, emp.hourly_cost
HAVING COUNT(aal.id) > 0
ORDER BY emp.name;

-- PASO 3: ACTUALIZAR LOS COSTES
-- ⚠️ IMPORTANTE: Este UPDATE modificará los datos
-- Ejecuta primero los SELECT anteriores para verificar

UPDATE account_analytic_line aal
SET employee_timesheet_cost = emp.hourly_cost
FROM hr_employee emp
WHERE aal.employee_id = emp.id
  AND aal.employee_id IS NOT NULL
  AND (aal.employee_timesheet_cost IS NULL OR aal.employee_timesheet_cost = 0)
  AND emp.hourly_cost IS NOT NULL
  AND emp.hourly_cost > 0;

-- PASO 4: Verificar resultado
SELECT
    COUNT(*) as lineas_actualizadas,
    SUM(aal.unit_amount * aal.employee_timesheet_cost) as coste_total
FROM account_analytic_line aal
WHERE aal.employee_timesheet_cost > 0;

-- PASO 5: Ver ejemplos de líneas actualizadas
SELECT
    aal.id,
    aal.date,
    emp.name as empleado,
    aal.unit_amount as horas,
    aal.employee_timesheet_cost as coste_hora,
    (aal.unit_amount * aal.employee_timesheet_cost) as coste_total,
    proj.name as proyecto
FROM account_analytic_line aal
INNER JOIN hr_employee emp ON aal.employee_id = emp.id
LEFT JOIN project_project proj ON aal.project_id = proj.id
WHERE aal.employee_timesheet_cost > 0
ORDER BY aal.date DESC
LIMIT 20;

