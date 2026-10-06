# cd_practices · Ejercicios de Odoo 19

Módulo de laboratorio para practicar la ORM y otras herramientas de Odoo 19.
Cada ejercicio está marcado en el código con un bloque de comentarios
`EJERCICIO N` y, casi siempre, con un método que lanza `NotImplementedError`
hasta que lo resuelvas.

## Cómo se usa

1. Instala el módulo y abre el menú **Prácticas** (verás elementos, reservas y
   datos de demo para trastear).
2. Abre el bloque de código que indica la tabla de abajo y resuelve el
   ejercicio. Los ejercicios declarativos (crear un campo, una vista, un grupo,
   etc.) se resuelven escribiendo tú el código donde te indican los comentarios.
3. Valida tus soluciones con los tests autocorrectivos:

```bash
# Reescala y ejecuta los tests del módulo (tag cd_practice)
odoo -d MI_BD -u cd_practices --stop-after-init --test-enable --test-tags=cd_practice
```

Con Docker (imagen `odoo:19`):

```bash
docker run --rm -v "$PWD:/mnt/extra-addons" --network host odoo:19 \
    odoo -d cd_practice_test -i cd_practices --stop-after-init \
         --test-enable --test-tags=cd_practice \
         --db_host=localhost --db_user=odoo --db_password=odoo
```

Puedes ejecutar solo un bloque o un test concreto:

```bash
--test-tags=cd_practice:TestOrmBasics                 # bloque 1 completo
--test-tags=cd_practice:TestFields.test_ex09_price_with_tax
```

Los tests están etiquetados `-standard`, así que **no** se ejecutan al instalar
el módulo de forma normal: solo cuando pasas `--test-tags=cd_practice`.

## Índice de ejercicios

### Bloque 1 · ORM básica — `tests/test_01_orm_basics.py`

| # | Método (en `models/cd_practice_item.py`) | Qué practicas |
|---|------------------------------------------|---------------|
| 1 | `exercise_01_create_items` | `create()` con lista de vals |
| 2 | `exercise_02_search_items` | `search()`: dominio, `order`, `limit` |
| 3 | `exercise_03_count_items_by_owner` | `search_count()` |
| 4 | `exercise_04_expensive_item_names` | `filtered()` + `mapped()` + `sorted()` |
| 5 | `exercise_05_set_state` | `write()` sobre un recordset |
| 6 | `exercise_06_delete_cancelled` | `unlink()` sobre un recordset |
| 7 | `exercise_07_complex_domain` | Dominios: `|`, `&`, `ilike` |
| 8 | `exercise_08_browse_vs_search` | `browse()` + `exists()` |

### Bloque 2 · Campos y decoradores — `tests/test_02_fields.py`

| # | Dónde | Qué practicas |
|---|-------|---------------|
| 9 | `cd_practice_item.py` | Campo computado almacenado (`store=True`, `@api.depends`) |
| 10 | `cd_practice_item.py` | Compute no almacenado + `@api.depends_context` |
| 11 | `cd_practice_item_line.py` | Campo `related` |
| 12 | `cd_practice_item.py` | `@api.onchange` (se prueba con `odoo.tests.Form`) |
| 13 | `cd_practice_item.py` | `@api.constrains` + `ValidationError` |
| 14 | `cd_practice_item.py` | `models.Constraint` (novedad de Odoo 19, sustituye a `_sql_constraints`) |
| 15 | `cd_practice_item.py` | `default` con lambda y `copy=False` |
| 16 | `cd_practice_item.py` | `_compute_display_name` (`name_get` ya no existe) |
| 17 | `cd_practice_item.py` | Sobrescribir `copy()` |
| 18 | `cd_practice_item.py` | Campo `active` + `_order` |

### Bloque 3 · Relaciones y ORM avanzada — `tests/test_03_relations.py`

| # | Dónde | Qué practicas |
|---|-------|---------------|
| 19 | `cd_practice_item.py` | One2many con `Command.create` |
| 20 | `cd_practice_item.py` | Many2many con `Command.set` / `Command.clear` |
| 21 | `cd_practice_member.py` | Delegación con `_inherits` sobre `res.partner` |
| 22 | `cd_practice_item.py` | Compute con `inverse` + `Command.set` |
| 23 | `cd_practice_item.py` | `_read_group()` (`read_group` está deprecado) |
| 24 | `cd_practice_item.py` | `search_fetch()` / `fetch()` |

### Bloque 4 · Vistas y acciones XML — `tests/test_04_views.py`

| # | Dónde | Qué practicas |
|---|-------|---------------|
| 25 | `views/cd_practice_tag_views.xml` | Vistas list/form + acción + menú |
| 26 | `models/res_partner.py` | Extender `res.partner`: One2many, computed y acción |
| 27 | `views/res_partner_views.xml` | Herencia de vista con XPath sobre `base.view_partner_form` |
| 28 | `cd_practice_item.py` + `views/cd_practice_item_views.xml` | Botón `type="object"` con `invisible="..."` |
| 29 | `data/cd_practice_actions.xml` | `ir.actions.server` |

### Bloque 5 · Seguridad — `tests/test_05_security.py`

| # | Dónde | Qué practicas |
|---|-------|---------------|
| 30 | `security/cd_practice_security.xml` + `security/ir.model.access.csv` | Grupo propio + ACL |
| 31 | `security/cd_practice_security.xml` | Record rule por usuario |
| 32 | `cd_practice_item.py` | `has_access()` (API nueva de Odoo 18/19) |

### Bloque 6 · Mail, wizards y crons — `tests/test_06_mail_wizard_cron.py`

| # | Dónde | Qué practicas |
|---|-------|---------------|
| 33 | `models/cd_practice_booking.py` + su vista | `mail.thread`, `tracking`, chatter, `message_post` |
| 34 | `wizards/cd_practice_booking_wizard.py` | `TransientModel` + `act_window` |
| 35 | `cd_practice_booking.py` + `data/cd_practice_cron.xml` | `ir.cron` (en 19 hereda de `ir.actions.server`) |

## Modelos de laboratorio

| Modelo | Uso |
|--------|-----|
| `cd.practice.item` | Modelo principal: aquí viven casi todos los ejercicios |
| `cd.practice.tag` | Etiquetas para Many2many y para el ejercicio de vistas |
| `cd.practice.item.line` | Líneas para los ejercicios de One2many y `related` |
| `cd.practice.booking` | Reservas para mail, wizard y cron |
| `res.partner` (extendido) | Herencia de un modelo core |
| `cd.practice.member` | Lo creas tú en el ejercicio 21 |

## Pistas generales de Odoo 19

- `Command` se importa de `odoo.fields` (`from odoo.fields import Command`).
- Las constraints SQL se declaran como atributos de clase con `models.Constraint`
  y el nombre debe empezar por `_`.
- `name_get()` ya no existe: se sobrescribe `_compute_display_name`.
- `read_group()` está deprecado: usa `_read_group()`.
- `get_view()` ha desaparecido; ahora existe `get_views()` / `get_combined_arch()`.
- Los grupos de usuario están en `res.users.group_ids` (ya no `groups_id`).
- En las vistas, `attrs` y `states` ya no existen: se usan expresiones Python en
  `invisible`, `readonly`, `required`.
- Documentación oficial: https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html
