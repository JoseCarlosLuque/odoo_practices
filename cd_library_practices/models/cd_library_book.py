from odoo import api, fields, models


class CdLibraryBook(models.Model):
    """Modelo de laboratorio para los ejercicios de ORM.

    Lee el README.md del módulo: ahí tienes el índice completo de ejercicios,
    el bloque al que pertenece cada uno y el test que lo valida.
    """

    _name = 'cd.library.book'
    _description = 'Libro de la biblioteca'

    # =========================================================================
    # CAMPOS DE ANDAMIAJE
    # Estos campos ya vienen creados para que puedas practicar la ORM sin
    # tener que montar el modelo entero. No los toques salvo que el enunciado
    # de un ejercicio te lo pida.
    # =========================================================================
    name = fields.Char(string='Título', required=True)
    description = fields.Text(string='Sinopsis')
    author_id = fields.Many2one('res.partner', string='Autor', ondelete='cascade')
    genre_ids = fields.Many2many(
        'cd.library.genre',
        'cd_library_book_genre_rel',
        'book_id',
        'genre_id',
        string='Géneros',
    )
    copy_ids = fields.One2many('cd.library.copy', 'book_id', string='Ejemplares')
    loan_ids = fields.One2many('cd.library.loan', 'book_id', string='Préstamos')
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
    )
    replacement_cost = fields.Monetary(string='Coste de reposición', currency_field='currency_id')
    quantity = fields.Integer(string='Nº de ejemplares', default=1)
    publication_date = fields.Date(string='Fecha de publicación')
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('available', 'Disponible'),
            ('loaned', 'Prestado'),
            ('withdrawn', 'Retirado'),
        ],
        string='Estado',
        default='draft',
        required=True,
    )

    # #########################################################################
    # BLOQUE 2 · CAMPOS Y DECORADORES (ejercicios declarativos 9 a 18)
    # Aquí no hay métodos que rellenar: crea tú los campos y/o métodos que
    # pide cada ejercicio en ESTE modelo (salvo el 11, que va en el ejemplar).
    # #########################################################################

    # =========================================================================
    # EJERCICIO 9 · Bloque 2 · Test: TestFields.test_ex09_cost_with_tax
    # -------------------------------------------------------------------------
    # Crea un campo replacement_cost_with_tax (Float) computado y ALMACENADO
    # (store=True) que calcule el coste con un 21% de IVA:
    # replacement_cost * 1.21.
    # PISTA DE SINTAXIS
    #   replacement_cost_with_tax = fields.Float(
    #       string='...', compute='_compute_replacement_cost_with_tax', store=True)
    #
    #   @api.depends('replacement_cost')
    #   def _compute_replacement_cost_with_tax(self):
    #       ...  # recorre self y asigna book.replacement_cost * 1.21
    # =========================================================================

    # =========================================================================
    # EJERCICIO 10 · Bloque 2 · Test: TestFields.test_ex10_cost_with_markup
    # -------------------------------------------------------------------------
    # Crea un campo cost_with_markup (Float) computado NO almacenado que aplique
    # el margen que llegue en el contexto: library_markup (en %).
    #   book.with_context(library_markup=50).cost_with_markup -> cost * 1.5
    #   sin library_markup en el contexto -> cost
    # PISTAS
    #   - Usa @api.depends_context('library_markup') para que Odoo sepa que el
    #     valor depende del contexto y refresque la caché.
    #   - El valor se lee con self.env.context.get('library_markup', 0.0).
    # =========================================================================

    # =========================================================================
    # EJERCICIO 12 · Bloque 2 · Test: TestFields.test_ex12_onchange_author
    # -------------------------------------------------------------------------
    # Añade un @api.onchange('author_id') que rellene description con
    # 'Obra de {nombre del autor}' cuando haya author_id.
    # El test rellena el formulario con odoo.tests.Form y comprueba el valor.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 13 · Bloque 2 · Test: TestFields.test_ex13_constrains_cost
    # -------------------------------------------------------------------------
    # Añade un @api.constrains('replacement_cost') que lance ValidationError si
    # el coste es negativo. Importa ValidationError desde odoo.exceptions.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 14 · Bloque 2 · Test: TestFields.test_ex14_constraint_quantity
    # -------------------------------------------------------------------------
    # Añade una constraint SQL con la API nueva de Odoo 19 (models.Constraint):
    # el número de ejemplares no puede ser negativo.
    # PISTA DE SINTAXIS
    #   _check_quantity_non_negative = models.Constraint(
    #       'CHECK(quantity >= 0)',
    #       'El número de ejemplares no puede ser negativo.',
    #   )
    # (el nombre del atributo DEBE empezar por guion bajo; el test provoca un
    #  IntegrityError creando un registro con quantity negativa)
    # =========================================================================

    # =========================================================================
    # EJERCICIO 15 · Bloque 2 · Test: TestFields.test_ex15_reference_default
    # -------------------------------------------------------------------------
    # Crea un campo reference (Char, copy=False) cuyo default sea
    # 'LIB/{año actual}' usando un lambda con acceso a fields.
    # PISTA: default=lambda self: 'LIB/%s' % fields.Date.today().year
    # =========================================================================

    # =========================================================================
    # EJERCICIO 16 · Bloque 2 · Test: TestFields.test_ex16_display_name
    # -------------------------------------------------------------------------
    # Sobrescribe _compute_display_name para que display_name sea
    # '{name} [{quantity} ejemplares]'.
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
    # 2) Establece _order = 'replacement_cost desc, name' para que search([])
    #    devuelva los libros ordenados por coste descendente y luego por título.
    # =========================================================================

    # =========================================================================
    # EJERCICIO 22 · Bloque 3 · Test: TestRelations.test_ex22_genre_names_inverse
    # -------------------------------------------------------------------------
    # Crea un campo genre_names (Char) computado NO almacenado con inverse:
    #   - compute: une los nombres de genre_ids con ', ' (en su orden).
    #   - inverse: separa por comas, crea los géneros que no existan y
    #     escribe genre_ids usando Command.set.
    # PISTAS
    #   - @api.depends('genre_ids')
    #   - Para el inverse: self.write({'genre_ids': [Command.set(ids)]})
    #   - get-or-create de géneros: self.env['cd.library.genre'].search(...)
    #     + .create(...), o el truco genre = self.env['cd.library.genre'].create(...)
    #   - Command se importa en Odoo 19 así: from odoo.fields import Command
    # =========================================================================

    # =========================================================================
    # MÉTODOS DE LOS EJERCICIOS DE ORM (Bloque 1 y ejercicios de métodos)
    # =========================================================================

    # =========================================================================
    # EJERCICIO 1 · Bloque 1 · Test: TestOrmBasics.test_ex01_create_books
    # -------------------------------------------------------------------------
    # Crea 3 libros en UNA SOLA llamada a create() con una lista de vals:
    #   'Libro A' (coste 10), 'Libro B' (coste 20), 'Libro C' (coste 30).
    # Devuelve el recordset que retorna create().
    # PISTAS
    #   - create() acepta una lista de diccionarios: create([{...}, {...}]).
    #   - El resto de campos usan sus valores por defecto.
    #   - @api.model hace que self sea el modelo, no un registro.
    # =========================================================================
    @api.model
    def exercise_01_create_books(self):
        self.ensure_one()
        raise NotImplementedError('EJERCICIO 1 pendiente: create([{...}, {...}])')

    # =========================================================================
    # EJERCICIO 2 · Bloque 1 · Test: TestOrmBasics.test_ex02_search_books
    # -------------------------------------------------------------------------
    # Devuelve un recordset con los libros de coste >= min_cost,
    # ordenados de más caro a más barato y limitado a `limit` registros.
    # PISTA: search([('replacement_cost', '>=', min_cost)],
    #               order='replacement_cost desc', limit=limit)
    # =========================================================================
    @api.model
    def exercise_02_search_books(self, min_cost, limit):
        raise NotImplementedError('EJERCICIO 2 pendiente: search con dominio, order y limit')

    # =========================================================================
    # EJERCICIO 3 · Bloque 1 · Test: TestOrmBasics.test_ex03_count_by_author
    # -------------------------------------------------------------------------
    # Devuelve (int) cuántos libros pertenecen al partner `author`.
    # PISTA: search_count([('author_id', '=', author.id)])
    # =========================================================================
    @api.model
    def exercise_03_count_books_by_author(self, author):
        raise NotImplementedError('EJERCICIO 3 pendiente: search_count con dominio')

    # =========================================================================
    # EJERCICIO 4 · Bloque 1 · Test: TestOrmBasics.test_ex04_expensive_titles
    # -------------------------------------------------------------------------
    # Devuelve una lista con los títulos de los libros cuyo coste sea
    # MAYOR ESTRICTO que min_cost, ordenada alfabéticamente.
    # OBLIGATORIO: hazlo con search([]) y los métodos de recordset
    # filtered(), mapped() y sorted(), SIN usar dominio para el coste.
    # PISTA: search([]).filtered(lambda b: ...).mapped('name'), y luego sorted().
    # =========================================================================
    @api.model
    def exercise_04_expensive_book_titles(self, min_cost):
        raise NotImplementedError('EJERCICIO 4 pendiente: filtered + mapped + sorted')

    # =========================================================================
    # EJERCICIO 5 · Bloque 1 · Test: TestOrmBasics.test_ex05_set_state
    # -------------------------------------------------------------------------
    # Busca todos los libros cuyos títulos estén en la lista `names` y
    # cámbiales el estado a `new_state` de UNA SOLA escritura.
    # Devuelve cuántos registros has modificado.
    # PISTA: books = self.search([('name', 'in', names)]); el write() sobre
    # el recordset entero es una única llamada que aplica a todos.
    # =========================================================================
    @api.model
    def exercise_05_set_state(self, names, new_state):
        raise NotImplementedError('EJERCICIO 5 pendiente: write() sobre el recordset')

    # =========================================================================
    # EJERCICIO 6 · Bloque 1 · Test: TestOrmBasics.test_ex06_delete_withdrawn
    # -------------------------------------------------------------------------
    # Borra todos los libros en estado 'withdrawn' y devuelve cuántos
    # has borrado.
    # PISTA: search([('state', '=', 'withdrawn')]).unlink()
    # =========================================================================
    @api.model
    def exercise_06_delete_withdrawn(self):
        raise NotImplementedError('EJERCICIO 6 pendiente: unlink() sobre el recordset')

    # =========================================================================
    # EJERCICIO 7 · Bloque 1 · Test: TestOrmBasics.test_ex07_complex_domain
    # -------------------------------------------------------------------------
    # Devuelve una lista de títulos de los libros que cumplan TODO esto:
    #   (name contiene `text`  O  description contiene `text`)  Y coste >= min_cost
    # OBLIGATORIO: usa un único dominio con los operadores lógicos '|' y '&'
    # (o su forma implícita) y el operador 'ilike'.
    # PISTA: ['&', '|', ('name', 'ilike', text), ('description', 'ilike', text),
    #         ('replacement_cost', '>=', min_cost)]
    # =========================================================================
    @api.model
    def exercise_07_complex_domain(self, text, min_cost):
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
    # EJERCICIO 19 · Bloque 3 · Test: TestRelations.test_ex19_add_copies
    # -------------------------------------------------------------------------
    # Sobre este libro (self), crea un ejemplar por cada código en
    # `copy_codes`, usando UNA SOLA escritura con Command.create.
    # Devuelve el recordset de ejemplares creados.
    # PISTAS
    #   - from odoo.fields import Command  (en Odoo 19 ya no se importa de odoo)
    #   - self.write({'copy_ids': [Command.create({'name': c}) for c in copy_codes]})
    #   - Las tuplas mágicas (0, 0, {...}) siguen existiendo por RPC, pero en
    #     Python se usan los objetos Command.
    # =========================================================================
    def exercise_19_add_copies(self, copy_codes):
        raise NotImplementedError('EJERCICIO 19 pendiente: Command.create')

    # =========================================================================
    # EJERCICIO 20 · Bloque 3 · Test: TestRelations.test_ex20_set_and_clear_genres
    # -------------------------------------------------------------------------
    # a) exercise_20_set_genres(genre_names): deja en genre_ids EXACTAMENTE los
    #    géneros indicados (los crea si no existen). Devuelve genre_ids.
    # b) exercise_20_clear_genres(): quita todos los géneros. Devuelve True.
    # OBLIGATORIO: usa Command.set y Command.clear.
    # PISTA: self.write({'genre_ids': [Command.set(ids)]})
    #        self.write({'genre_ids': [Command.clear()]})
    # =========================================================================
    def exercise_20_set_genres(self, genre_names):
        raise NotImplementedError('EJERCICIO 20 pendiente: Command.set')

    def exercise_20_clear_genres(self):
        raise NotImplementedError('EJERCICIO 20 pendiente: Command.clear')

    # =========================================================================
    # EJERCICIO 23 · Bloque 3 · Test: TestRelations.test_ex23_read_group
    # -------------------------------------------------------------------------
    # Devuelve el resultado de agrupar TODOS los libros por `state` y
    # contar cuántos hay en cada estado, usando _read_group (Odoo 19 ya no
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
    # Devuelve los libros en estado 'available' ordenados por coste
    # descendente, trayendo SOLO los campos name y replacement_cost a la caché.
    # PISTA: search_fetch(dominio, ['name', 'replacement_cost'],
    #                     order='replacement_cost desc')
    #        search_fetch combina search + fetch en una sola consulta (Odoo 16.2+).
    # =========================================================================
    @api.model
    def exercise_24_search_fetch_available(self):
        raise NotImplementedError('EJERCICIO 24 pendiente: search_fetch')

    # =========================================================================
    # EJERCICIO 28 · Bloque 4 · Test: TestViews.test_ex28_button_and_method
    # -------------------------------------------------------------------------
    # a) Implementa action_mark_available(): pasa a 'available' todos los
    #    libros de self que estén en 'draft'. Devuelve True.
    #    PISTA: self.filtered(lambda b: b.state == 'draft').write({...})
    # b) Abre views/cd_library_book_views.xml y añade el botón en el header
    #    (hay instrucciones dentro del XML).
    # =========================================================================
    def action_mark_available(self):
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
    # Método de ayuda YA implementado: abre el asistente de préstamo.
    # Te sirve de ejemplo de cómo devolver un act_window con contexto.
    # -------------------------------------------------------------------------
    def action_open_loan_wizard(self):
        self.ensure_one()
        return {
            'name': 'Nuevo préstamo',
            'type': 'ir.actions.act_window',
            'res_model': 'cd.library.loan.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_book_id': self.id},
        }
