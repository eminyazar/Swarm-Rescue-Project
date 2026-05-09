import pandas as pd
from utils import math_utils
import config

class SimulationLogger:
    def __init__(self):
        self.data = []

    def log_state(self, frame, swarm, environment):
        """Her karede (frame) sürünün metriklerini kaydeder."""
        # Sürünün hedefe olan ortalama uzaklığını hesapla
        total_distance = sum([math_utils.distance(agent.position, environment.target) for agent in swarm.agents])
        avg_distance = total_distance / len(swarm.agents)

        # Veriyi sözlük olarak listeye ekle
        self.data.append({
            "Kare_(Frame)": frame,
            "Zaman_(Saniye)": round(frame / config.FPS, 2),
            "Ortalama_Hedef_Uzakligi": round(avg_distance, 2),
            "Hedef_Bulundu": 1 if environment.target_found else 0
        })

    def save_to_csv(self, filename="swarm_results.csv"):
        """Simülasyon bitince tüm veriyi CSV dosyasına dönüştürür."""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"\n[BAŞARILI] Simülasyon verileri '{filename}' adıyla kaydedildi!")
        print("Bu dosyayı Excel'de açarak sunum grafiklerinizi çizebilirsiniz.")