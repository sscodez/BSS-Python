import asyncio
import aiocoap.resource as resource
import aiocoap

class BikeInventory:
    def _init_(self):
        self.bikes = []

    def add_bike(self, bike_name):
        self.bikes.append(bike_name)

    def get_bikes(self):
        return self.bikes

class GetBikesResource(resource.Resource):
    def _init_(self, inventory):
        super()._init_()
        self.inventory = inventory

    async def render_get(self, request):
        bikes = self.inventory.get_bikes()
        response_payload = "Available bikes: {}".format(", ".join(bikes))
        return aiocoap.Message(payload=response_payload.encode('utf-8'))

class AddBikeResource(resource.Resource):
    def _init_(self, inventory):
        super()._init_()
        self.inventory = inventory

    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        self.inventory.add_bike(payload)
        response_payload = "Added bike: {}".format(payload)
        return aiocoap.Message(payload=response_payload.encode('utf-8'))

class AvailalbeBikesResource(resource.Resource):
        async def render_get(self, request):
         response_payload = b'{"message": "Hello, CoAP! ,message": "Hello, CoAP! ,message": "Hello, CoAP! ,message": "Hello, CoAP! message": "Hello, CoAP! ,message": "Hello, CoAP!  "}'
         return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])

class NonAvailalbeBikesResource(resource.Resource):
        async def render_get(self, request):
         response_payload = b'{"message": "Hello, CoAP! ,message": "Hello, CoAP! ,message": "Hello, CoAP! ,message": "Hello, CoAP! message": "Hello, CoAP! ,message": "Hello, CoAP!  "}'
         return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])

      
class EchoResource(resource.Resource):
    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        response_payload = f'Received POST request with JSON payload: {payload}'.encode('utf-8')
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])

class RentBikeResource(resource.Resource):
    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        response_payload = f'Received POST request with JSON payload: {payload}'.encode('utf-8')
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])

class EndRentBikeResource(resource.Resource):
    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        response_payload = f'Received POST request with JSON payload: {payload}'.encode('utf-8')
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])

class RearBrakeResource(resource.Resource):
    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        response_payload = f'Received POST request with JSON payload: {payload}'.encode('utf-8')
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])


class FrontBrakeResource(resource.Resource):
    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        response_payload = f'Received POST request with JSON payload: {payload}'.encode('utf-8')
        return aiocoap.Message(payload=response_payload, content_format=aiocoap.numbers.media_types_rev['application/json'])


def main():
    inventory = BikeInventory()
    root = resource.Site()
    root.add_resource(['.well-known', 'core'], resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['hello'], BasicResource())
    root.add_resource(['getbikes'], GetBikesResource(inventory))
    root.add_resource(['addbikes'], AddBikeResource(inventory))
    root.add_resource(['echo'], EchoResource())

    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5688)))
    print("CoAP server running on port 5688")


    asyncio.get_event_loop().run_forever()

if _name_ == "_main_":
    main()
