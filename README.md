E-commerce API

E-commerce API Features:

    - Customer and CustomerAccount Management:
      - Create Customer
      - Read Customer
      - Update Customer
      - Delete Customer
      - Create CustomerAccount
      - Read CustomerAccount
      - Update CustomerAccount
      - Delete CustomerAccount

    - Product Catalog:
      - Create Product
      - Read Product
      - Update Product
      - Delete Product
      - List Products
      - View and Manage Product Stock Levels
      - Restock Products When Low

    - Order Processing:
      - Place Order
      - Retrieve Order
      - Track Order
      - Manage Order History
      - Cancel Order
      - Calculate Order Total Price

    - Database Integration

    - Data Validation and Error Handling

    - User Interface

Endpoits:

    - Customer and CustomerAccount endpoints:
      - Create Customer: POST /customers
      - Read Customer: GET /customers/<id>
      - Update Customer: PUT /customers/<id>
      - Delete Customer: DELETE /customers/<id>
      - Create CustomerAccount: POST /customer_accounts
      - Read CustomerAccount: GET /customer_accounts/<id>
      - Update CustomerAccount: PUT /customer_accounts/<id>
      - Delete CustomerAccount: DELETE /customer_accounts/<id>

    - Product:
      - Create Product: POST /products
      - Read Product: GET /products/<id>
      - Update Product: PUT /products/<id>
      - Delete Product: DELETE /products/<id>
      - List Products:GET /products
      
    - Order:
      - Place Order: POST /orders
      - Retrieve Order: GET /orders/<id>
      - Track Order: 
      - Manage Order History: GET /customers/<customer_id>/orders
      - Cancel Order: POST /orders/<id>/cancel
      - Calculate Order Total Price: GET /orders/<id>/total_price

    - Stock Management:
      - update_product_stock: PUT /products/<id>/stock
      - restock_products: POST/products/restock

Contributing

Contributions to enhance this application are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

Support

If you encounter any issues, please open a problem on the project's GitHub page.

Author info

Wamisho Debero - [wamisho-d/E-commerce API/]https://github.com/wamisho-d/ecommerce_app/edit/main/README.md
