"""
Funciones auxiliares para tests de SauceDemo
Basado en conocimientos de Clases 1-8
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_saucedemo(driver, username, password):
    """
    Realiza el login en SauceDemo
    Basado en el código de ejemplo de Clase 8
    
    Args:
        driver: WebDriver instance
        username (str): Nombre de usuario
        password (str): Contraseña
    """
    # Esperar a que se cargue el formulario de login (Clase 8)
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    
    # Ingresar credenciales (Clase 8)
    username_input.send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    
    # Hacer clic en el botón de login (Clase 8)
    driver.find_element(By.ID, "login-button").click()
    
    # Verificar que el login fue exitoso (Clase 8)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item"))
    )


def agregar_producto_al_carrito(driver, indice=0):
    """
    Agrega un producto al carrito por su índice
    Basado en ejercicios de Clase 7 y 8
    
    Args:
        driver: WebDriver instance
        indice (int): Índice del producto (0 para el primero)
    
    Returns:
        dict: Información del producto agregado (nombre, precio)
    """
    # Obtener productos (Clase 7)
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    producto = productos[indice]
    
    # Obtener información del producto (Clase 8)
    nombre = producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = producto.find_element(By.CLASS_NAME, "inventory_item_price").text
    
    # Click en botón "Add to cart" usando tag (Clase 7)
    boton = producto.find_element(By.TAG_NAME, "button")
    boton.click()
    
    return {
        "nombre": nombre,
        "precio": precio
    }


def obtener_contador_carrito(driver):
    """
    Obtiene el valor del contador del carrito
    Basado en Clase 8
    
    Args:
        driver: WebDriver instance
    
    Returns:
        str: Número de items en el carrito, o "0" si está vacío
    """
    try:
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        return badge.text
    except:
        return "0"


def navegar_al_carrito(driver):
    """
    Navega a la página del carrito de compras
    Basado en Clase 8
    
    Args:
        driver: WebDriver instance
    """
    carrito_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    carrito_link.click()
    
    # Esperar a que cargue la página del carrito
    WebDriverWait(driver, 10).until(
        EC.url_contains("/cart.html")
    )