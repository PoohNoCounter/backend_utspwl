# uts backend

## cara menjalankan

1. clone repository ini `git clone https://github.com/PoohNoCounter/backend_utspwl`
2. masuk ke folder repository `cd backend_utspwl`

## menjalankan server gRPC

1. masuk ke folder server `cd grpc-server`
2. buat virtual environment `python3 -m venv env`
3. aktifkan virtual environment `.\env\Scripts\activate`
4. buat database di mysql dengan nama `uts_pwl_andre`
5. install requirements `.\env\Scripts\pip install -e .`
6. jalankan migrasi database `.\env\Scripts\alembic upgrade head`
7. jalankan server `python -m app.py`

## menjalankan client gRPC

1. masuk ke folder client `cd grpc_client`
2. buat virtual environment `python3 -m venv env`
3. aktifkan virtual environment `.\env\Scripts\activate`
4. install requirements `.\env\Scripts\pip install -e .`
5. jalankan client `.\env\Scripts\pserve development.ini --reload`
