# projectile.py

import pygame


class Projectile:
    def __init__(self, x, y, vel_x, vel_y, image, radius=None):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.image = image
        # Jika radius tidak disediakan, ambil dari lebar gambar (asumsi gambar berbentuk lingkaran atau persegi)
        self.radius = radius if radius is not None else image.get_width() // 2
        self.active = (
            False  # Projectile dimulai dalam keadaan tidak aktif sampai ditembakkan
        )

    def update(self):
        """Memperbarui posisi projectile berdasarkan kecepatan dan gravitasi."""
        # Hanya perbarui jika projectile aktif
        if self.active:
            self.vel_y += 0.5  # Gravitasi
            self.x += self.vel_x
            self.y += self.vel_y

    def draw(self, screen):
        """Menggambar projectile pada layar."""
        # Hanya gambar jika projectile aktif
        if self.active:
            # Gambar gambar di tengah koordinat self.x, self.y
            screen.blit(
                self.image,
                (
                    int(self.x - self.image.get_width() // 2),
                    int(self.y - self.image.get_height() // 2),
                ),
            )

    def deactivate(self):
        """Menonaktifkan projectile dan memindahkannya ke luar layar."""
        self.active = False
        self.x = -100  # Pindahkan ke luar layar
        self.y = -100
        self.vel_x = 0
        self.vel_y = 0
