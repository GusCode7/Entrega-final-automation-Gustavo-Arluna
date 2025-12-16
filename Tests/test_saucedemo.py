"""
Pre-Entrega Automatización QA
Gustavo Arluna
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import SauceDemoHelpers
import time

class TestSauceDemo:
    """Clase principal de tests para SauceDemo"""
    
    @pytest.fixture(scope="function")
    def driver(self):
        """
        Fixture que inicializa y cierra el driver de Selenium
        Se ejecuta antes y después de cada test
        """
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    def test_login_exitoso(self, driver):
        """
        Test 1: Automatización de Login
        - Navega a saucedemo.com
        - Ingresa credenciales válidas
        - Valida redirección exitosa a /inventory.html
        """
        helper = SauceDemoHelpers(driver)
        
        # Navegar a la página de login
        driver.get("https://www.saucedemo.com/")
        
        # Ingresar credenciales válidas
        username = "standard_user"
        password = "secret_sauce"
        
        helper.login(username, password)
        
        # Validar login exitoso con espera explícita
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("/inventory.html"))
        
        # Verificar URL contiene /inventory.html
        assert "/inventory.html" in driver.current_url, "No se redirigió correctamente a inventory"
        
        # Verificar presencia del título "Products" o "Swag Labs"
        title_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        assert title_element.text == "Products", f"Título incorrecto: {title_element.text}"
        
        print("✓ Login exitoso validado correctamente")
    
    def test_navegacion_y_catalogo(self, driver):
        """
        Test 2: Navegación y Verificación del Catálogo
        - Valida título de la página
        - Verifica presencia de productos
        - Lista nombre y precio del primer producto
        - Valida elementos de la interfaz (menú, filtros)
        """
        helper = SauceDemoHelpers(driver)
        
        # Realizar login primero
        driver.get("https://www.saucedemo.com/")
        helper.login("standard_user", "secret_sauce")
        
        wait = WebDriverWait(driver, 10)
        
        # Validar título de la página
        title_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        assert title_element.text == "Products", "El título de la página no es correcto"
        print(f"✓ Título validado: {title_element.text}")
        
        # Verificar presencia de productos
        productos = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
        )
        assert len(productos) > 0, "No se encontraron productos en el catálogo"
        print(f"✓ Productos encontrados: {len(productos)}")
        
        # Listar nombre y precio del primer producto
        primer_producto = productos[0]
        nombre = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
        precio = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text
        
        print(f"✓ Primer producto - Nombre: {nombre}, Precio: {precio}")
        
        # Validar elementos importantes de la interfaz
        # Menú hamburguesa
        menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
        assert menu_button.is_displayed(), "El menú no está visible"
        print("✓ Menú hamburguesa presente")
        
        # Filtro de productos
        filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")
        assert filtro.is_displayed(), "El filtro de productos no está visible"
        print("✓ Filtro de productos presente")
        
        # Carrito de compras
        carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        assert carrito.is_displayed(), "El carrito de compras no está visible"
        print("✓ Carrito de compras presente")
    
    def test_interaccion_carrito(self, driver):
        """
        Test 3: Interacción con Productos y Carrito
        - Añade primer producto al carrito
        - Verifica incremento del contador
        - Navega al carrito
        - Comprueba que el producto aparezca en el carrito
        """
        helper = SauceDemoHelpers(driver)
        
        # Realizar login
        driver.get("https://www.saucedemo.com/")
        helper.login("standard_user", "secret_sauce")
        
        wait = WebDriverWait(driver, 10)
        
        # Obtener el primer producto
        productos = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
        )
        primer_producto = productos[0]
        
        # Guardar información del producto antes de agregarlo
        nombre_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
        precio_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text
        
        print(f"Producto a agregar: {nombre_producto} - {precio_producto}")
        
        # Añadir producto al carrito
        boton_add = primer_producto.find_element(By.TAG_NAME, "button")
        boton_add.click()
        print("✓ Producto agregado al carrito")
        
        # Verificar que el contador del carrito se incremente
        contador_carrito = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        assert contador_carrito.text == "1", f"El contador debería ser 1, pero es {contador_carrito.text}"
        print(f"✓ Contador del carrito: {contador_carrito.text}")
        
        # Navegar al carrito de compras
        carrito_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        carrito_link.click()
        
        # Esperar a que cargue la página del carrito
        wait.until(EC.url_contains("/cart.html"))
        print("✓ Navegado al carrito")
        
        # Verificar que el producto aparezca en el carrito
        item_en_carrito = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        
        nombre_en_carrito = item_en_carrito.find_element(By.CLASS_NAME, "inventory_item_name").text
        precio_en_carrito = item_en_carrito.find_element(By.CLASS_NAME, "inventory_item_price").text
        
        # Validar que el producto en el carrito sea el mismo que agregamos
        assert nombre_en_carrito == nombre_producto, f"El nombre no coincide: {nombre_en_carrito} vs {nombre_producto}"
        assert precio_en_carrito == precio_producto, f"El precio no coincide: {precio_en_carrito} vs {precio_producto}"
        
        print(f"✓ Producto verificado en carrito: {nombre_en_carrito} - {precio_en_carrito}")
        print("✓ Test de carrito completado exitosamente")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=reports/reporte.html", "--self-contained-html"])