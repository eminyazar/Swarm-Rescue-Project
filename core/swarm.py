# core/swarm.py
import numpy as np
import config
from utils import math_utils
from core.agent import Agent

class Swarm:
    def __init__(self):
        """
        Sistem başladığında config dosyasındaki sayı kadar robotu 
        ekranın rastgele yerlerinde oluşturur ve bir listeye ekler.
        """
        self.agents = [
            Agent(np.random.uniform(0, config.WIDTH), 
                  np.random.uniform(0, config.HEIGHT)) 
            for _ in range(config.NUM_AGENTS)
        ]

    def run(self, environment):
        """
        Ana döngüden (main.py) her karede çağrılacak.
        """
        for agent in self.agents:
            # --- 1. HEDEF KONTROLÜ ---
            # Eğer hedef henüz bulunmadıysa ve bu robot hedefe çok yaklaştıysa sinyal ver!
            if not environment.target_found:
                if math_utils.distance(agent.position, environment.target) < 30:
                    environment.target_found = True
                    print("HEDEF BULUNDU! Sürü oraya yönlendiriliyor...")

            # --- 2. VEKTÖRLERİ HESAPLA ---
            separation_force = self.separate(agent)
            alignment_force = self.align(agent)
            cohesion_force = self.cohere(agent)
            
            # Yeni eklenen çevresel kuvvetler
            obstacle_force = environment.get_obstacle_force(agent)
            target_force = environment.get_target_force(agent)

            # --- 3. KUVVETLERİ UYGULA (Katsayılarla Çarparak) ---
            agent.apply_force(separation_force * config.W_SEPARATION)
            agent.apply_force(alignment_force * config.W_ALIGNMENT)
            agent.apply_force(cohesion_force * config.W_COHESION)
            
            # Engelden kaçınma çok önemlidir, o yüzden ağırlığı yüksek olmalı
            agent.apply_force(obstacle_force * config.W_OBSTACLE)
            agent.apply_force(target_force * config.W_GOAL)

            # İvmeyi hıza, hızı konuma dönüştür
            agent.update()

    def separate(self, agent):
        """
        KURAL 1: AYRILMA (Separation)
        Robotun çok yakınına giren diğer robotlardan uzaklaşmasını sağlar.
        """
        steer = np.array([0.0, 0.0])
        total = 0
        
        for other in self.agents:
            if other is not agent:
                d = math_utils.distance(agent.position, other.position)
                # Sadece belli bir mesafeden yakınsa (Çarpışma tehlikesi)
                if 0 < d < (config.PERCEPTION_RADIUS / 2):
                    # Diğer robottan uzaklaşacak ters vektörü bul
                    diff = agent.position - other.position
                    diff = math_utils.normalize(diff)
                    diff /= d  # Yakınlaştıkça itme kuvveti artar
                    steer += diff
                    total += 1
                    
        if total > 0:
            steer /= total
            steer = math_utils.normalize(steer) * config.MAX_SPEED
            # İstediğimiz hızdan şu anki hızımızı çıkarıp direksiyon kuvvetini buluyoruz (Reynolds Formülü)
            steer -= agent.velocity
            steer = math_utils.limit(steer, config.MAX_FORCE)
            
        return steer

    def align(self, agent):
        """
        KURAL 2: HİZALANMA (Alignment)
        Robotun, görüş alanındaki diğer robotların ortalama yönüne dönmesini sağlar.
        """
        sum_velocity = np.array([0.0, 0.0])
        total = 0
        
        for other in self.agents:
            if other is not agent:
                d = math_utils.distance(agent.position, other.position)
                if 0 < d < config.PERCEPTION_RADIUS:
                    sum_velocity += other.velocity
                    total += 1
                    
        if total > 0:
            sum_velocity /= total
            sum_velocity = math_utils.normalize(sum_velocity) * config.MAX_SPEED
            steer = sum_velocity - agent.velocity
            steer = math_utils.limit(steer, config.MAX_FORCE)
            return steer
            
        return np.array([0.0, 0.0])

    def cohere(self, agent):
        """
        KURAL 3: BİRLEŞME (Cohesion)
        Robotun, görüş alanındaki diğer robotların "ağırlık merkezine" gitmesini sağlar.
        """
        sum_position = np.array([0.0, 0.0])
        total = 0
        
        for other in self.agents:
            if other is not agent:
                d = math_utils.distance(agent.position, other.position)
                if 0 < d < config.PERCEPTION_RADIUS:
                    sum_position += other.position
                    total += 1
                    
        if total > 0:
            # Merkeze doğru olan vektörü hesapla (Hedef - Mevcut Konum)
            center = sum_position / total
            desired = center - agent.position
            desired = math_utils.normalize(desired) * config.MAX_SPEED
            steer = desired - agent.velocity
            steer = math_utils.limit(steer, config.MAX_FORCE)
            return steer
            
        return np.array([0.0, 0.0])