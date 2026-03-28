from odoo import fields, models


class PosPreparationDisplayStage(models.Model):
    _name = 'pos.preparation.display.stage'
    _description = 'POS Preparation Display Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    display_id = fields.Many2one(
        'pos.preparation.display',
        string='Preparation Display',
        required=True,
        ondelete='cascade',
    )
    fold = fields.Boolean(
        string='Folded in Kanban',
        default=False,
        help='Folded stages are hidden by default in the kanban view.',
    )
