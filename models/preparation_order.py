from odoo import api, fields, models


class PosPreparationDisplayOrder(models.Model):
    _name = 'pos.preparation.display.order'
    _description = 'POS Preparation Display Order'
    _order = 'create_date desc'
    _rec_name = 'display_name'

    display_id = fields.Many2one(
        'pos.preparation.display',
        string='Preparation Display',
        required=True,
        ondelete='cascade',
    )
    pos_order_id = fields.Many2one(
        'pos.order',
        string='POS Order',
        ondelete='cascade',
    )
    pos_order_line_ids = fields.Many2many(
        'pos.order.line',
        string='Order Lines',
    )
    stage_id = fields.Many2one(
        'pos.preparation.display.stage',
        string='Stage',
        group_expand='_read_group_stage_ids',
        tracking=True,
    )
    note = fields.Text(string='Notes')
    order_reference = fields.Char(
        string='Order Ref',
        related='pos_order_id.pos_reference',
        store=True,
    )
    order_date = fields.Datetime(
        string='Order Date',
        related='pos_order_id.date_order',
        store=True,
    )
    product_names = fields.Text(
        string='Items',
        compute='_compute_product_names',
        store=True,
    )
    color = fields.Integer(string='Color', default=0)
    company_id = fields.Many2one(
        'res.company',
        related='display_id.company_id',
        store=True,
    )

    @api.depends('pos_order_line_ids', 'pos_order_line_ids.product_id')
    def _compute_product_names(self):
        for order in self:
            lines = order.pos_order_line_ids
            if lines:
                items = []
                for line in lines:
                    qty = int(line.qty) if line.qty == int(line.qty) else line.qty
                    items.append(f'{qty}x {line.product_id.name}')
                order.product_names = '\n'.join(items)
            else:
                order.product_names = ''

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """Show all stages in kanban, even empty ones."""
        # Get display_id from context or domain
        display_id = self.env.context.get('default_display_id')
        if display_id:
            return self.env['pos.preparation.display.stage'].search([
                ('display_id', '=', display_id),
            ], order=order)
        return stages

    def action_next_stage(self):
        """Move order to the next stage."""
        for order in self:
            if not order.stage_id or not order.display_id:
                continue
            stages = order.display_id.stage_ids.sorted('sequence')
            current_idx = list(stages).index(order.stage_id) if order.stage_id in stages else -1
            if current_idx < len(stages) - 1:
                order.stage_id = stages[current_idx + 1]

    def action_done(self):
        """Move order to the last (done) stage."""
        for order in self:
            if order.display_id and order.display_id.stage_ids:
                order.stage_id = order.display_id.stage_ids.sorted('sequence')[-1]
