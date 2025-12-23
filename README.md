# Pretty Pixels

Yapay zeka destekli profesyonel yüz düzenleme uygulaması.

![Pretty Pixels](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)

## Özellikler
- **Leke Giderme**: Tıklayarak lekeleri ve kusurları giderin
- **Yüz Yumuşatma**: Yüz detaylarını koruyarak yapay zeka destekli cilt yumuşatma
- **Makyaj Uygulama**:
  - 8 farklı renk seçeneğiyle ruj (Kırmızı, Pembe, Mercan, Berry, Nude, Şarap, Turuncu, Mor)
  - 6 farklı renk seçeneğiyle allık (Pembe, Şeftali, Mercan, Gül, Mor, Berry)
- **Göz ve Kaş Keskinleştirme**: Gözler ve kaşları netleştirerek belirginleştirin
- **Anlık Önizleme**: Önce/Sonra karşılaştırma görünümü
- **Geri Dönüşümlü Düzenleme**: Orijinal fotoğrafı her zaman korur


### Gereksinimler
- Python 3.8 veya üzeri
- pip paket yöneticisi

### Kurulum Adımları

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullaniciadi/PrettyPixels.git
cd PrettyPixels
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

Uygulamayı çalıştırın:
```bash
python main.py
```

### Nasıl Kullanılır:

1. **Fotoğraf Yükle**: "Load Image" butonuna tıklayın ve bir fotoğraf seçin
2. **Efekt Uygula**: Kaydırıcıları kullanarak efekt yoğunluğunu ayarlayın (0-100)
   - Smoothing: Cilt dokusunu yumuşatır
   - Lipstick: Renk seçin ve yoğunluğu ayarlayın
   - Blush: Renk seçin ve yoğunluğu ayarlayın
   - Sharpening: Göz ve kaş netliğini artırır
3. **Leke Giderme**: "Remove Blemish" fotoğraftaki lekelere tıklayın
4. **Kaydet**: "Save Image" butonuna tıklayarak düzenlenmiş fotoğrafı dışa aktarın
5. **Sıfırla**: "Reset" butonuyla orijinal fotoğrafa geri dönün

### Kullanılan Teknolojiler
- **OpenCV**: Görüntü işleme ve bilgisayarlı görü
- **MediaPipe**: Yüz ağı tespiti (468 yüz işaret noktası)
- **NumPy**: Sayısal işlemler
- **Tkinter**: Arayüz çerçevesi
- **PIL/Pillow**: Görüntü işleme


### Temel Özellik Uygulamaları
- **Yüz Tespiti**: MediaPipe Face Mesh ile 468 işaret noktası
- **Maske Oluşturma**: Hassas yüz bölgesi segmentasyonu
- **Bilateral Filtreleme**: Kenar koruyucu yumuşatma
- **Inpainting (TELEA)**: Leke giderme algoritması
- **Unsharp Masking**: Keskinleştirme tekniği
- **Overlay Blending**: Doğal makyaj uygulama

## Gerekli Paketler

```
opencv-python==4.8.1.78
mediapipe==0.10.8
numpy==1.24.3
Pillow==10.1.0
```



