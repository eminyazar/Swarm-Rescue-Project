# core/environment.py
import numpy as np
import cv2
import config
from utils import math_utils

class Environment:
    def __init__(self):
        # Labirent duvarları: (x, y, genişlik, yükseklik)
        self.obstacles = [
            (100, 100, 30, 400),  # Sol uzun duvar
            (300, 0, 30, 300),    # Üstten inen duvar
            (300, 450, 400, 30),  # Alttan sağa giden duvar
            (550, 150, 30, 180)   # Ortadaki küçük engel
        ]
        
        # Arama kurtarma hedefi (Kazazede konumu)
        self.target = self._generate_valid_target() 
        self.target_radius = 15
        self.target_found = False # Sürüden biri hedefi buldu mu?

    def _generate_valid_target(self):
        """
        Hedefi rastgele oluşturur, ancak bir duvarın içine düşmediğinden emin olur.
        Eğer duvara denk gelirse, boş bir yer bulana kadar tekrar dener.
        """
        while True:
            # Ekranın kenarlarından 50 piksel içeride rastgele bir nokta seç
            tx = np.random.uniform(50, config.WIDTH - 50)
            ty = np.random.uniform(50, config.HEIGHT - 50)
            
            inside_wall = False
            for (x, y, w, h) in self.obstacles:
                # Hedefin duvara çok yakın (veya içinde) olup olmadığını kontrol et
                # 20 piksellik bir güvenlik payı bırakıyoruz
                if (x - 20) < tx < (x + w + 20) and (y - 20) < ty < (y + h + 20):
                    inside_wall = True
                    break
                    
            if not inside_wall:
                return np.array([tx, ty])

    def draw(self, frame):
        """Çevreyi (Duvarlar ve Hedef) ekrana çizer."""
        # Engelleri çiz
        for (x, y, w, h) in self.obstacles:
            cv2.rectangle(frame, (x, y), (x+w, y+h), config.COLOR_OBSTACLE, -1)
            
        # Hedefi çiz (Bulunmadıysa kırmızı, bulunduysa yeşil)
        color = (0, 255, 0) if self.target_found else config.COLOR_TARGET
        cv2.circle(frame, (int(self.target[0]), int(self.target[1])), self.target_radius, color, -1)

    def get_obstacle_force(self, agent):
        """
        GELİŞMİŞ ENGELDEN KAÇINMA (Anti-Tunneling)
        Duvara yaklaştıkça itme kuvveti eksponansiyel olarak artar.
        """
        steer = np.array([0.0, 0.0])
        count = 0
        
        for (x, y, w, h) in self.obstacles:
            closest_x = max(x, min(agent.position[0], x + w))
            closest_y = max(y, min(agent.position[1], y + h))
            closest_point = np.array([closest_x, closest_y])

            d = math_utils.distance(agent.position, closest_point)
            
            # 1. PANİK DURUMU: Robot duvarın içine girdiyse (d == 0)
            if d == 0:
                # Duvarın merkezini bul ve robotu merkezden ters yöne şiddetle dışarı fırlat
                center_x, center_y = x + w/2, y + h/2
                escape_vec = agent.position - np.array([center_x, center_y])
                escape_vec = math_utils.normalize(escape_vec)
                # Maksimum hızın çok üstünde anlık bir şok kuvveti uygula
                return escape_vec * config.MAX_SPEED * 5.0 
                
            # 2. NORMAL KAÇINMA DURUMU: Duvara yaklaşıyorsa
            if 0 < d < config.OBSTACLE_RADIUS:
                diff = agent.position - closest_point
                diff = math_utils.normalize(diff)
                
                # KRİTİK NOKTA: Duvara ne kadar yakınsa, kuvvet o kadar katlanır (Ters Kare Kanunu benzeri)
                # Mesafe azaldıkça çarpan büyür.
                diff *= (config.OBSTACLE_RADIUS / d) 
                
                steer += diff
                count += 1
                
        if count > 0:
            steer /= count
            steer = math_utils.normalize(steer) * config.MAX_SPEED
            steer -= agent.velocity
            
            # LİMİTİ YÜKSELTTİK: Duvarın itme gücü, diğer tüm kuvvetlerin toplamından (hedef, sürü) daha güçlü olmalı
            steer = math_utils.limit(steer, config.MAX_FORCE * 4.0) 
            
        return steer

    def get_target_force(self, agent):
        """
        Hedef bulunduğunda tüm sürüyü o noktaya çeken çekim kuvveti.
        """
        if self.target_found:
            desired = self.target - agent.position
            d = math_utils.distance(agent.position, self.target)
            
            # Hedefe ulaştıysa yavaşla ve etrafında dur (Arrival behavior)
            if d < 40:
                m = np.interp(d, [0, 40], [0, config.MAX_SPEED])
                desired = math_utils.normalize(desired) * m
            else:
                desired = math_utils.normalize(desired) * config.MAX_SPEED
                
            steer = desired - agent.velocity
            steer = math_utils.limit(steer, config.MAX_FORCE)
            return steer
            
        return np.array([0.0, 0.0])