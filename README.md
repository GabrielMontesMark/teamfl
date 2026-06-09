# Reporte de Funcionalidad: Módulos Migrados a Odoo 19

Este documento describe de forma práctica y sencilla la funcionalidad de cada uno de los módulos que han sido migrados exitosamente a la versión de Odoo 19. Está pensado para que cualquier usuario final pueda entender qué beneficio o característica aporta cada módulo al sistema, así como las definiciones necesarias por parte del cliente para su configuración.

---

## 🛒 Punto de Venta (POS)

### 1. Cliente por Defecto Automático (`pw_pos_default_customer`)
**¿Qué hace?** 
Ahorra tiempo a los cajeros asignando automáticamente un cliente cada vez que inician un nuevo pedido en la caja. 
**Beneficio:** Evita que el cajero tenga que buscar o crear un cliente genérico para las ventas rápidas.
**Configuración a consultar al cliente:** ¿Qué cliente específico (nombre, RUT/DNI) se debe definir en el sistema como el usuario por defecto para generar estas ventas rápidas en caja?

### 2. Facturación Automática (`pw_pos_auto_invoicing`)
**¿Qué hace?** 
Fuerza a que todas las ventas realizadas en el Punto de Venta generen una factura legal de forma automática.
**Beneficio:** Agiliza el cobro, ya que el cajero no tiene que recordar presionar el botón de "Factura" en cada venta; el sistema lo hace por él.
**Configuración a consultar al cliente:** ¿Desean que esta regla aplique a todos los Puntos de Venta (cajas) por igual, o hay alguna caja específica que deba seguir emitiendo solo recibos sin factura automática?

### 3. Impresión Rápida sin Descargas (`pos_invoice_print_without_download`)
**¿Qué hace?** 
Envía la orden de impresión del recibo directamente sin forzar al navegador a descargar un archivo PDF en la computadora del cajero.
**Beneficio:** Mantiene limpia la computadora de la caja (no se llena de archivos descargados) y reduce los clics necesarios para cobrar.
**Configuración a consultar al cliente:** ¿El bloqueo de la descarga del PDF se aplicará para todas las sucursales, o existe algún rol (como un supervisor) que sí deba conservar la capacidad de descargar los archivos de las facturas?

---

## 🧾 Facturación y Contabilidad

### 4. Recibo Térmico para Facturas (`thermal_invoice_report`)
**¿Qué hace?** 
Agrega un nuevo formato de impresión para las facturas que adapta el diseño al tamaño de las impresoras térmicas (las impresoras pequeñas de recibos/tickets).
**Beneficio:** Permite entregar facturas formales en formato ticket, ahorrando papel y luciendo más profesionales en mostradores físicos.
**Configuración a consultar al cliente:** ¿Cuáles son las medidas exactas de sus impresoras térmicas (ej. 58mm o 80mm) y qué información comercial específica (logo, redes sociales, políticas de devolución) desean que salga impresa en la parte inferior del ticket?

### 5. Control de Secuencias Contables (`od_journal_sequence`)
**¿Qué hace?** 
Devuelve a Odoo la capacidad de llevar una numeración estricta y personalizada por cada "Diario Contable" (por ejemplo, numeraciones distintas para Ventas Nacionales vs. Ventas Internacionales).
**Beneficio:** Facilita el cumplimiento de normas fiscales locales al permitir que la numeración de facturas y pagos siga reglas exactas definidas por el usuario.
**Configuración a consultar al cliente:** ¿Cuál es la estructura y formato exacto (prefijos, cantidad de ceros a la izquierda, si se reinicia cada año) que debe tener la numeración para cada uno de sus diarios contables?

### 6. Pagos por Adelantado (`account_payment_advance`)
**¿Qué hace?** 
Crea un flujo de trabajo sencillo para registrar dinero que los clientes entregan antes de que exista una factura (Anticipos).
**Beneficio:** El equipo de ventas o cobranza puede registrar un saldo a favor del cliente y luego aplicarlo fácilmente cuando se genere la factura final.
**Configuración a consultar al cliente:** ¿En qué cuenta contable específica y bajo qué Diario se deben registrar los fondos correspondientes a los anticipos recibidos de los clientes?

### 7. Impresión Rápida de Facturas (`account_move_print`)
**¿Qué hace?** 
Añade botones o atajos adicionales para mandar a imprimir las facturas directamente desde la pantalla de contabilidad con menos esfuerzo.
**Beneficio:** Mejora la experiencia del usuario reduciendo los clics diarios necesarios para procesos repetitivos.
**Configuración a consultar al cliente:** ¿En qué estados de la factura (Borrrador, Publicada, Pagada) desean que esté disponible este botón rápido de impresión?

---

## 📄 Diseño y Reportes Avanzados

### 8. Plantillas Profesionales de Word/LibreOffice (`report_extend_bf`)
**¿Qué hace?** 
Permite que cualquier persona pueda diseñar sus propios reportes (como contratos, cotizaciones o facturas) utilizando Microsoft Word o LibreOffice y luego subirlos a Odoo.
**Beneficio:** Elimina la dependencia de programadores para cambiar el diseño visual de un documento. Si la empresa quiere cambiar su logo, mover texto o cambiar los colores de un contrato, el personal administrativo puede hacerlo editando un archivo de texto normal.
**Configuración a consultar al cliente:** ¿Qué documentos, contratos o formatos específicos de la empresa necesitan ser diagramados en LibreOffice para integrarlos como reportes automáticos dentro del sistema?
