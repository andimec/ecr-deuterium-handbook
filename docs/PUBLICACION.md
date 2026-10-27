# Creación del repositorio y publicación en GitHub Pages

## A. Crear el repositorio público

1. Inicia sesión en GitHub con la cuenta `andimec`.
2. Abre https://github.com/new.
3. En **Owner**, selecciona `andimec`.
4. En **Repository name**, escribe `ecr-deuterium-handbook`.
5. En **Visibility**, selecciona **Public**.
6. Para publicar desde el paquete que ya contiene `README.md`, deja **Add a README**, **.gitignore** y **Choose a license** sin seleccionar. Es importante comenzar con un repositorio vacío.
7. Pulsa **Create repository**.

## B. Subir el contenido

Extrae el ZIP del proyecto y abre un terminal dentro del directorio `ecr-deuterium-handbook` (el que contiene este README).

```bash
git init -b main
git add .
git commit -m "docs: initial ECR deuterium handbook"
git remote add origin https://github.com/andimec/ecr-deuterium-handbook.git
git push -u origin main
```

El `push` requiere autenticación GitHub a través del gestor de credenciales o de `gh auth login`; GitHub ya no acepta contraseñas de cuenta como método de autenticación para este proceso. Si el directorio tiene un repositorio Git previo, no repitas `git init` y comprueba `git remote -v`.

## C. Activar GitHub Pages

1. En el repositorio nuevo, abre **Settings**.
2. En la barra lateral entra en **Pages**.
3. En **Build and deployment → Source**, elige **GitHub Actions**.
4. En **Actions**, selecciona el workflow **Verificar y publicar manual ECR**.
5. Comprueba que los trabajos `build` y `deploy` terminan correctamente. Si no hay una ejecución, utiliza **Run workflow** en la rama `main`.
6. Abre https://andimec.github.io/ecr-deuterium-handbook/ una vez que GitHub confirme el despliegue.

No es necesario configurar `gh-pages`, `CNAME`, un dominio privado ni claves secretas. El workflow utiliza el `GITHUB_TOKEN` efímero suministrado por GitHub Actions con permisos mínimos para Pages. El sitio puede tardar algunos minutos en propagarse después del despliegue.

## D. Mantener la página

- El contenido está en `content/manual_ecr_deuterio.md`. Edítalo en GitHub con el icono de lápiz. Guarda con un commit en `main` para actualizar el sitio.
- Los cálculos y la interfaz están en `scripts/construir_manual.py`. Edita con una rama y pull request, porque un cambio en ecuaciones o JavaScript exige revisar resultados.
- Cada `push` a `main` ejecuta comprobaciones, genera la página y la publica.
- Las pull requests ejecutan el proceso de compilación y validación, pero **no publican**.
- El editor de Markdown incluido en la web permite cambios locales y exportarlos, pero no hace commits a GitHub. Copia o sube el archivo exportado a `content/manual_ecr_deuterio.md` para publicar los cambios.
- Las ecuaciones se componen con MathJax desde un CDN; se necesita conexión para su visualización tipográfica. El texto y las calculadoras no requieren otro servicio.

## E. Resolución de problemas

- **404 en Pages:** verifica que el repositorio existe, es público y que el workflow desplegó correctamente; consulta `Settings → Pages` para la URL publicada.
- **No arranca el workflow:** confirma que `pages.yml` está en `.github/workflows/` y la rama se llama `main`; desde `Actions` ejecútalo manualmente.
- **Build falla:** revisa el log del paso fallido. Las pruebas son estrictas y evitan publicar una versión incoherente.
- **Cambios en el Markdown no aparecen:** comprueba que el commit está en `main`, que el workflow terminó y recarga el navegador.
- **Ecuaciones sin renderizar:** verifica la conexión a `cdn.jsdelivr.net` para MathJax; el contenido LaTeX sigue siendo legible.
- **Páginas deshabilitadas por políticas institucionales:** revisa configuraciones de acciones y permisos de la cuenta o del repositorio.

Referencia oficial: https://docs.github.com/es/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
