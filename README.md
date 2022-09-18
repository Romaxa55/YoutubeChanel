# Это проект автоматизирует работать с YouTube каналом.

### По функционалу
- Работает по Yourube Api v3
- Создает из одного более 100 видео на разных языках и накладывать на него эффекты, текст, субтитры, водяные знаки и анимации... (MoveiPy library)
- Создавать субтитры для ютуба более чем на 100 языках (Google Translate api + Youtube api)
- Загружать видео на канал по api + генерация привью для обложки так же с надписями на разных языках

Какие методы испльзую я:
После того, когда у меня есть оригинальный видtо клип^ готовый для выгрузки на YouTube

Метод Translate
```python
t = Translate(Lang_file, Video_file)
t.translateSub(subs)
```
Делаю заготовку суптитров для видео и перевожу на языки по списку

Метод Converter
```python
c = Converter()
c.createVideo()
```
В многопоточном режиме multiprocessing.Pool вызываю метод RenderVideo и генерирую на других яыках видео, уже с субтитрами, с водяными знаками и привьшкаи, все захардкожено в класе Converter

Метод Youtube
```python
y = Youtube()
print(y.GetVideoInfo('tlikR8wiunA'))
```
Нужен чисто для получения постоянного токена

Последний метод UpdateVideoInfo
```python
videoIDs = settings.config['VideoId']
y.UpdateVideoInfo(videoIDs)
```
Из за ограничений по квотам до 6 видео в сутки по api, принятл решение в ручном режиме выгружать по 15 видео за раз, затем для каждого загруженого видео в config.yaml введу табличку, где язык = id загруженного видео
```yaml
VideoId:
        - am: EbOEKBKtMqU
        - de: l7Gwja3Zj3U
        - en: 49yenQtddyQ
        - af: QKe-RHRc8qA
```
После чего через UpdateVideoInfo(dict(videoIDs)) обновляю заголовки. описание, загружаю привью обложку, выставляю статусы публичный и многое другое....

