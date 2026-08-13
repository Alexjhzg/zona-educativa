# 🤝 Guía de Contribución - Zona Educativa

¡Gracias por tu interés en contribuir al proyecto **Zona Educativa**!

---

## 🛠️ Flujo de Trabajo (Workflow)

1. **Haz un Fork del Repositorio**.
2. **Crea una Rama para tu Feature o Fix**:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   # o
   git checkout -b fix/correccion-bug
   ```
3. **Sigue las Normas de Estilo**:
   - **Backend**: Python PEP8, sintaxis asíncrona en FastAPI y typing con Pydantic.
   - **Frontend**: Vue 3 `<script setup>`, naming conventions en camelCase y clases utilitarias de TailwindCSS.
4. **Prueba tus Cambios**:
   - Asegúrate de que los contenedores compilen sin errores:
     ```bash
     docker-compose up --build
     ```
5. **Haz Commit y Push**:
   ```bash
   git commit -m "feat: añade autocompletado en solicitudes"
   git push origin feature/nueva-funcionalidad
   ```
6. **Abre un Pull Request (PR)** describiendo los cambios realizados y capturas si aplica.

---

## 🐛 Reportar Problemas (Issues)

Si encuentras un error o tienes una propuesta de mejora, por favor abre un **Issue** incluyendo:
- Comportamiento esperado vs comportado real.
- Pasos para reproducir el problema.
- Logs o capturas de pantalla relevantes.
