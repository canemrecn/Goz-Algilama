import cv2
#OpenCV kütüphaneSİNİ içe aktarılır.
yuzCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
gozCascade = cv2.CascadeClassifier('Cascades/haarcascade_eye.xml')
#Yüz ve göz tespiti için kullanılacak olan sınıflandırıcılar yükleniyor.
kamera = cv2.VideoCapture(0)
kamera.set(3, 1280)
kamera.set(4, 720)
#Kameraya erişim sağlanıyor ve kamera ayarları yapılıyor. 3. parametre (3)
# kameranın genişliğini, 4. parametre (4) ise yüksekliğini belirler.
dosyaad = None
kaydedici = None
#Video kaydetme için dosya adı ve kaydedici değişkenleri başlangıçta atanıyor.
while True:
    ret, kare = kamera.read()
    if not ret:
        break
#Sürekli bir döngü ile kameradan görüntü okunuyor.
# Eğer okuma başarılı değilse döngüden çıkılıyor.
    gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
    yuzler = yuzCascade.detectMultiScale(
        gri,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
#Okunan karenin gri tonlamaya dönüştürülmesi ve yüz tespiti yapılması. detectMultiScale
# fonksiyonu, yüzleri bulmak için Cascade sınıflandırıcısını kullanır.
    for (x, y, w, h) in yuzler:
        cv2.rectangle(kare, (x, y), (x+w, y+h), (255, 0, 0), 2)
        gri_kutu = gri[y:y+h, x:x+w]
        renkli_kutu = kare[y:y+h, x:x+w]
        gozler = gozCascade.detectMultiScale(
            gri_kutu,
            scaleFactor=1.5,
            minNeighbors=10,
            minSize=(3, 3)
        )
        for (ex, ey, ew, eh) in gozler:
            cv2.rectangle(renkli_kutu, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
#Yüzlerin etrafına dikdörtgen çiziliyor ve gözler tespit ediliyor. Yüz bölgesi, gri tonlamalı ve
# renkli kare üzerinde belirli bir konumda bulunur.
    cv2.imshow('kare', kare)
#Sonuç karesinin görüntülenmesi.
    if kaydedici is None and dosyaad is not None:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp.4
        kaydedici = cv2.VideoWriter(dosyaad, fourcc, 24.0, (kare.shape[1], kare.shape[0]), True)
#Eğer kaydedici henüz tanımlanmamışsa ve dosya adı belirtilmişse, bir video kaydedici oluşturulur.
# fourcc değişkeni, video codec'ini belirler. kare.shape[1] ve kare.shape[0] karenin genişliği ve
# yüksekliğini temsil eder.
    if kaydedici is not None:
        kaydedici.write(kare)
#Kaydedici tanımlanmışsa, mevcut kareyi kaydeder.
    k = cv2.waitKey(10) & 0xff
    if k == 27 or k == ord('q'):  # press 'ESC' or 'q' to quit
        break
#Klavyeden tuş girişlerini kontrol eder. Eğer ESC veya q tuşuna basılırsa döngüden çıkılır.
kamera.release()
#Kamera kaynağının serbest bırakılması.
if kaydedici:
    kaydedici.release()
#Kaydedici varsa serbest bırakılır.
cv2.destroyAllWindows()
#Tüm açık pencerelerin kapatılması ve kaynakların serbest bırakılması.
