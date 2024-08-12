import json
import os

# Kullanıcı sınıfı: Kullanıcı bilgilerini (username, password, email) tutmak için kullanılan sınıf.
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

# Kullanıcı deposu sınıfı: Kullanıcıların yönetimi, kaydedilmesi, giriş/çıkış işlemleri gibi işlevleri barındırır.
class UserRepository:
    def __init__(self):
        self.users = []  # Kullanıcıları tutan liste
        self.isLoggedIn = False  # Kullanıcının giriş yapıp yapmadığını kontrol eden bayrak
        self.currentUser = {}  # Giriş yapmış kullanıcının bilgilerini tutar

        # .json dosyasından kullanıcıları yükle
        self.loadUser()

    # .json dosyasından kullanıcıları yükleme işlemini gerçekleştirir.
    def loadUser(self):
        if os.path.exists('users.json'):  # Dosya varsa yükleme işlemi yapılır
            with open("users.json", "r") as file:
                users = json.load(file)
                for user in users:
                    # Her kullanıcıyı User sınıfına dönüştür ve users listesine ekle
                    newUser = User(username=user["username"], password=user["password"], email=user["email"])
                    self.users.append(newUser)
            print(self.users)

    # Yeni bir kullanıcı kaydetme işlemi yapılır.
    def register(self, user: User):
        self.users.append(user)  # Kullanıcıyı listeye ekle
        self.saveToFile()  # Kullanıcıyı .json dosyasına kaydet
        print("Kullanıcı oluşturuldu.")

    # Kullanıcının giriş yapma işlemi gerçekleştirilir.
    def login(self, username, password):
        for user in self.users:  # Tüm kullanıcıları kontrol et
            if user.username == username and user.password == password:  # Kullanıcı adı ve şifre eşleşirse
                self.isLoggedIn = True  # Kullanıcının giriş yapmış olduğunu belirle
                self.currentUser = user  # Giriş yapmış kullanıcıyı güncelle
                print("Giriş yapıldı.")
                break

    # Kullanıcının çıkış yapma işlemi gerçekleştirilir.
    def logout(self):
        self.isLoggedIn = False  # Giriş durumunu sıfırla
        self.currentUser = {}  # Giriş yapmış kullanıcıyı temizle
        print("Çıkış yapıldı.")

    # Giriş yapan kullanıcının kimliğini gösterir.
    def identity(self):
        if self.isLoggedIn:
            print(f"Kullanıcı Adı: {self.currentUser.username}")
        else:
            print("Giriş yapılmadı.")

    # Kullanıcı bilgilerini bir .json dosyasına kaydeder.
    def saveToFile(self):
        list_of_users = []

        for user in self.users:
            list_of_users.append(user.__dict__)  # Kullanıcı bilgilerini dictionary formatına çevir ve listeye ekle
        with open("users.json", "w") as file:
            json.dump(list_of_users, file)  # Listeyi .json dosyasına yaz

# Kullanıcı deposu nesnesi oluşturulur.
repository = UserRepository()

# Kullanıcı ile etkileşimli menü döngüsü başlatılır.
while True:
    print("Menü".center(50, "*"))
    secim = input("1- Register\n2- Login\n3- Logout\n4- Identity\n5- Exit\nSeçiminiz: ")

    if secim == "5":
        break  # Programdan çıkış yapılır
    else:
        if secim == "1":
            # Kullanıcıdan bilgilerini al ve yeni bir kullanıcı oluştur
            username = input("Kullanıcı Adı: ")
            password = input("Şifre: ")
            email = input("Email: ")
            
            user = User(username=username, password=password, email=email)
            repository.register(user)  # Kullanıcıyı kaydet

            print(repository.users)  # Mevcut kullanıcıları yazdır

        elif secim == "2":
            # Eğer zaten giriş yapılmışsa
            if repository.isLoggedIn:
                print("Zaten giriş yapılmış durumda.")
            else:
                # Kullanıcıdan giriş bilgileri alınır
                username = input('Kullanıcı Adı: ')
                password = input('Şifre: ')
            
                repository.login(username, password)  # Giriş işlemi yapılır
                print("Başarılı giriş yapıldı.")

        elif secim == "3":
            repository.logout()  # Çıkış işlemi yapılır

        elif secim == "4":
            repository.identity()  # Giriş yapan kullanıcının kimliği gösterilir
            
        else:
            print("Yanlış seçim.")
