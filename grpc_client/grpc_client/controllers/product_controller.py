from pyramid.view import view_defaults, view_config
from pyramid.response import Response
from grpc_client.grpc.product_client import GrpcClient


@view_defaults(renderer="json", route_name="product")
class ProductView:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get(self):
        try:
            if self.request.params.get("id") is not None:
                client = GrpcClient()

                response = client.get_product(id=self.request.params.get("id"))

                if response is None:
                    return Response(status=404, json_body={"message": "not found"})

                return Response(status=200, json_body={"data": response})

            client = GrpcClient()

            response = client.get_products()

            if response is []:
                return Response(status=404, json_body={"message": "not found"})

            return Response(status=200, json_body={"data": response})

        except Exception as e:
            return Response(status=500, json_body={"message": str(e)})

    @view_config(request_method="POST")
    def post(self):
        try:
            if (
                "name" not in self.request.json_body
                or "description" not in self.request.json_body
                or "price" not in self.request.json_body
                or "image" not in self.request.json_body
                or "stock" not in self.request.json_body
            ):
                return Response(
                    status=400,
                    json_body={"status": False, "message": "Bad Request"},
                )

            client = GrpcClient()

            response = client.create_product(
                name=self.request.json_body["name"],
                price=self.request.json_body["price"],
                description=self.request.json_body["description"],
                stock=self.request.json_body["stock"],
                image=self.request.json_body["image"],
            )

            return Response(status=200, json_body={"data": response})

        except Exception as e:
            return Response(status=500, json_body={"message": str(e)})

    @view_config(request_method="PUT")
    def put(self):
        try:
            if (
                "id" not in self.request.json_body
                or "name" not in self.request.json_body
                or "description" not in self.request.json_body
                or "price" not in self.request.json_body
                or "image" not in self.request.json_body
                or "stock" not in self.request.json_body
            ):
                return Response(
                    status=400,
                    json_body={"status": False, "message": "Bad Request"},
                )

            client = GrpcClient()

            response = client.update_product(
                id=self.request.json_body["id"],
                name=self.request.json_body["name"],
                price=self.request.json_body["price"],
                description=self.request.json_body["description"],
                stock=self.request.json_body["stock"],
                image=self.request.json_body["image"],
            )

            return Response(status=200, json_body={"data": response})

        except Exception as e:
            return Response(status=500, json_body={"message": str(e)})

    @view_config(request_method="DELETE")
    def delete(self):
        try:
            if "id" not in self.request.json_body:
                return Response(
                    status=400,
                    json_body={"status": False, "message": "Bad Request"},
                )

            client = GrpcClient()

            response = client.delete_product(id=self.request.json_body["id"])

            return Response(status=200, json_body={"data": response})

        except Exception as e:
            return Response(status=500, json_body={"message": str(e)})
