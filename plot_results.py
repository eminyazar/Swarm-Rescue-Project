# plot_results.py
import pandas as pd
import matplotlib.pyplot as plt

def create_convergence_graph():
    # 1. Kaydettiğimiz veriyi oku
    try:
        df = pd.read_csv("swarm_results.csv")
    except FileNotFoundError:
        print("Hata: 'swarm_results.csv' dosyası bulunamadı. Önce main.py'yi çalıştırın.")
        return

    # 2. Grafik tuvalini oluştur (Canva slaytlarına tam oturacak boyutlarda)
    plt.figure(figsize=(10, 6))

    # 3. Ana çizgiyi çiz (Zaman vs Uzaklık)
    plt.plot(df["Zaman_(Saniye)"], df["Ortalama_Hedef_Uzakligi"], 
             label="Sürünün Ortalama Uzaklığı", color="#ff7f0e", linewidth=2.5)

    # 4. Hedefin ilk bulunduğu anı tespit et ve grafikte işaretle
    hedef_bulunan_anlar = df[df["Hedef_Bulundu"] == 1]["Zaman_(Saniye)"]
    
    if not hedef_bulunan_anlar.empty:
        ilk_bulunma = hedef_bulunan_anlar.iloc[0]
        # O ana kırmızı kesik bir çizgi çek
        plt.axvline(x=ilk_bulunma, color="#d62728", linestyle="--", 
                    label=f"Hedef Tespit Edildi ({ilk_bulunma} sn)")

    # 5. Başlık, Eksenler ve Izgara Ayarları (Akademik Görünüm)
    plt.title("Sürü Robotiği: Kolektif Yakınsama (Convergence) Analizi", fontsize=14, fontweight='bold')
    plt.xlabel("Simülasyon Zamanı (Saniye)", fontsize=12)
    plt.ylabel("Hedefe Olan Ortalama Uzaklık (Piksel)", fontsize=12)
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend(fontsize=11)

    # 6. Yüksek çözünürlüklü (300 dpi) olarak kaydet
    plt.savefig("convergence_graph.png", dpi=300, bbox_inches='tight')
    print("\n[BAŞARILI] Grafik yüksek çözünürlüklü olarak 'convergence_graph.png' adıyla kaydedildi!")
    
    # Ekranda da göster
    plt.show()

if __name__ == "__main__":
    create_convergence_graph()