# **NetScanning - Escáner de Red**

**NetScanning** es una herramienta en Python diseñada para escanear redes, identificar hosts activos y analizar puertos abiertos. Es ideal para auditorías de red, permitiendo escaneos rápidos y sencillos.

## **Características Principales**
- **Detección de hosts** en la red.
- **Escaneo de puertos abiertos** en dispositivos detectados.
- Uso de las librerías `socket` y `subprocess` para la identificación de servicios.
- **Interfaz sencilla** y fácil de usar.

## **Modo de Uso**
1. Ejecuta el siguiente comando en la terminal:
   python3 NetScanning.py
# Actualizaciones

1. **Compatibilidad multiplataforma**:
   - El script ahora detecta automáticamente el sistema operativo (Windows, Linux, macOS) y utiliza el comando `ping` adecuado para cada uno.

2. **Validación de la red**:
   - Se agregó una validación para asegurarse de que la red ingresada esté en formato CIDR válido antes de proceder con el escaneo.

3. **Escaneo de puertos personalizados**:
   - Ahora el usuario puede ingresar un rango de puertos o puertos específicos (por ejemplo, `80,443,1-1024`).

4. **Manejo de errores mejorado**:
   - Se agregaron más bloques `try-except` para evitar que el programa se detenga inesperadamente.
   - Mensajes de error más descriptivos para facilitar la depuración.

5. **Generación de informes**:
   - Se agregó la opción de guardar los resultados del escaneo en un archivo de texto (`informe.txt` o un nombre personalizado).
   - El informe incluye hosts activos, puertos abiertos y banners de servicios.

6. **Interfaz más amigable**:
   - Mensajes de salida más claros y organizados, con indicadores como `[+]` para éxito y `[!]` para advertencias o errores.
   - Pregunta al usuario si desea guardar el informe antes de salir.

7. **Optimización de concurrencia**:
   - Ajuste del número de workers en `ThreadPoolExecutor` para equilibrar el rendimiento y el uso de recursos.

8. **Banner grabbing mejorado**:
   - Ahora el banner grabbing es más robusto y maneja mejor los errores al intentar obtener información de servicios.

9. **Verificación de permisos**:
   - El script verifica si el archivo de informe ya existe y muestra una advertencia antes de sobrescribirlo.
   - Muestra la ruta absoluta del archivo guardado para que el usuario sepa dónde se encuentra.

10. **Nombre personalizado del archivo de informe**:
    - El usuario puede elegir un nombre personalizado para el archivo de informe. Si no se especifica, se usa `informe.txt` por defecto.
