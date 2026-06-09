/** @odoo-module */

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    setup(vals) {
        super.setup(vals);
        if (this.config && this.config.pos_customer_id && !this.partner_id) {
            const default_customer_id = this.config.pos_customer_id.id || this.config.pos_customer_id[0];
            if (default_customer_id && this.models && this.models["res.partner"]) {
                const partner = this.models["res.partner"].get(default_customer_id);
                if (partner) {
                    this.partner_id = partner;
                }
            }
        }
    },
});
