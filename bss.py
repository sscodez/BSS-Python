import asyncio
import aiocoap.resource as resource
import aiocoap
import mysql.connector


mysql_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'bss',
}

class BikeInventory:
    def __init__(self):
        self.bikes = []

    def add_bike(self, bike_name):
        self.bikes.append(bike_name)

    def get_bikes(self):
        return self.bikes


class AvailableBikesResource(resource.Resource):
    async def render_get(self, request):
        try:
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM bikes  WHERE isRented = 0 ")
            result = cursor.fetchall()
            response_payload = str(result).encode('utf-8')
        except Exception as e:
            response_payload = f"Error: {str(e)}".encode('utf-8')
        finally:
            cursor.close()
            connection.close()
        
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])


class NonAvailableBikesResource(resource.Resource):
    async def render_get(self, request):
        try:
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM bikes  WHERE isRented = 1 ")
            result = cursor.fetchall()
            response_payload = str(result).encode('utf-8')
        except Exception as e:
            response_payload = f"Error: {str(e)}".encode('utf-8')
        finally:
            cursor.close()
            connection.close()
        
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])

class AddBikesResource(resource.Resource):
    async def render_post(self, request):
        try:
            payload = request.payload.decode('utf-8')
            bike_model, bike_name = payload.split(',')

            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()

            query = "INSERT INTO bikes (bikeModel, bikeName) VALUES (%s, %s)"
            values = (bike_model, bike_name)
            cursor.execute(query, values)
            connection.commit()

            response_payload = b'Data inserted successfully'

        except Exception as e:
            response_payload = f"Error: {str(e)}".encode('utf-8')
        finally:
            cursor.close()
            connection.close()
        
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])


class RentBikeResource(resource.Resource):
    async def render_post(self, request):
        try:
            payload = request.payload.decode('utf-8')
            bike_id, cyclist_id = payload.split(',')

            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()

            query = "UPDATE bikes SET isRented = %s , cyclistId = %s WHERE bikeId = %s "
            values = (1, bike_id, cyclist_id)
            cursor.execute(query, values)
            connection.commit()

            response_payload = b'Data updated successfully'

        except Exception as e:
            response_payload = f"Error: {str(e)}".encode('utf-8')
        finally:
            cursor.close()
            connection.close()
        
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])

class EndBikeResource(resource.Resource):
    async def render_post(self, request):
        try:
            payload = request.payload.decode('utf-8')
            bike_id, cyclist_id = payload.split(',')

            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()

            query = "UPDATE bikes SET isRented = %s , cyclistId = %s WHERE bikeId = %s "
            values = (0, bike_id, 0)
            cursor.execute(query, values)
            connection.commit()

            response_payload = b'Data updated successfully'

        except Exception as e:
            response_payload = f"Error: {str(e)}".encode('utf-8')
        finally:
            cursor.close()
            connection.close()
        
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])


class FrontBrakeResource(resource.Resource):
    async def render_post(self, request):
        try:
            payload = request.payload.decode('utf-8')
            bike_id = int(payload)

            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()

            # Get the current value of frontBrake
            query_select = "SELECT frontBrake FROM your_table WHERE bikeId = %s AND isRented = 1  "
            cursor.execute(query_select, (bike_id,))
            current_front_brake = cursor.fetchone()[0]

            # Toggle frontBrake value
            new_front_brake = 1 - current_front_brake

            # Update the frontBrake value
            query_update = "UPDATE your_table SET frontBrake = %s WHERE bikeId = %s AND isRented = 1  "
            cursor.execute(query_update, (new_front_brake, bike_id))
            connection.commit()

            response_payload = f'Front brake toggled. New value: {new_front_brake}'.encode('utf-8')

        except Exception as e:
            response_payload = f"Error: {str(e)}".encode('utf-8')
        finally:
            cursor.close()
            connection.close()
        
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])

class RearBrakeResource(resource.Resource):
    async def render_post(self, request):
        try:
            payload = request.payload.decode('utf-8')
            bike_id = int(payload)

            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()

            # Get the current value of frontBrake
            query_select = "SELECT rearBrake FROM bikes WHERE bikeId = %s AND isRented = 1  "
            cursor.execute(query_select, (bike_id,))
            current_front_brake = cursor.fetchone()[0]

            # Toggle frontBrake value
            new_rear_brake = 1 - current_front_brake

            # Update the frontBrake value
            query_update = "UPDATE bikes SET rearBrake = %s WHERE bikeId = %s AND isRented = 1 "
            cursor.execute(query_update, (new_rear_brake, bike_id))
            connection.commit()

            response_payload = f'Rear brake toggled. New value: {new_rear_brake}'.encode('utf-8')

        except Exception as e:
            response_payload = f"Error: {str(e)}".encode('utf-8')
        finally:
            cursor.close()
            connection.close()
        
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])



def main():
    inventory = BikeInventory()
    root = resource.Site()
    root.add_resource(['.well-known', 'core'], resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['addBikes'], AddBikesResource())
    root.add_resource(['nonavailableBikes'], NonAvailableBikesResource())
    root.add_resource(['availableBikes'], AvailableBikesResource())
    root.add_resource(['rentBikes'], RentBikeResource())
    root.add_resource(['endRentBikes'], EndBikeResource())
    root.add_resource(['frontBrake'], FrontBrakeResource())
    root.add_resource(['rearBrake'], RearBrakeResource())

    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5688)))
    print("CoAP server running on port 5688")


    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
