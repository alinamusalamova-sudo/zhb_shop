import models
import database


def initialize_database():
    database.init_db()
    print("Таблицы созданы успешно")
    admin_exists = models.get_user("admin")
    if not admin_exists:
        admin_id = models.create_user("admin", "admin@zhb.ru", "admin123")
        print(f"Создан администратор: логин 'admin', пароль 'admin123'")
    products = models.get_all_products()
    if len(products) == 0:
        sample_products = [
            {
                "name": "Кольцо ЖБИ КС-10-9",
                "description": "Кольцо стеновое для колодца, диаметр 1м, высота 0.9м",
                "price": 3500.00,
                "image_url": "https://avatars.mds.yandex.net/get-goods_pic/12716636/hataed344493897969a812d1586cb11a295/orig"
            },
            {
                "name": "Плита перекрытия ПК-60-15",
                "description": "Пустотная плита перекрытия, длина 6м",
                "price": 12500.00,
                "image_url": "https://avatars.mds.yandex.net/i?id=f81d21f5c013c0ffe8996b4366d70d27_l-5192508-images-thumbs&n=13"
            },
            {
                "name": "Блок ФБС 24-6-6",
                "description": "Фундаментный блок стеновой 2400x600x600мм",
                "price": 2800.00,
                "image_url": "https://st25.stpulscen.ru/images/product/584/274/418_original.jpg"
            },
            {
                "name": "Лоток теплотрассы ЛТ-10",
                "description": "Лоток для прокладки теплотрасс",
                "price": 4200.00,
                "image_url": "https://www.rusgbi.ru/uploads/goods/65dc6ef115ff4.png"
            },
            {
                "name": "Кольцо с дном КЦД-10",
                "description": "Кольцо с днищем для канализационных колодцев",
                "price": 5800.00,
                "image_url": "https://tosno.vimos.ru/u/shop/265/orig/26578934_4a499f13acfcc2917932f61254020258595733ddc7381b8f78d0acc58f909776.jpg"
            }
        ]

        user = models.get_user("admin")
        if user:
            for product in sample_products:
                product_id = models.add_product(
                    name=product["name"],
                    description=product["description"],
                    price=product["price"],
                    user_id=user['id'],
                    image_url=product["image_url"])
                print(f"  Добавлен товар: {product['name']}")

        categories = [
            ("Кольца колодцев", "Кольца для канализационных, водопроводных колодцев"),
            ("Плиты перекрытий", "Пустотные плиты перекрытия"),
            ("Фундаментные блоки", "Блоки ФБС для фундаментов"),
            ("Лотки теплотрасс", "Лотки для прокладки коммуникаций"),
        ]
        from database import get_db
        conn = get_db()
        cursor = conn.cursor()

        for cat_name, cat_desc in categories:
            cursor.execute(
                "INSERT INTO categories (name, description) "
                "VALUES (%s, %s)",
                (cat_name, cat_desc)
            )
            print(f"  Добавлена категория: {cat_name}")
        conn.commit()
        cursor.close()
        conn.close()
    print("\Статистика")
    print(f"Пользователей в системе: {models.get_all_users_count()}")
    print(f"Товаров в каталоге: {len(models.get_all_products())}")
    print("\nИнициализация завершена")
    print("\nДанные для входа:")
    print("  Логин: admin")
    print("  Пароль: admin123")
    print("  Email: admin@zhb.ru")

if __name__ == "__main__":
    initialize_database()