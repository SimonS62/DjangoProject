import redis
import json
from django.conf import settings


def test_redis_connection():
    try:
        # Подключение к Redis
        r = redis.Redis(host='localhost', port=6379, db=0)

        # Тест записи
        test_key = "test:djangoconnection"
        test_value = {"message": "Redis работает!", "timestamp": str(r.time())}

        r.set(test_key, json.dumps(test_value))

        # Тест чтения
        result = r.get(test_key)
        if result:
            decoded_result = json.loads(result)
            print("✅ Redis подключен успешно!")
            print(f"Данные из Redis: {decoded_result}")
            return True
        else:
            print("❌ Ошибка при чтении из Redis")
            return False

    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        return False

if __name__ == "__main__":
    test_redis_connection()
