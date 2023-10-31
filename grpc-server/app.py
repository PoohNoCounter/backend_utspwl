from concurrent import futures
import time
import logging
import grpc

from config.config import engine
from sqlalchemy import insert, text, values, select, update, delete, desc


from models.product import Product

import product_pb2
import product_pb2_grpc


class ProductServicer(product_pb2_grpc.ProductServiceServicer):
    def ProductCreate(self, request, context):
        with engine.connect() as conn:
            query = insert(Product).values(
                name=request.name,
                price=request.price,
                description=request.description,
                stock=request.stock,
                image=request.image,
            )
            conn.execute(query)

            conn.commit()

            return product_pb2.ProductCreateResponse(
                product=product_pb2.Product(
                    name=request.name,
                    price=request.price,
                    description=request.description,
                    stock=request.stock,
                    image=request.image,
                )
            )

    def ProductList(self, request, context):
        with engine.connect() as conn:
            res = conn.execute(select(Product).order_by(desc(Product.id))).all()

            conn.commit()

            products = []
            for row in res:
                products.append(
                    product_pb2.Product(
                        id=row[0],
                        name=row[1],
                        price=row[2],
                        description=row[3],
                        stock=row[4],
                        image=row[5],
                    )
                )
            return product_pb2.ProductListResponse(products=products)

    def ProductDetail(self, request, context):
        with engine.connect() as conn:
            query = select(Product).where(Product.id == request.id)
            result = conn.execute(query).first()

            conn.commit()
            if result is None:
                return product_pb2.ProductDetailResponse()

            product = product_pb2.Product(
                id=result[0],
                name=result[1],
                price=result[2],
                description=result[3],
                stock=result[4],
                image=result[5],
            )

            return product_pb2.ProductDetailResponse(product=product)

    def ProductUpdate(self, request, context):
        with engine.connect() as conn:
            query = (
                update(Product)
                .where(Product.id == request.id)
                .values(
                    name=request.name,
                    price=request.price,
                    description=request.description,
                    stock=request.stock,
                    image=request.image,
                )
            )
            conn.execute(query)

            conn.commit()

            return product_pb2.ProductUpdateResponse(
                product=product_pb2.Product(
                    id=request.id,
                    name=request.name,
                    price=request.price,
                    description=request.description,
                    stock=request.stock,
                    image=request.image,
                )
            )

    def ProductDelete(self, request, context):
        with engine.connect() as conn:
            query = delete(Product).where(Product.id == request.id)
            conn.execute(query)
            conn.commit()
            return product_pb2.ProductDeleteResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started at port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    logging.basicConfig()
    serve()
