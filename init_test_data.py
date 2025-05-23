from db.database import global_init, create_session
from models.room_images import RoomImage
from models.rooms import Room

# Указываем путь к базе
global_init("instance/resort.db")

# Получаем сессию
session = create_session()

# Удалим старые данные (необязательно)
session.query(RoomImage).delete()
session.query(Room).delete()
session.commit()

# Создаём комнаты
room1 = Room(
    name="Уютный номер у моря",
    description="Просторный номер с видом на море и балконом.",
    price_per_night=5000,
    capacity=2,
    amenities="Wi-Fi, Кондиционер, Мини-бар",
    room_type="standard"
)
room2 = Room(
    name="Семейный номер",
    description="Идеально подходит для семьи с детьми. 2 спальни.",
    price_per_night=8000,
    capacity=4,
    amenities="Wi-Fi, ТВ, Холодильник",
    room_type="family"
)

session.add_all([room1, room2])
session.commit()

# Картинки
img1 = RoomImage(room_id=room1.id, image_url="/static/images/first.jpg")
img2 = RoomImage(room_id=room2.id, image_url="/static/images/second.jpg")

session.add_all([img1, img2])
session.commit()

print("✅ Тестовые комнаты добавлены.")
