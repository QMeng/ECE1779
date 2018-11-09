from app_worker import app_worker

if __name__ == "__main__":
    app_worker.run(host='0.0.0.0', port=8080)