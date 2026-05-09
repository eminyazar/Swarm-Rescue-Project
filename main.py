# main.py
import cv2
import numpy as np
import config
from core.swarm import Swarm
from core.environment import Environment
from utils import math_utils
from utils.logger import SimulationLogger

def main():
    print("Sürü Simülasyonu Başlatılıyor...")
    print("Çıkmak için ekrandayken 'q' tuşuna basın.")
    
    # Sürüyü ve Haritayı Başlat
    swarm = Swarm()
    env = Environment()
    logger = SimulationLogger()
    
    window_name = "Swarm Rescue - Kolektif Arama Kurtarma Simulasyonu"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, config.WIDTH, config.HEIGHT)

    frame_count = 0

    while True:
        frame = np.zeros((config.HEIGHT, config.WIDTH, 3), dtype=np.uint8)
        frame[:] = config.COLOR_BG
        
        # 1. Çevreyi Çiz (Duvarlar ve Hedef)
        env.draw(frame)
        
        # 2. Sürüyü çalıştır (Haritayı parametre olarak gönderiyoruz)
        swarm.run(env)
        
        # 3. Robotları Çiz
        for agent in swarm.agents:
            center = (int(agent.position[0]), int(agent.position[1]))
            
            if np.linalg.norm(agent.velocity) > 0:
                dir_vec = (agent.velocity / np.linalg.norm(agent.velocity)) * (config.AGENT_RADIUS * 3)
                tip = (int(agent.position[0] + dir_vec[0]), int(agent.position[1] + dir_vec[1]))
                cv2.line(frame, center, tip, (255, 255, 255), 1) 
            
            # Eğer hedef bulunduysa ve robot hedefe yaklaştıysa sinyal ışığı yak (mavi)
            if env.target_found and math_utils.distance(agent.position, env.target) < 60:
                cv2.circle(frame, center, config.AGENT_RADIUS, (255, 200, 0), -1) # Mavi
            else:
                cv2.circle(frame, center, config.AGENT_RADIUS, config.COLOR_AGENT, -1) # Turuncu

        if env.target_found:
            # Hedef bulunduysa yeşil renkli koordinat yazısı
            text = f"HEDEF BULUNDU! Konum: X: {int(env.target[0])}, Y: {int(env.target[1])}"
            cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            # Hedef henüz bulunmadıysa beyaz renkli arama yazısı
            text = "Sistem: Arama-Kurtarma Devam Ediyor..."
            cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow(window_name, frame)

        logger.log_state(frame_count, swarm, env)
        frame_count += 1

        if cv2.waitKey(1000 // config.FPS) & 0xFF == ord('q'):
            print("Simülasyon sonlandırıldı.")
            break
            
    cv2.destroyAllWindows()

    logger.save_to_csv()

if __name__ == "__main__":
    main()