/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        const store = this.store || (this.env && this.env.services && this.env.services.store) || this.pos;
        if (store && store.config && store.config.is_auto_invoice) {
            const order = this.currentOrder || (typeof store.get_order === 'function' ? store.get_order() : null);
            if (order && typeof order.set_to_invoice === 'function') {
                order.set_to_invoice(true);
            } else if (order) {
                order.to_invoice = true; // Fallback
            }
        }
    },
});
