# Веб-месенджер з кодуванням повідомлень
Цей проєкт містить веб-застосунок, написаний на Django, в якому реалізований месенджер для обміну даними, в тому числі і медіа з кодуванням за допомогою Rabin Cryptosystem. Веб-застосунок має наступний функціонал:
1. Створення та видалення нових користувачів.
2. При реєстрації в користувача створюється публічний та приватний ключ.
3. Користувачі можуть листуватись один з одним, відправляючи текст або фото.
4. Користувач має доступ до свого публічного ключа.
5. Користувач може передивитись історію своїх листувань.

Для того, щоб користуватись веб-застосунком потрібно виконати наступні дії:
1. Склонувати репозиторій:
  git clone https://github.com/kostyaCS/DiscretteProjectUCU.git

 
 2. Перейти в папку репозиторію:
  cd DiscretteProjectUCU
 
 3. Інсталювати необхідні бібліотеки:
  pip install -r requirements.txt
  
 4. Запустити сервер:
  python manage.py runserver

Після цього потрібно перейти за адресою http://localhost:8000, щоб потрапити на головну сторінку веб-застоснку. Тепер подивимось як це працює!
Зареєструємось, та зайдемо на основну сторінку користувача:

<img width="356" alt="Знімок екрана 2023-05-28 о 11 34 36" src="https://github.com/kostyaCS/DiscretteProjectUCU/assets/116595519/21195b5d-5b5b-489b-ae9b-401610413434">

Можемо побачити, що ми маємо доступ до нашого публічного ключа, він є у відкритому доступі. Тепер спробуємо написати повідомлення нашому другу Денису, який зареєстрований в системі:
Для цього введемо його нік в пошуку:
<img width="1499" alt="Знімок екрана 2023-05-28 о 11 36 00" src="https://github.com/kostyaCS/DiscretteProjectUCU/assets/116595519/0906bba2-9ac3-4fe7-8ad4-5f62e436bdec">

Переходимо на наш з ним чат, та привітаємось:
<img width="1507" alt="Знімок екрана 2023-05-28 о 11 39 06" src="https://github.com/kostyaCS/DiscretteProjectUCU/assets/116595519/124abf98-cf10-4300-88fa-a7f3493103bf">
Тепер подивимось, як зберігається це повідомлення в базі даних:
<img width="829" alt="Знімок екрана 2023-05-28 о 11 40 07" src="https://github.com/kostyaCS/DiscretteProjectUCU/assets/116595519/43d4fe01-4580-4422-bcad-53a3cc006bd1">
Як ми бачимо, в базі даних це повідомлення закодоване публічним ключем Дениса, однак, якщо ми перейдемо на його сторінку - побачимо, що воно відображається коректно, адже після запиту з бази даних автоматично відбувається декодування приватним ключем отримувача:
<img width="1504" alt="Знімок екрана 2023-05-28 о 11 42 07" src="https://github.com/kostyaCS/DiscretteProjectUCU/assets/116595519/d22b6d67-4888-4868-9dd2-1ac691e05990">

## Загалом, нами було реалізовано чотири алгоритми:
### DSA - це алгоритм цифрового підпису (DSA). Алгоритм цифрового підпису (DSA) - це широко використовуваний криптографічний алгоритм з відкритим ключем для створення та перевірки цифрових підписів. Він був розроблений Національним інститутом стандартів і технологій (NIST) в США і опублікований як федеральний стандарт в 1994 році. DSA широко використовується для цифрових підписів у різних сферах, включаючи безпечний зв'язок, електронні транзакції, розповсюдження програмного забезпечення та протоколи автентифікації. Він надає засоби для перевірки автентичності та цілісності цифрових даних. Основна ідея полягає в тому, що ми не шифруємо повідомлення, а додаємо до нього спеціальний "підпис". Таким чином, якщо користувач змінить початкове повідомлення, ми дізнаємося про це за допомогою RSA.
### RSA -  широко використовуваний криптографічний алгоритм, названий на честь його винахідників. RSA широко використовується в різних додатках, включаючи протоколи безпечного зв'язку, такі як SSL/TLS, захищена електронна пошта, цифрові сертифікати, безпечна передача файлів і безпечний віддалений доступ. Ми починаємо з генерації двох ключів - публічного та приватного. Обидва ключі являють собою кортежі, кожен з яких містить prime_product - добуток простих чисел у заданому діапазоні байт. Відкритий ключ є випадковим числом добутку функції фі(Ейлера) на ці два числа, а закритий ключ є оберненим до цього числа за модулем.
### Rabin cryptosystem - це алгоритм шифрування з відкритим ключем, розроблений Майклом Рабіном у 1979 році. Криптосистема Рабіна вважається асиметричною схемою шифрування, тобто вона використовує різні ключі для шифрування і дешифрування. Криптосистема Рабіна використовується в різних додатках, включаючи цифрові підписи, протоколи обміну ключами та безпечні комунікації. Однак вона менш поширена в порівнянні з іншими алгоритмами шифрування, такими як RSA, які також покладаються на складність факторизації. Основна ідея полягає в тому, що ми генеруємо відкритий і закритий ключі. Відкритий ключ - це добуток двох закритих ключів (за замовчуванням 50 байт). Кодування просте - ми просто беремо двійкове представлення ascii кожного символу і додаємо до нашого ключа модуль квадрата цього представлення.
### ElGamal encryption system

Детальніше про всі алгоритми та їх застосування ми описпали у нашому юпітері, який знаходиться в теці проєкту.
