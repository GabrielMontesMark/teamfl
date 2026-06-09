/** @odoo-module */

/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { patch } from "@web/core/utils/patch";

patch(ReceiptScreen.prototype, {
    setup(){
        super.setup(...arguments);
    },
    
    canPrintInvoice() {
        const order = (this.props && this.props.order) || this.currentOrder || (this.pos && typeof this.pos.get_order === 'function' && this.pos.get_order()) || (this.store && typeof this.store.get_order === 'function' && this.store.get_order());
        if (!order) return false;
        
        // Handle both active order objects and finalized serialized JSON orders
        if (typeof order.is_to_invoice === 'function') return order.is_to_invoice();
        if (order.is_to_invoice === true || order.to_invoice === true) return true;
        if (order.account_move || order.invoice_id || order.account_move_id) return true;
        
        return false;
    },

    async printInvoicePdf(){ 
        const order = (this.props && this.props.order) || this.currentOrder || (this.pos && typeof this.pos.get_order === 'function' && this.pos.get_order()) || (this.store && typeof this.store.get_order === 'function' && this.store.get_order());
        
        // Find the invoice ID from the order
        let invoiceId = order.invoice_id || order.account_move || order.account_move_id;
        if (!invoiceId && order.get_account_move) invoiceId = order.get_account_move();
        
        // En Odoo 19, account_move puede ser un objeto en lugar de un número. Extraemos el ID numérico.
        if (invoiceId && typeof invoiceId === 'object') {
            invoiceId = invoiceId.id || invoiceId[0] || invoiceId;
        }
        
        if (!invoiceId) {
            console.error("POS Invoice Print Without Download: Could not find invoice ID on the order", order);
            alert("The invoice ID could not be found for this order. It might still be synchronizing.");
            return;
        }

        try {
            const orm = this.orm || (this.env && this.env.services && this.env.services.orm);
            
            // Llamamos a nuestro backend para generar el Base64 (sin que Odoo lo detecte como archivo a descargar)
            const result = await orm.call(
                "pos.order",
                "action_invoice_pdf",
                [parseInt(invoiceId)],
            );
            
            // Usamos la misma librería de impresión rápida, o un iFrame nativo si la librería no está en Odoo 19
            if (typeof printJS !== 'undefined') {
                printJS({printable: result, type: 'pdf', base64: true});
            } else {
                const pdfData = "data:application/pdf;base64," + result;
                const iframe = document.createElement('iframe');
                iframe.style.display = 'none';
                iframe.src = pdfData;
                document.body.appendChild(iframe);
                iframe.onload = () => {
                    iframe.contentWindow.print();
                    // Limpieza después de imprimir
                    setTimeout(() => document.body.removeChild(iframe), 10000);
                };
            }
        } catch (error) {
            console.error(error);
            alert("Connection Error trying to print invoice.");
        }
    }
});

