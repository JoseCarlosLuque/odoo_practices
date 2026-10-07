# Prácticas de Odoo 19

Colección de módulos de laboratorio para practicar el desarrollo backend en
Odoo 19 con casos reales de negocio. Cada módulo propone 35 ejercicios
organizados en 6 bloques, de menos a más dificultad, con tests autocorrectivos
para validar tus soluciones.

| Módulo | Temática | Tag de tests | Modelo principal |
|--------|----------|--------------|------------------|
| [`cd_practices`](cd_practices/README.md) | Elementos y reservas (genérico) | `cd_practice` | `cd.practice.item` |
| [`cd_library_practices`](cd_library_practices/README.md) | Biblioteca | `cd_library_practice` | `cd.library.book` |
| [`cd_vet_practices`](cd_vet_practices/README.md) | Clínica veterinaria | `cd_vet_practice` | `cd.vet.pet` |
| [`cd_gym_practices`](cd_gym_practices/README.md) | Gimnasio | `cd_gym_practice` | `cd.gym.membership` |
| [`cd_clothes_practices`](cd_clothes_practices/README.md) | Tienda de ropa | `cd_clothes_practice` | `cd.clothes.product` |
| [`cd_furniture_practices`](cd_furniture_practices/README.md) | Fábrica de muebles | `cd_furniture_practice` | `cd.furniture.product` |
| [`cd_restaurant_practices`](cd_restaurant_practices/README.md) | Restaurante | `cd_restaurant_practice` | `cd.restaurant.dish` |

Todos parten del mismo temario, así que puedes hacerlos en cualquier orden:
cada uno refuerza los mismos conceptos sobre un dominio distinto.

## Cómo funciona cada módulo

Cada ejercicio está marcado en el código con un bloque de comentarios
`EJERCICIO N` y, casi siempre, con un método que lanza `NotImplementedError`
hasta que lo resuelvas. Los ejercicios declarativos (crear un campo, una vista,
un grupo de seguridad...) se resuelven escribiendo tú el código donde indican
los comentarios. Cada módulo tiene su propio `README.md` con el índice completo
de ejercicios y los comandos exactos.

Los bloques son:

1. **ORM básica**: `create`, `search`, dominios, recordsets.
2. **Campos y decoradores**: computes, `related`, `onchange`, constraints.
3. **Relaciones y ORM avanzada**: `Command`, `_inherits`, `_read_group`.
4. **Vistas y acciones XML**: list/form, herencia de vistas, server actions.
5. **Seguridad**: grupos, ACL, record rules, `has_access`.
6. **Mail, wizards y crons**: chatter, `TransientModel`, `ir.cron`.

Los tests están etiquetados `-standard`, por lo que no se ejecutan al instalar
el módulo: solo cuando pasas `--test-tags=<tag>`.

## Instalación

Coloca este directorio (o los módulos que quieras) en el `addons_path` de tu
Odoo 19 e instala el módulo desde Ajustes o por línea de comandos:

```bash
odoo -d MI_BD -i cd_library_practices --stop-after-init
```

Con Docker (imagen `odoo:19`):

```bash
docker run --rm -v "$PWD:/mnt/extra-addons" --network host odoo:19 \
    odoo -d MI_BD -i cd_library_practices --stop-after-init \
         --db_host=localhost --db_user=odoo --db_password=odoo
```

Los datos de demo se cargan en bases creadas con demo habilitada. En una base
nueva creada por línea de comandos, añade `--without-demo=False` si los quieres.

## Validar tus soluciones

Ejecuta los tests del módulo (y solo esos) con su tag:

```bash
# Biblioteca
odoo -d MI_BD -u cd_library_practices --stop-after-init --test-enable --test-tags=cd_library_practice

# Veterinaria
odoo -d MI_BD -u cd_vet_practices --stop-after-init --test-enable --test-tags=cd_vet_practice

# Gimnasio
odoo -d MI_BD -u cd_gym_practices --stop-after-init --test-enable --test-tags=cd_gym_practice

# Tienda de ropa
odoo -d MI_BD -u cd_clothes_practices --stop-after-init --test-enable --test-tags=cd_clothes_practice

# Fábrica de muebles
odoo -d MI_BD -u cd_furniture_practices --stop-after-init --test-enable --test-tags=cd_furniture_practice

# Restaurante
odoo -d MI_BD -u cd_restaurant_practices --stop-after-init --test-enable --test-tags=cd_restaurant_practice

# Genérico
odoo -d MI_BD -u cd_practices --stop-after-init --test-enable --test-tags=cd_practice
```

Puedes ejecutar solo un bloque o un test concreto:

```bash
--test-tags=cd_library_practice:TestOrmBasics              # bloque 1 completo
--test-tags=cd_library_practice:TestFields.test_ex09_cost_with_tax
```

Mientras no resuelvas un ejercicio, sus tests fallarán con el mensaje
`EJERCICIO N pendiente: ...`; es lo esperado.

## Pistas generales de Odoo 19

- `Command` se importa de `odoo.fields` (`from odoo.fields import Command`).
- Las constraints SQL se declaran con `models.Constraint` y el nombre debe
  empezar por `_`.
- `name_get()` ya no existe: se usa `_compute_display_name`.
- `read_group()` está deprecado: usa `_read_group()`.
- `get_view()` ha desaparecido; ahora existe `get_views()` / `get_combined_arch()`.
- Los grupos de usuario están en `res.users.group_ids` (ya no `groups_id`).
- En las vistas, `attrs` y `states` ya no existen: se usan expresiones Python en
  `invisible`, `readonly`, `required`.
- Documentación oficial: https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html
