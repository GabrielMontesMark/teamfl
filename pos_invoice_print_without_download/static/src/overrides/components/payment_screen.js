/** @odoo-module */

/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

let isServicePatched = false;

patch(PaymentScreen.prototype, {
    setup() {
        if (super.setup) {
            super.setup(...arguments);
        }
        
        if (!isServicePatched) {
            const posStore = this.pos || this.store || (this.env && this.env.services && (this.env.services.pos || this.env.services.store));
            const actionService = this.env && this.env.services && this.env.services.action;
            const reportService = this.report || (this.env && this.env.services && this.env.services.report);
            
            if (actionService) {
                const originalActionDoAction = actionService.doAction;
                actionService.doAction = async (action, args) => {
                    if (posStore && posStore.config.invoice_print && (action === "account.account_invoices" || action === "account.report_invoice" || (action && action.report_name && action.report_name.includes('invoice')))) {
                        console.log("POS Invoice Print Without Download: Permanently intercepted action download");
                        return true;
                    }
                    return originalActionDoAction.call(actionService, action, args);
                };
            }
            if (reportService) {
                const originalReportDoAction = reportService.doAction;
                reportService.doAction = async (action, args) => {
                    if (posStore && posStore.config.invoice_print && (action === "account.account_invoices" || action === "account.report_invoice" || (action && action.report_name && action.report_name.includes('invoice')))) {
                        console.log("POS Invoice Print Without Download: Permanently intercepted report download");
                        return true;
                    }
                    return originalReportDoAction.call(reportService, action, args);
                };
            }
            
            const ormService = this.env && this.env.services && this.env.services.orm;
            if (ormService) {
                const originalOrmCall = ormService.call;
                ormService.call = async function(model, method, args, kwargs) {
                    if (!window.pos_invoice_print_manual_trigger && posStore && posStore.config.invoice_print && model === "account.move" && method === "action_invoice_download_pdf") {
                        console.log("POS Invoice Print Without Download: Permanently intercepted invoice download RPC call");
                        // Return a safe 'do nothing' notification action instead of a boolean to prevent OWL crashes
                        return { 
                            type: 'ir.actions.client', 
                            tag: 'display_notification', 
                            params: { 
                                title: 'Success', 
                                message: 'Invoice generated successfully.', 
                                type: 'success', 
                                sticky: false 
                            } 
                        };
                    }
                    return originalOrmCall.apply(this, arguments);
                };
            }
            
            isServicePatched = true;
        }
    }
});
