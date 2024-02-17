import os
import shutil

def kopyala_galeryi(kaynak_dizin, hedef_dizin):
    # Kaynak dizindeki tüm dosyaları listele
    dosyalar = os.listdir(kaynak_dizin)
    
    # Dosyaları hedef dizine kopyala
    for dosya in dosyalar:
        dosya_yolu = os.path.join(kaynak_dizin, dosya)
        if os.path.isfile(dosya_yolu):  # Sadece dosya ise kopyala
            shutil.copy(dosya_yolu, hedef_dizin)

# Kaynak ve hedef dizinleri belirle
kaynak_dizin = "/storage/emulated/0/DCIM"  # Cihazın galeri dizini
hedef_dizin = "./KraWter"  # GitHub deposu

# Kaynak dizindeki dosyaları GitHub deposuna kopyala
kopyala_galeryi(kaynak_dizin, hedef_dizin)

# GitHub deposuna dosyaları eklemek için gerekli adımları yap
os.chdir(hedef_dizin)
os.system("git add .")
os.system("git commit -m 'Added photos from device'")
os.system("git push origin main")
