# 🧪 GUÍA DE PRUEBAS - Account Analytic Line Employee Price
## Módulo migrado a Odoo 18
## Fecha: 2025-11-26

---

## ✅ CHECKLIST DE PRUEBAS

### 📋 **PRUEBAS BÁSICAS**

#### ✓ **1. Verificar instalación del módulo**
- [ ] El módulo aparece en Aplicaciones
- [ ] Estado: Instalado (no "A actualizar")
- [ ] No hay errores en el log de Odoo

**Cómo verificar:**
```bash
cd /home/guillermo2005200/odoo18_2
docker-compose logs odoo | grep -i "account_analytic_line_employee_price"
```

---

#### ✓ **2. Verificar campos en la interfaz**

**Pasos:**
1. Ve a: **Hojas de horas → Todos los partes de horas**
2. Click en el icono de columnas (⚙️) superior derecha
3. Verifica que existen y puedes activar:
   - [ ] "Coste de la hoja de tiempo del empleado" (employee_timesheet_cost)
   - [ ] "Coste total de la hoja de horas del empleado" (employee_timesheet_cost_total)

**Resultado esperado:**
- Ambos campos visibles en la lista
- Los valores NO deben ser 0.00 en líneas existentes

---

### 🆕 **PRUEBAS DE CREACIÓN**

#### ✓ **3. Crear línea CON empleado configurado**

**Pasos:**
1. Ve a: **Hojas de horas → Mis hojas de horas**
2. Click en **+ Crear**
3. Rellena:
   - **Proyecto:** Cualquiera
   - **Empleado:** Selecciona un empleado con hourly_cost configurado
   - **Descripción:** "Prueba con empleado"
   - **Horas:** 5
4. **ANTES de guardar**, verifica en el formulario:
   - [ ] El campo "Coste de la hoja de tiempo del empleado" se rellena automáticamente
   - [ ] El valor debe ser el hourly_cost del empleado
5. Guarda la línea
6. Verifica en la vista de lista:
   - [ ] "Coste de la hoja de tiempo del empleado" = hourly_cost del empleado
   - [ ] "Coste total" = Horas × hourly_cost

**Ejemplo esperado:**
- Empleado: JOSE MIGUEL CABALLERO (hourly_cost = 11.00 €/h)
- Horas: 5
- **Resultado:** Coste = 11.00 €, Total = 55.00 €

---

#### ✓ **4. Crear línea SIN empleado (caso PARTES BRICODEPOT)**

**Pasos:**
1. Ve a: **Hojas de horas → Mis hojas de horas**
2. Click en **+ Crear**
3. Rellena:
   - **Proyecto:** PARTES BRICODEPOT (o cualquier proyecto)
   - **Empleado:** (DEJAR VACÍO)
   - **Descripción:** "Prueba sin empleado"
   - **Horas:** 8
4. **ANTES de guardar**, verifica:
   - [ ] El campo "Coste de la hoja de tiempo del empleado" = **4.38 €**
5. Guarda la línea
6. Verifica en la vista de lista:
   - [ ] "Coste de la hoja de tiempo del empleado" = 4.38 €
   - [ ] "Coste total" = 8 × 4.38 = **35.04 €**

**⚠️ IMPORTANTE:** Este es el caso crítico que estaba fallando antes.

---

#### ✓ **5. Crear línea con empleado SIN hourly_cost**

**Pasos previos:** Asegúrate de tener un empleado sin hourly_cost configurado
1. Ve a: **Empleados** → Selecciona un empleado
2. Pestaña: **Configuración de RR.HH.**
3. Campo "Coste por Hora": Déjalo en 0 o vacío
4. Guarda

**Ahora crea la línea:**
1. Ve a: **Hojas de horas → Mis hojas de horas**
2. Crea nueva línea:
   - **Proyecto:** Cualquiera
   - **Empleado:** El empleado sin hourly_cost
   - **Horas:** 3
3. Verifica:
   - [ ] El coste debe ser **4.38 €** (fallback automático)
   - [ ] Total = 3 × 4.38 = **13.14 €**

---

### 🔄 **PRUEBAS DE MODIFICACIÓN**

#### ✓ **6. Cambiar empleado en línea existente**

**Pasos:**
1. Abre una línea de timesheet existente
2. Cambia el empleado por otro con diferente hourly_cost
3. Verifica:
   - [ ] El coste se actualiza automáticamente con el nuevo hourly_cost
   - [ ] El total se recalcula automáticamente

---

#### ✓ **7. Modificar horas en línea existente**

**Pasos:**
1. Abre una línea con coste 4.38 € y 8 horas (total 35.04 €)
2. Cambia las horas a **10**
3. Guarda
4. Verifica:
   - [ ] El coste por hora sigue siendo 4.38 €
   - [ ] El total se actualiza a **43.80 €** (10 × 4.38)

---

### 📊 **PRUEBAS DE VISUALIZACIÓN**

#### ✓ **8. Verificar totales en vista de lista**

**Pasos:**
1. Ve a: **Hojas de horas → Todos los partes de horas**
2. Activa la columna "Coste total de la hoja de horas del empleado"
3. Verifica:
   - [ ] La columna muestra un total sumado al final
   - [ ] El total coincide con la suma de todas las líneas

---

#### ✓ **9. Verificar permisos de usuario**

**Pasos:**
1. Inicia sesión con un usuario SIN el grupo "Recursos Humanos / Oficial"
2. Ve a: **Hojas de horas → Mis hojas de horas**
3. Verifica:
   - [ ] Los campos de coste NO deben ser visibles (por seguridad)

**Pasos para usuario CON permisos:**
1. Inicia sesión con un usuario CON el grupo "Recursos Humanos / Oficial"
2. Ve a: **Hojas de horas**
3. Verifica:
   - [ ] Los campos de coste SÍ son visibles

---

### 🔍 **PRUEBAS DE DATOS HISTÓRICOS**

#### ✓ **10. Verificar datos migrados desde Odoo 14**

**Pasos SQL:**
```sql
-- Conectar a la base de datos
docker-compose exec -T db psql -U odoo -d proye_26_1

-- Verificar líneas actualizadas
SELECT
    COUNT(*) as total_lineas_con_coste,
    COUNT(DISTINCT employee_id) as empleados_distintos,
    SUM(unit_amount) as total_horas,
    SUM(employee_timesheet_cost * unit_amount) as coste_total
FROM account_analytic_line
WHERE employee_timesheet_cost > 0;
```

**Resultado esperado:**
- [ ] Total líneas con coste > 7,500
- [ ] Coste total > 0
- [ ] No hay valores NULL en líneas con horas > 0

---

#### ✓ **11. Verificar líneas del 31/08/2023**

**Pasos SQL:**
```sql
docker-compose exec -T db psql -U odoo -d proye_26_1 -c "
SELECT
    COUNT(*) as lineas,
    AVG(employee_timesheet_cost) as coste_promedio,
    SUM(employee_timesheet_cost * unit_amount) as total
FROM account_analytic_line
WHERE date = '2023-08-31'
  AND employee_timesheet_cost > 0;
"
```

**Resultado esperado:**
- [ ] Hay líneas con fecha 31/08/2023
- [ ] Todas tienen employee_timesheet_cost > 0
- [ ] El coste promedio está entre 4.00 y 12.00 €/h

---

### 🎯 **PRUEBAS ESPECÍFICAS PARTES BRICODEPOT**

#### ✓ **12. Verificar líneas históricas de PARTES BRICODEPOT**

**Pasos SQL:**
```sql
docker-compose exec -T db psql -U odoo -d proye_26_1 -c "
SELECT
    date,
    unit_amount as horas,
    employee_timesheet_cost as coste_hora,
    (unit_amount * employee_timesheet_cost) as total
FROM account_analytic_line
WHERE date = '2023-08-31'
  AND employee_id IS NULL
  AND employee_timesheet_cost > 0
ORDER BY date DESC
LIMIT 5;
"
```

**Resultado esperado:**
- [ ] Líneas sin employee_id tienen coste = 4.38 €
- [ ] Los totales se calculan correctamente

---

### ⚡ **PRUEBAS DE RENDIMIENTO**

#### ✓ **13. Crear múltiples líneas rápidamente**

**Pasos:**
1. Crea 10 líneas de timesheet seguidas
2. Alterna entre:
   - Líneas con empleado
   - Líneas sin empleado (solo proyecto)
3. Verifica:
   - [ ] Todas las líneas se crean sin errores
   - [ ] Los costes se asignan correctamente en todas
   - [ ] No hay ralentización notable

---

### 🔧 **PRUEBAS TÉCNICAS**

#### ✓ **14. Verificar hooks de migración**

**Pasos:**
```bash
cd /home/guillermo2005200/odoo18_2
docker-compose logs odoo | grep -i "employee_timesheet_cost" | tail -20
```

**Resultado esperado:**
- [ ] No hay errores relacionados con employee_timesheet_cost
- [ ] Los logs muestran la migración exitosa

---

#### ✓ **15. Verificar integridad de la base de datos**

**Pasos SQL:**
```sql
docker-compose exec -T db psql -U odoo -d proye_26_1 -c "
-- Líneas con horas pero sin coste (NO debería haber)
SELECT COUNT(*) as lineas_problematicas
FROM account_analytic_line
WHERE unit_amount > 0
  AND (employee_timesheet_cost IS NULL OR employee_timesheet_cost = 0);
"
```

**Resultado esperado:**
- [ ] lineas_problematicas = 0 (o muy pocas)

---

### 📱 **PRUEBAS DE COMPATIBILIDAD**

#### ✓ **16. Verificar en diferentes vistas**

**Verificar en:**
- [ ] Vista de lista de hojas de horas
- [ ] Vista de formulario de línea individual
- [ ] Vista de árbol en "Mis hojas de horas"
- [ ] Vista de análisis/pivot de hojas de horas
- [ ] Reportes de hojas de horas (si existen)

---

#### ✓ **17. Verificar exportación**

**Pasos:**
1. Ve a: **Hojas de horas → Todos los partes de horas**
2. Selecciona varias líneas
3. Click en **Acción → Exportar**
4. Selecciona los campos:
   - Fecha
   - Empleado
   - Horas
   - Coste de la hoja de tiempo del empleado
   - Coste total
5. Exporta
6. Verifica:
   - [ ] El archivo se descarga correctamente
   - [ ] Los valores de coste están presentes
   - [ ] No hay errores en la exportación

---

### 🐛 **PRUEBAS DE CASOS EXTREMOS**

#### ✓ **18. Línea sin proyecto ni empleado**

**Pasos:**
1. Intenta crear una línea analítica:
   - **Proyecto:** (vacío)
   - **Empleado:** (vacío)
   - **Horas:** 2
2. Verifica:
   - [ ] El sistema permite crearla O muestra error apropiado
   - [ ] Si se crea, el coste debe ser 0 o 4.38 (según lógica)

---

#### ✓ **19. Cambiar coste manualmente**

**Pasos:**
1. Crea una línea con coste automático 4.38 €
2. En el formulario, cambia manualmente el coste a **10.00 €**
3. Guarda
4. Verifica:
   - [ ] El coste se queda en 10.00 € (respeta el cambio manual)
   - [ ] El total se recalcula con el nuevo coste

---

#### ✓ **20. Línea con 0 horas**

**Pasos:**
1. Crea una línea con:
   - Empleado: Cualquiera
   - **Horas:** 0
2. Verifica:
   - [ ] El coste por hora se asigna normalmente
   - [ ] El total es 0 (0 × coste = 0)

---

## 📝 **REGISTRO DE PRUEBAS**

### Plantilla de registro:

```
Fecha de prueba: _______________
Probado por: _______________
Base de datos: proye_26_1

✓ = Pasó
✗ = Falló
⚠ = Necesita revisión

[ ] Prueba 1: Verificar instalación
[ ] Prueba 2: Verificar campos
[ ] Prueba 3: Crear con empleado
[ ] Prueba 4: Crear sin empleado (CRÍTICO)
[ ] Prueba 5: Empleado sin hourly_cost
[ ] Prueba 6: Cambiar empleado
[ ] Prueba 7: Modificar horas
[ ] Prueba 8: Verificar totales
[ ] Prueba 9: Verificar permisos
[ ] Prueba 10: Datos históricos
[ ] Prueba 11: Líneas 31/08/2023
[ ] Prueba 12: PARTES BRICODEPOT histórico
[ ] Prueba 13: Rendimiento
[ ] Prueba 14: Logs de migración
[ ] Prueba 15: Integridad BD
[ ] Prueba 16: Diferentes vistas
[ ] Prueba 17: Exportación
[ ] Prueba 18: Sin proyecto ni empleado
[ ] Prueba 19: Cambio manual
[ ] Prueba 20: 0 horas

Observaciones:
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## 🚨 **PROBLEMAS CONOCIDOS Y SOLUCIONES**

### ⚠️ Si los campos no aparecen:
```bash
# Limpiar caché del navegador
Ctrl + F5

# O actualizar el módulo
docker-compose run --rm odoo odoo -u account_analytic_line_employee_price -d proye_26_1 --stop-after-init
docker-compose restart odoo
```

### ⚠️ Si los costes están en 0:
```sql
# Ejecutar actualización manual
docker-compose exec -T db psql -U odoo -d proye_26_1 -c "
UPDATE account_analytic_line aal
SET employee_timesheet_cost = emp.hourly_cost
FROM hr_employee emp
WHERE aal.employee_id = emp.id
  AND (aal.employee_timesheet_cost IS NULL OR aal.employee_timesheet_cost = 0)
  AND emp.hourly_cost > 0;
"
```

### ⚠️ Si las nuevas líneas no toman coste automático:
```bash
# Verificar que el módulo está actualizado
docker-compose restart odoo
# Luego actualiza el módulo desde la interfaz
```

---

## ✅ **CRITERIOS DE ACEPTACIÓN**

El módulo se considera **100% funcional** si:

1. ✅ Todas las líneas existentes tienen coste > 0 (excepto las que deben ser 0)
2. ✅ Las nuevas líneas CON empleado toman el hourly_cost del empleado
3. ✅ Las nuevas líneas SIN empleado toman 4.38 € automáticamente
4. ✅ Los totales se calculan correctamente
5. ✅ Los campos son visibles solo para usuarios con permisos
6. ✅ No hay errores en los logs de Odoo
7. ✅ El rendimiento es aceptable (< 2 segundos para crear línea)
8. ✅ Los datos históricos están correctamente migrados

---

## 📞 **SOPORTE**

Si encuentras algún problema:

1. **Revisa los logs:**
   ```bash
   docker-compose logs odoo | grep -i error | tail -50
   ```

2. **Verifica la base de datos:**
   ```bash
   docker-compose exec -T db psql -U odoo -d proye_26_1
   ```

3. **Reinicia Odoo:**
   ```bash
   docker-compose restart odoo
   ```

---

**Última actualización:** 2025-11-26
**Versión del módulo:** 18.0.1.0.2
**Estado:** ✅ Migración completada

