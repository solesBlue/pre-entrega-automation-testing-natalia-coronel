#from concurrent.futures import wait

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import login, agregar_primer_producto
##import time

@pytest.fixture() 
##@pytest.fixture (scope="module")
##scope="module"sirve para que el driver se inicie una sola vez por módulo de prueba. En este caso usamos el helper driver() para iniciar el driver y cerrarlo al final de todas las pruebas del módulo, asi que no hace falta usar scope="module" en este caso.
def driver():
    #service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

## Automatización de Login
def test_01_saucedemo_login(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.url_contains("/inventory.html")
    )
    assert "/inventory.html" in driver.current_url, "Error! Login failed: No se redirigió a la página de inventario (/inventory.html)."


    inicio_producto = driver.find_element(By.CSS_SELECTOR, ".title")

    assert inicio_producto.text == "Products", \
        "Error! No se visualiza la sección Products."

## Navegación y verificación del catálogo: (Clases 6 a 8)
def test_02_catalogo(driver):
    login(driver)  ##utiliza la función login() definida en helpers.py para iniciar sesión antes de realizar las verificaciones del catálogo
    
    page_title = driver.title
    section_title = driver.find_element(By.CLASS_NAME, "title").text

    assert page_title == "Swag Labs", "Error! El título de la página no coincide con 'Swag Labs'. Se indica en el título actual: " + page_title

    assert section_title == "Products", "Error! El título de la sección no coincide con 'Products'. Se indica en el título actual: " + section_title

def test_03_productos_visibles(driver):
    login(driver)  
    productos_lista = driver.find_elements(By.CLASS_NAME, "inventory_item")

    assert len(productos_lista) > 0, "Error! No se encontraron productos visibles en el catálogo."

    nombre_producto = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    precio_producto= driver.find_elements(By.CLASS_NAME, "inventory_item_price")

    ##requisito: validar que el primer producto tenga nombre y precio
    nombre_primer_producto = nombre_producto[0].text
    precio_primer_producto = precio_producto[0].text

    assert nombre_primer_producto != "", \
        "Error! El primer producto no posee nombre."

    assert precio_primer_producto != "", \
        "Error! El primer producto no posee precio."

    print("Nombre del producto:", nombre_primer_producto)
    print("Precio:", precio_primer_producto)


def test_04_validar_UI (driver):
    login(driver)  

    menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
    assert menu_button.is_displayed(), "Error! El botón de menú no es visible."

    filtros = driver.find_element(By.CLASS_NAME, "product_sort_container")
    assert filtros.is_displayed(), "Error! El filtro de productos no es visible."

## Interacción con productos: (Clase 8)
def test_05_agregar_producto(driver):
    login(driver)  

    # boton_agregar = driver.find_elements(By.CLASS_NAME, "btn_inventory")[0]
    # boton_agregar.click()

    agregar_primer_producto(driver)

    # Esperar que el botón cambie a "Remove"
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "btn_inventory"),"Remove")
    )

    boton_remove = driver.find_elements(By.CLASS_NAME,"btn_inventory")[0]
    assert boton_remove.text == "Remove", "Error! El botón no cambió a 'Remove' después de agregar el producto al carrito."

def test_06_verificar_carrito(driver):
    login(driver)  
    agregar_primer_producto(driver)

    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"),"1")
    )

    contador_carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert contador_carrito == "1", "Error! El contador del carrito no muestra '1' después de agregar un producto. Se muestra: " + contador_carrito

def test_07_navegar_carrito(driver):
    login(driver)  

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/cart.html"))

    assert "/cart.html" in driver.current_url, "Error! No se redirigió a la página del carrito (/cart.html)."

def test_08_verificar_producto_agregado(driver):
    login(driver)  

    # Obtener datos del primer producto
    nombre_producto = driver.find_elements(By.CLASS_NAME,"inventory_item_name")[0].text
    precio_producto = driver.find_elements(By.CLASS_NAME,"inventory_item_price")[0].text

    agregar_primer_producto(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/cart.html")
)

    nombre_producto_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio_producto_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_price").text

    assert nombre_producto_carrito == nombre_producto, \
        "Error! El producto del carrito no coincide con el producto agregado."

    assert precio_producto_carrito == precio_producto, \
        "Error! El precio del producto en el carrito no coincide con el precio del catálogo."

    print("Nombre del producto en el carrito:", nombre_producto_carrito)
    print("Precio del producto en el carrito:", precio_producto_carrito)