# Sistema de Detección de Somnolencia

Sistema para detectar somnolencia en el conductor de vehículo.

---

## Tecnologías Usadas
- Python
- OpenCV
- Arduino

---

## **Requisitos Técnicos**

Para ejecutar la aplicación son necesarios tener instalados los siguientes requisitos en tu máquina local:

- Docker para la ejecución de la aplicación mediante contenedor.
- Python para ejecutar localmente.

---

## Descripción

Este sistema fue pensado para detectar signos de somnolencia en conductores de vehículos con el fin de alertar mediante una placa Arduino y un buzzer. Esto funciona a través del conteo de parpadeos y la duración de cada uno, para así poder determinar cuando el conductor presenta alguna señal de somnolencia o sueño.

# Pasos para ejecutar

1. **Clonar el repositorio** del proyecto en tu máquina local:
   ```bash
   git clone https://github.com/MarcoAntonioRG/Sistema-de-Somnolencia.git
   cd App-Rent-a-Car 

2. Instalar las librerías en un entorno local o virtual desde `requirements.txt` con:
   ```bash
   pip install -r requirements.txt
   ```
                      
4. Ejecutar la aplicación con:
   ```bash         
   python Detector_Micro_Sueño.py
   ```
                
   o con Docker mediante:
   ```bash
   docker compose up

5. Para cerrar la ventana de la aplicación basta con presionar el botón de cerrar o presionar la tecla `Esc`.
