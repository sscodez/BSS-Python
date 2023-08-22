# Bike Sharing System CoAP Server with AIocoap and MySQL

This repository contains the implementation of a Bike Sharing System CoAP (Constrained Application Protocol) Server using the AIocoap library in Python and MySQL as the database backend. The server enables communication with IoT devices using the CoAP protocol to manage bike sharing operations.

## Features

- **CoAP Communication:** The server supports the CoAP protocol for efficient communication with IoT devices, making it suitable for constrained environments.

- **Bike Management:** Users can request information about available bikes, reserve bikes, and return bikes through CoAP requests.

- **Database Integration:** The server interacts with a MySQL database to store and retrieve bike and reservation data.

## Prerequisites

- Python 3.x
- MySQL database
- AIocoap library (`pip install aiocoap`)
- MySQL Connector (`pip install mysql-connector-python`)

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/bike-sharing-coap.git
   cd bike-sharing-coap
   ```

2. Set up the MySQL database:
   
   - Create a database named `bike_sharing`.
   - Execute the `database.sql` script to create the necessary tables.

3. Modify the `config.py` file:

   - Replace the placeholders with your MySQL database credentials.

## Usage

1. Start the CoAP server:

   ```bash
   python coap_server.py
   ```

2. IoT devices can now send CoAP requests to interact with the bike sharing system.

   - To get the list of available bikes: `GET coap://<server_ip>:5683/bikes`
   - To reserve a bike: `POST coap://<server_ip>:5683/reserve`
   - To return a bike: `POST coap://<server_ip>:5683/return`

## API Endpoints

- `GET /bikes`: Retrieve the list of available bikes.
- `POST /reserve`: Reserve a bike.
- `POST /return`: Return a bike.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was inspired by the need to create an efficient and lightweight bike sharing system using CoAP and MySQL.
- Thanks to the AIocoap developers and the open-source community for providing the necessary tools and resources.

---

**Note:** This README is a template and should be customized according to the actual implementation and project structure. Make sure to include accurate instructions, dependencies, and explanations that match your specific project.
