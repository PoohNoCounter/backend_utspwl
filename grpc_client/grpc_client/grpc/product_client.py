import logging

import grpc

# import grpc_client.grpc_client.produk_pb2_grpc as products_pb2_grpc
# import produk_client.grpc_client.produk_pb2 as products_pb2
import grpc_client.grpc.product_pb2_grpc as products_pb2_grpc
import grpc_client.grpc.product_pb2 as products_pb2


class GrpcClient:
    def __init__(self):
        self.host = "localhost"
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            "{}:{}".format(self.host, self.server_port)
        )

        # bind the client and the server
        self.stub = products_pb2_grpc.ProductServiceStub(self.channel)

    def create_product(self, name, price, description, stock, image):
        response = self.stub.ProductCreate(
            products_pb2.ProductCreateRequest(
                name=name,
                price=price,
                description=description,
                stock=stock,
                image=image,
            )
        )

        return dict(
            name=response.product.name,
            price=response.product.price,
            description=response.product.description,
            stock=response.product.stock,
            image=response.product.image,
        )

    def get_products(self):
        response = self.stub.ProductList(products_pb2.ProductListRequest())

        if response is None:
            return None

        return [
            dict(
                id=product.id,
                name=product.name,
                price=product.price,
                description=product.description,
                stock=product.stock,
                image=product.image,
            )
            for product in response.products
        ]

    def get_product(self, id):
        response = self.stub.ProductDetail(
            products_pb2.ProductDetailRequest(id=int(id))
        )

        if response.product.id == 0:
            return None

        return dict(
            id=response.product.id,
            name=response.product.name,
            price=response.product.price,
            description=response.product.description,
            stock=response.product.stock,
            image=response.product.image,
        )

    def update_product(self, id, name, price, description, stock, image):
        response = self.stub.ProductUpdate(
            products_pb2.ProductUpdateRequest(
                id=int(id),
                name=name,
                price=price,
                description=description,
                stock=stock,
                image=image,
            )
        )

        return dict(
            id=response.product.id,
            name=response.product.name,
            price=response.product.price,
            description=response.product.description,
            stock=response.product.stock,
            image=response.product.image,
        )

    def delete_product(self, id):
        response = self.stub.ProductDelete(
            products_pb2.ProductDeleteRequest(id=int(id))
        )

        print(response)

        return dict()
