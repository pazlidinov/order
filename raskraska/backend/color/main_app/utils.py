from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# Rasmni yuklab olish va piksel ma'lumotlariga aylantirish
def load_image(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    return np.array(img)


# Ranglarni k-means bilan tahlil qilib, rang palitrasini yaratish
def get_palette(image, num_colors):
    # Rasmdan piksel ma'lumotlarini olish
    pixels = image.reshape(-1, 3)

    # K-means algoritmini ishlatib, ranglarni aniqlash
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)

    # Aniqlangan ranglarni qaytarish
    return kmeans.cluster_centers_.astype(int)


# Rasmni ranglar palitrasiga asoslangan holda qayta chizish
def recolor_image(image, palette):
    pixels = image.reshape(-1, 3)

    # Har bir piksel uchun eng yaqin rangni topish
    new_pixels = np.array(
        [
            palette[np.argmin(np.linalg.norm(palette - pixel, axis=1))]
            for pixel in pixels
        ]
    )

    # Qayta ishlangan rasmdan yangi rasmni yaratish
    return new_pixels.reshape(image.shape)


# Rasmlarni saqlash va ko'rsatish
def save_and_show_image(image, output_path):
    img = Image.fromarray(image.astype("uint8"))
    img.save(output_path)
    plt.imshow(img)
    plt.axis("off")
    plt.show()


# Asosiy funksiya
def main(image_path, num_colors):
    # Rasmni yuklab olish
    image = load_image(image_path)

    # Rang palitrasini yaratish
    palette = get_palette(image, num_colors)

    # Rasmni qayta chizish
    new_image = recolor_image(image, palette)
    return new_image

    # Yangi rasmni saqlash va ko'rsatish
    # save_and_show_image(new_image, output_path)


# Qo'llash: rasmingiz joylashgan manzil va chiqish fayli nomini kiriting
# if __name__ == "__main__":
#     main("input_image.jpg", 10)
