# Flask CRUD de Usuarios

Aplicación de ejemplo para login y CRUD de usuarios usando Flask y MySQL.

## Requisitos
- Python 3.8+
- MySQL/MariaDB
- `pip install -r requirements.txt`

## Estructura
- `app.py`: aplicación Flask principal.
- `templates/`: plantillas HTML.
- `schema.sql`: script de creación de la base de datos y tabla.

## Configuración
1. Crear una base de datos MySQL, por ejemplo `flasklab`.
2. Ejecutar `schema.sql` en MySQL.
3. Ajustar los datos de conexión en `app.py`:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
4. Ejecutar:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

## Abrir en VS Code
- Abre VS Code.
- Selecciona `File > Open Folder...` y elige `C:\Users\Usuario\Documents\flask_admin_crud`.
- Inserta la carpeta en VS Code y usa el depurador con la configuración en `.vscode/launch.json`.

## Uso
- Navegar a `http://127.0.0.1:5000`.
- Iniciar sesión con el usuario admin creado en `schema.sql`.
- Usar el panel para crear, editar y eliminar usuarios.

## Observaciones
- El usuario administrador puede ver y gestionar todos los registros.
- Si quieres evitar que el administrador se elimine a sí mismo, no uses el botón de eliminar sobre el propio usuario.
