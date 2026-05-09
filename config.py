# --- EKRAN VE SİMÜLASYON AYARLARI ---
WIDTH, HEIGHT = 800, 600  # Simülasyon pencere boyutu
FPS = 30                  # Saniyedeki kare sayısı

# --- SÜRÜ (AGENT) AYARLARI ---
NUM_AGENTS = 30           # Simülasyondaki toplam robot sayısı
AGENT_RADIUS = 4          # Robotların ekrandaki çizim boyutu
MAX_SPEED = 4.0           # Robotun çıkabileceği maksimum hız
MAX_FORCE = 0.1           # Direksiyon/Dönüş kuvveti (Büyük olursa çok keskin dönerler)

# --- SENSÖR VE ALGI MENZİLLERİ ---
PERCEPTION_RADIUS = 50.0  # Robotun diğer robotları gördüğü yarıçap (Lokal İletişim)
OBSTACLE_RADIUS = 30.0    # Duvarları/engelleri algılama mesafesi

# --- BOIDS KATSAYILARI (AĞIRLIKLAR) ---
# Bu değerlerle oynayarak sürünün karakterini değiştireceğiz
W_SEPARATION = 1.5        # Çarpışmayı önleme (Ayrılma)
W_ALIGNMENT = 1.0         # Komşularla aynı yöne gitme (Hizalanma)
W_COHESION = 1.0          # Sürü merkezinde kalma (Birleşme)

# Ekstra Kurallar
W_OBSTACLE = 3.0          # Engelden kaçınma (En yüksek öncelik olmalı ki duvara çarpmasınlar)
W_GOAL = 2.0              # Hedef bulunduğunda hedefe duyulan çekim gücü

# --- RENKLER (OpenCV BGR Formatı Kullanır, RGB değil!) ---
COLOR_BG = (40, 40, 40)         # Koyu gri arka plan (Enkaz ortamı)
COLOR_AGENT = (0, 165, 255)     # Turuncu (Kurtarma robotları)
COLOR_TARGET = (0, 0, 255)      # Kırmızı (Bulunacak hedef)
COLOR_OBSTACLE = (150, 150, 150)# Açık gri (Duvarlar/Engeller)