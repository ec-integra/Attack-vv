# EC-INEGRA
![176a12e4-7bcb-4015-8b15-6ab9d2d9bff5](https://user-images.githubusercontent.com/116355531/197199151-55fe450a-90f8-4402-a8f2-218e6ecfc886.jpg)
# Авторы
1. [Басан Елена Сергеевна](https://github.com/lennylenny161), контакты: ebasan@sfedu.ru
2. Басан Александр Сергеевич, контакты: deb@ec-integra.ru
3. [Рязанов Максим Сергеевич](https://github.com/Entarudin), контакты: riazanov@sfedu.ru
## Описание
Attack-vv - это программный модуль верификации векторов атак, который на основе скана программы NetworkScanner выполняет сетевые атаки (syn flood, upd flood, arp spofing, brute force, dchp starvation) с целью анализа защищенности сети.
## Функционал
Модуль представляет собой набор утилит для тестирования безопасности узла сети, в том числе на проверку подверженности атакам данного узла и верификации векторов атак.
### Модуль проверяет узел на подверженность следующим атакам:
* SYN-флуд (SYN flood attack)
* UDP-флуд (UDP flood attack)
* ARP-spoofing
* Атака «грубой силой» (brute force)
* Истощение ресурсов DHCP (DHCP starvation)

### Результат работы Attack-vv будет представлен в файле result.json
## Чтобы запустить проект, нужно в терминале выполнить команды:
- Перейти в рабочую директорию проекта
- Добавить в корень проекта файл data.json
- chmod ugo+x start_main
- sudo ./start_main
