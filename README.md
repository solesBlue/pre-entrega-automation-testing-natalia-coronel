# Pre-entrega - Automation QA

Proyecto de automatización de pruebas funcionales realizado como parte del curso de Automation QA de Talento Lab.

## Propósito del proyecto

El objetivo del proyecto es automatizar pruebas sobre el sitio web: 
https://www.saucedemo.com/

Que permiten verificar:

- Inicio de sesión
- Navegación y visualización del catálogo de productos
- Visualización de elementos principales de la interfaz
- Agregado de productos al carrito
- Actualización del contador del carrito
- Navegación hacia el carrito de compras
- Verificación del producto agregado al carrito

Las pruebas fueron desarrolladas de forma independiente, preparando en cada caso las precondiciones necesarias para su ejecución.

## Tecnologías utilizadas

- Python 3
- Pytest
- Selenium WebDriver
- Google Chrome
- Git
- GitHub

## Comando para ejecutar las pruebas 
python -m pytest tests/test_saucedemo.py -v

## Estructura del proyecto

```text
pre-entrega-automation-testing-natalia-coronel/
│
├── tests/
│   └── test_saucedemo.py
│
├── utils/
│   └── helpers.py
│
├── .gitignore
└── README.md

