import numpy as np
import config
from utils import math_utils

class Agent:
    def __init__(self, x, y):
        """
        Robotun başlangıç konumu ve rastgele ilk hızı ayarlanır.
        """
        self.position = np.array([x, y], dtype=float)
        
        # Robota başlangıçta rastgele bir yön (0 ile 360 derece arası) veriyoruz
        angle = np.random.uniform(0, 2 * np.pi)
        self.velocity = np.array([np.cos(angle), np.sin(angle)]) * config.MAX_SPEED
        
        # İvme (Acceleration) her frame'de uygulanan kuvvetlere göre değişecek
        self.acceleration = np.array([0.0, 0.0])

    def apply_force(self, force):
        """
        Boids kurallarından veya engellerden gelen vektörel kuvvetleri robota uygular.
        F = m*a (Kütleyi 1 kabul ediyoruz, o yüzden Kuvvet = İvme)
        """
        self.acceleration += force

    def update(self):
        """
        Her karede (frame) robotun yeni konumunu hesaplar.
        """
        # 1. Hızı ivme ile güncelle
        self.velocity += self.acceleration
        
        # 2. Hız sınırını aşmasını engelle (Çok hızlı uçup gitmemeleri için)
        self.velocity = math_utils.limit(self.velocity, config.MAX_SPEED)
        
        # 3. Yeni konumu belirle
        self.position += self.velocity
        
        # 4. İvmeyi sıfırla (Çünkü kuvvetler her tick'te yeniden hesaplanacak)
        self.acceleration = np.array([0.0, 0.0])
        
        # Ekran sınırlarından çıkmamaları için basit bir kontrol
        self._check_edges()

    def _check_edges(self):
        """
        Geçici bir sınır kontrolü: Ekranın bir ucundan çıkan diğerinden girer.
        İlerleyen aşamalarda buraya duvar (engel) tanımlayacağımız için 
        robotlar buralara hiç çarpmadan dönecekler.
        """
        if self.position[0] > config.WIDTH:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = config.WIDTH

        if self.position[1] > config.HEIGHT:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = config.HEIGHT