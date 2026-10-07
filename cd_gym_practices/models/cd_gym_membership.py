from odoo import api, fields, models


class CdGymMembership(models.Model):
    """Modelo de laboratorio para los ejercicios de ORM.

    Lee el README.md del módulo: ahí tienes el índice completo de ejercicios,
    el bloque al que pertenece cada uno y el test que lo valida.
    """

    _name = 'cd.gym.membership'
    _description = 'Cuota de gimnasio'

    # =========================================================================
    # CAMPOS DE ANDAMIAJE
    # Estos campos ya vienen creados para que puedas practicar la ORM sin
    # tener que montar el modelo entero. No los toques salvo que el enunciado
    # de un ejercicio te lo pida.
    # =========================================================================
    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    partner_id = fields.Many2one('res.partner', string='Socio', ondelete='cascade')
    activity_ids = fields.Many2many(
        'cd.gym.activity',
        'cd_gym_membership_activity_rel',
        'membership_id',
        'activity_id',
        string='Actividades',
    )
    service_ids = fields.One2many('cd.gym.membership.line', 'membership_id', string='Servicios')
    booking_ids = fields.One2many('cd.gym.booking', 'membership_id', string='Reservas')
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
    )
    price = fields.Monetary(string='Precio de la cuota', currency_field='currency_id')
    quantity = fields.Integer(string='Nº de sesiones', default=1)
    start_date = fields.Date(string='Fecha de inicio')
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('active', 'Activa'),
            ('frozen', 'Congelada'),
            ('cancelled', 'Cancelada'),
        ],
        string='Estado',
        default='draft',
        required=True,
    )

    # #########################################################################
    # BLOQUE 2 · CAMPOS Y DECORADORES (ejercicios declarativos 9 a 18)
    # Aquí no hay métodos que rellenar: crea tú los campos y/o métodos que
    # pide cada ejercicio en ESTE modelo (salvo el 11, que va en el servicio).
    # #########################################################################

    # =========================================================================
    # EJERCICIO 9 · Bloque 2 · Test: TestFields.test_ex09_price_with_tax
    # -------------------------------------------------------------------------
    # Crea un campo price_with_tax (Float) computado y ALMACENADO (store=True)
    # que calcule el precio con un 21% de IVA: price * 1.21.
    # PISTA DE SINTAXIS
    #   price_with_tax = fields.Float(string='...', compute='_compute_price_with_tax', store=True)
    #
    #   @api.depends('price')
    #   def _compute_price_with_tax(self):
    #       ...  # recorre self y asigna membership.price * 1.21
    # =========================================================================

    # =========================================================================
    # EJERCICIO 10 · Bloque 2 · Test: TestFields.test_ex10_price_with_markup
    # -------------------------------------------------------------------------
    # Crea un campo price_with_markup (Float) computado NO almacenado que aplique
    # el margen que llegue en el contexto: gym_markup (en %).
    #   membership.with_context(gym_markup=50).price_with_markup -> price * 1.5
    #   sin gym_markup en el contexto -> price
    # PISTAS
    #   - Usa @api.depends_context('gym_markup') para que Odoo sepa que el
    #     valor depende del contexto y refresque la caché.
    #   - El valor se lee con self.env.context.get('gym_markup', 0.0).
    # =========================================================================

    # =========================================================================
    # EJERCICIO 12 · Bloque 2 · Test: TestFields.test_ex12_onchange_partner
    # -------------------------------------------------------------------------
    # Añade un @api.onchange('partner_id') que rellene description con
    # 'Cuota de {nombre del socio}' cuando haya partner_id.
    # El test rellena el formulario con odoo.tests.Form y comprueba el valor.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 13 · Bloque 2 · Test: TestFields.test_ex13_constrains_price
    # -------------------------------------------------------------------------
    # Añade un @api.constrains('price') que lance ValidationError si el precio
    # es negativo. Importa ValidationError desde odoo.exceptions.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 14 · Bloque 2 · Test: TestFields.test_ex14_constraint_quantity
    # -------------------------------------------------------------------------
    # Añade una constraint SQL con la API nueva de Odoo 19 (models.Constraint):
    # el número de sesiones no puede ser negativo.
    # PISTA DE SINTAXIS
    #   _check_quantity_non_negative = models.Constraint(
    #       'CHECK(quantity >= 0)',
    #       'El número de sesiones no puede ser negativo.',
    #   )
    # (el nombre del atributo DEBE empezar por guion bajo; el test provoca un
    #  IntegrityError creando un registro con quantity negativa)
    # =========================================================================

    # =========================================================================
    # EJERCICIO 15 · Bloque 2 · Test: TestFields.test_ex15_reference_default
    # -------------------------------------------------------------------------
    # Crea un campo reference (Char, copy=False) cuyo default sea
    # 'GYM/{año actual}' usando un lambda con acceso a fields.
    # PISTA: default=lambda self: 'GYM/%s' % fields.Date.today().year
    # =========================================================================

    # =========================================================================
    # EJERCICIO 16 · Bloque 2 · Test: TestFields.test_ex16_display_name
    # -------------------------------------------------------------------------
    # Sobrescribe _compute_display_name para que display_name sea
    # '{name} [{quantity} sesiones]'.
    # OJO: en Odoo 19 name_get() ya NO existe, se usa display_name.
    # PISTA: decora el método con @api.depends('name', 'quantity').
    # =========================================================================

    # =========================================================================
    # EJERCICIO 17 · Bloque 2 · Test: TestFields.test_ex17_copy_override
    # -------------------------------------------------------------------------
    # Sobrescribe copy(self, default=None) para que la copia siempre tenga
    # state='draft' y quantity=1 (respetando el resto de valores pedidos).
    # PISTA: llama a super().copy(default) con tu diccionario actualizado.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 18 · Bloque 2 · Test: TestFields.test_ex18_active_and_order
    # -------------------------------------------------------------------------
    # 1) Añade el campo active (Boolean, default=True).
    # 2) Establece _order = 'price desc, name' para que search([]) devuelva
    #    las cuotas ordenadas por precio descendente y luego por nombre.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 22 · Bloque 3 · Test: TestRelations.test_ex22_activity_names_inverse
    # -------------------------------------------------------------------------
    # Crea un campo activity_names (Char) computado NO almacenado con inverse:
    #   - compute: une los nombres de activity_ids con ', ' (en su orden).
    #   - inverse: separa por comas, crea las actividades que no existan y
    #     escribe activity_ids usando Command.set.
    # PISTAS
    #   - @api.depends('activity_ids')
    #   - Para el inverse: self.write({'activity_ids': [Command.set(ids)]})
    #   - get-or-create de actividades: self.env['cd.gym.activity'].search(...)
    #     + .create(...), o el truco activity = self.env['cd.gym.activity'].create(...)
    #   - Command se importa en Odoo 19 así: from odoo.fields import Command
    # =========================================================================

    # =========================================================================
    # MÉTODOS DE LOS EJERCICIOS DE ORM (Bloque 1 y ejercicios de métodos)
    # =========================================================================

    # =========================================================================
    # EJERCICIO 1 · Bloque 1 · Test: TestOrmBasics.test_ex01_create_memberships
    # -------------------------------------------------------------------------
    # Crea 3 cuotas en UNA SOLA llamada a create() con una lista de vals:
    #   'Cuota A' (precio 10), 'Cuota B' (precio 20), 'Cuota C' (precio 30).
    # Devuelve el recordset que retorna create().
    # PISTAS
    #   - create() acepta una lista de diccionarios: create([{...}, {...}]).
    #   - El resto de campos usan sus valores por defecto.
    #   - @api.model hace que self sea el modelo, no un registro.
    # =========================================================================
    @api.model
    def exercise_01_create_memberships(self):
        self.ensure_one()
        raise NotImplementedError('EJERCICIO 1 pendiente: create([{...}, {...}])')

    # =========================================================================
    # EJERCICIO 2 · Bloque 1 · Test: TestOrmBasics.test_ex02_search_memberships
    # -------------------------------------------------------------------------
    # Devuelve un recordset con las cuotas de precio >= min_price,
    # ordenadas de más caras a más baratas y limitado a `limit` registros.
    # PISTA: search([('price', '>=', min_price)], order='price desc', limit=limit)
    # =========================================================================
    @api.model
    def exercise_02_search_memberships(self, min_price, limit):
        raise NotImplementedError('EJERCICIO 2 pendiente: search con dominio, order y limit')

    # =========================================================================
    # EJERCICIO 3 · Bloque 1 · Test: TestOrmBasics.test_ex03_count_by_partner
    # -------------------------------------------------------------------------
    # Devuelve (int) cuántas cuotas pertenecen al partner `partner`.
    # PISTA: search_count([('partner_id', '=', partner.id)])
    # =========================================================================
    @api.model
    def exercise_03_count_memberships_by_partner(self, partner):
        raise NotImplementedError('EJERCICIO 3 pendiente: search_count con dominio')

    # =========================================================================
    # EJERCICIO 4 · Bloque 1 · Test: TestOrmBasics.test_ex04_expensive_names
    # -------------------------------------------------------------------------
    # Devuelve una lista con los nombres de las cuotas cuyo precio sea
    # MAYOR ESTRICTO que min_price, ordenada alfabéticamente.
    # OBLIGATORIO: hazlo con search([]) y los métodos de recordset
    # filtered(), mapped() y sorted(), SIN usar dominio para el precio.
    # PISTA: search([]).filtered(lambda m: ...).mapped('name'), y luego sorted().
    # =========================================================================
    @api.model
    def exercise_04_expensive_membership_names(self, min_price):
        raise NotImplementedError('EJERCICIO 4 pendiente: filtered + mapped + sorted')

    # =========================================================================
    # EJERCICIO 5 · Bloque 1 · Test: TestOrmBasics.test_ex05_set_state
    # -------------------------------------------------------------------------
    # Busca todas las cuotas cuyos nombres estén en la lista `names` y
    # cámbiales el estado a `new_state` de UNA SOLA escritura.
    # Devuelve cuántos registros has modificado.
    # PISTA: memberships = self.search([('name', 'in', names)]); el write()
    # sobre el recordset entero es una única llamada que aplica a todos.
    # =========================================================================
    @api.model
    def exercise_05_set_state(self, names, new_state):
        raise NotImplementedError('EJERCICIO 5 pendiente: write() sobre el recordset')

    # =========================================================================
    # EJERCICIO 6 · Bloque 1 · Test: TestOrmBasics.test_ex06_delete_cancelled
    # -------------------------------------------------------------------------
    # Borra todas las cuotas en estado 'cancelled' y devuelve cuántas
    # has borrado.
    # PISTA: search([('state', '=', 'cancelled')]).unlink()
    # =========================================================================
    @api.model
    def exercise_06_delete_cancelled(self):
        raise NotImplementedError('EJERCICIO 6 pendiente: unlink() sobre el recordset')

    # =========================================================================
    # EJERCICIO 7 · Bloque 1 · Test: TestOrmBasics.test_ex07_complex_domain
    # -------------------------------------------------------------------------
    # Devuelve una lista de nombres de las cuotas que cumplan TODO esto:
    #   (name contiene `text`  O  description contiene `text`)  Y precio >= min_price
    # OBLIGATORIO: usa un único dominio con los operadores lógicos '|' y '&'
    # (o su forma implícita) y el operador 'ilike'.
    # PISTA: ['&', '|', ('name', 'ilike', text), ('description', 'ilike', text),
    #         ('price', '>=', min_price)]
    # =========================================================================
    @api.model
    def exercise_07_complex_domain(self, text, min_price):
        raise NotImplementedError('EJERCICIO 7 pendiente: dominio con | & ilike')

    # =========================================================================
    # EJERCICIO 8 · Bloque 1 · Test: TestOrmBasics.test_ex08_browse_vs_search
    # -------------------------------------------------------------------------
    # Recibe una lista de ids (puede contener ids que no existen) y devuelve
    # un diccionario con:
    #   'found': cuántos existen de verdad
    #   'missing': lista de ids que no existen
    # PISTA: browse(ids).exists() filtra los que no existen.
    # =========================================================================
    @api.model
    def exercise_08_browse_vs_search(self, ids):
        raise NotImplementedError('EJERCICIO 8 pendiente: browse() + exists()')

    # =========================================================================
    # EJERCICIO 19 · Bloque 3 · Test: TestRelations.test_ex19_add_services
    # -------------------------------------------------------------------------
    # Sobre esta cuota (self), crea un servicio por cada nombre en
    # `service_names`, usando UNA SOLA escritura con Command.create.
    # Devuelve el recordset de servicios creados.
    # PISTAS
    #   - from odoo.fields import Command  (en Odoo 19 ya no se importa de odoo)
    #   - self.write({'service_ids': [Command.create({'name': n})
    #                                 for n in service_names]})
    #   - Las tuplas mágicas (0, 0, {...}) siguen existiendo por RPC, pero en
    #     Python se usan los objetos Command.
    # =========================================================================
    def exercise_19_add_services(self, service_names):
        raise NotImplementedError('EJERCICIO 19 pendiente: Command.create')

    # =========================================================================
    # EJERCICIO 20 · Bloque 3 · Test: TestRelations.test_ex20_set_and_clear_activities
    # -------------------------------------------------------------------------
    # a) exercise_20_set_activities(activity_names): deja en activity_ids
    #    EXACTAMENTE las actividades indicadas (las crea si no existen).
    #    Devuelve activity_ids.
    # b) exercise_20_clear_activities(): quita todas las actividades.
    #    Devuelve True.
    # OBLIGATORIO: usa Command.set y Command.clear.
    # PISTA: self.write({'activity_ids': [Command.set(ids)]})
    #        self.write({'activity_ids': [Command.clear()]})
    # =========================================================================
    def exercise_20_set_activities(self, activity_names):
        raise NotImplementedError('EJERCICIO 20 pendiente: Command.set')

    def exercise_20_clear_activities(self):
        raise NotImplementedError('EJERCICIO 20 pendiente: Command.clear')

    # =========================================================================
    # EJERCICIO 23 · Bloque 3 · Test: TestRelations.test_ex23_read_group
    # -------------------------------------------------------------------------
    # Devuelve el resultado de agrupar TODAS las cuotas por `state` y
    # contar cuántas hay en cada estado, usando _read_group (Odoo 19 ya no
    # usa read_group).
    # PISTA: self._read_group([], ['state'], ['__count'])
    #        -> [(estado, count), ...]
    # =========================================================================
    @api.model
    def exercise_23_read_group_by_state(self):
        raise NotImplementedError('EJERCICIO 23 pendiente: _read_group con __count')

    # =========================================================================
    # EJERCICIO 24 · Bloque 3 · Test: TestRelations.test_ex24_search_fetch
    # -------------------------------------------------------------------------
    # Devuelve las cuotas en estado 'active' ordenadas por precio
    # descendente, trayendo SOLO los campos name y price a la caché.
    # PISTA: search_fetch(dominio, ['name', 'price'], order='price desc')
    #        search_fetch combina search + fetch en una sola consulta (Odoo 16.2+).
    # =========================================================================
    @api.model
    def exercise_24_search_fetch_active(self):
        raise NotImplementedError('EJERCICIO 24 pendiente: search_fetch')

    # =========================================================================
    # EJERCICIO 28 · Bloque 4 · Test: TestViews.test_ex28_button_and_method
    # -------------------------------------------------------------------------
    # a) Implementa action_mark_active(): pasa a 'active' todas las cuotas
    #    de self que estén en 'draft'. Devuelve True.
    #    PISTA: self.filtered(lambda m: m.state == 'draft').write({...})
    # b) Abre views/cd_gym_membership_views.xml y añade el botón en el header
    #    (hay instrucciones dentro del XML).
    # =========================================================================
    def action_mark_active(self):
        raise NotImplementedError('EJERCICIO 28 pendiente: filtered() + write() y el botón en la vista')

    # =========================================================================
    # EJERCICIO 32 · Bloque 5 · Test: TestSecurity.test_ex32_has_access
    # -------------------------------------------------------------------------
    # Devuelve True si el usuario actual puede escribir sobre estos registros
    # y False si no. Usa la API nueva de Odoo 18/19 has_access().
    # PISTA: return self.has_access('write')
    # =========================================================================
    def exercise_32_has_write_access(self):
        raise NotImplementedError('EJERCICIO 32 pendiente: has_access')

    # -------------------------------------------------------------------------
    # Método de ayuda YA implementado: abre el asistente de reserva.
    # Te sirve de ejemplo de cómo devolver un act_window con contexto.
    # -------------------------------------------------------------------------
    def action_open_booking_wizard(self):
        self.ensure_one()
        return {
            'name': 'Nueva reserva',
            'type': 'ir.actions.act_window',
            'res_model': 'cd.gym.booking.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_membership_id': self.id},
        }
