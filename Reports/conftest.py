"""
Configuración global de Pytest
Basado en Clase 4 - pytest-html
"""

import pytest
from datetime import datetime
import os


def pytest_configure(config):
    """
    Configuración inicial de Pytest (Clase 4)
    Crea carpetas necesarias
    """
    # Crear carpeta reports si no existe
    if not os.path.exists("reports"):
        os.makedirs("reports")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de Pytest que captura screenshots en caso de fallos
    Concepto visto en Clase 4 (reportes) y Clase 8 (Selenium)
    """
    outcome = yield
    report = outcome.get_result()
    
    # Solo capturar screenshot si el test falló
    if report.when == "call" and report.failed:
        # Obtener el driver del fixture
        driver = item.funcargs.get('driver', None)
        
        if driver:
            # Crear carpeta reports si no existe
            if not os.path.exists("reports"):
                os.makedirs("reports")
            
            # Generar nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name
            screenshot_path = f"reports/FAILED_{test_name}_{timestamp}.png"
            
            # Guardar screenshot
            try:
                driver.save_screenshot(screenshot_path)
                print(f"\n📸 Screenshot de fallo guardada: {screenshot_path}")
            except Exception as e:
                print(f"Error al capturar screenshot: {e}")