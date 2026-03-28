from odoo import api, fields, models


class PosPreparationDisplay(models.Model):
    _name = 'pos.preparation.display'
    _description = 'POS Preparation Display'
    _order = 'name'

    name = fields.Char(
        string='Display Name',
        required=True,
        help='Name of this preparation display (e.g., Kitchen Display #1, Bar Display)',
    )
    pos_config_ids = fields.Many2many(
        'pos.config',
        string='Point of Sale Shops',
        help='POS shops whose orders will appear on this display. '
             'Leave empty to show orders from all shops.',
    )
    pos_category_ids = fields.Many2many(
        'pos.category',
        string='Product Categories',
        help='Only show order lines from these POS categories. '
             'Leave empty to show all categories.',
    )
    stage_ids = fields.One2many(
        'pos.preparation.display.stage',
        'display_id',
        string='Preparation Stages',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)
    order_count = fields.Integer(
        string='Active Orders',
        compute='_compute_order_count',
    )

    @api.depends('stage_ids')
    def _compute_order_count(self):
        for display in self:
            display.order_count = self.env['pos.preparation.display.order'].search_count([
                ('display_id', '=', display.id),
            ])

    def action_open_preparation_screen(self):
        """Open the preparation kanban screen for this display."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.name,
            'res_model': 'pos.preparation.display.order',
            'view_mode': 'kanban,list',
            'domain': [('display_id', '=', self.id)],
            'context': {
                'default_display_id': self.id,
                'search_default_group_by_stage': True,
            },
        }
