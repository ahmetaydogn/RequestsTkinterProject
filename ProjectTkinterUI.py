import tkinter as tk
from PIL import ImageTk, Image
import requests
import webbrowser
import RequestsOperations

# Root oluşturma ve ortala ayarları
window = tk.Tk()
SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight()
App_Width = 500
App_Height = 400
x = (SCREEN_WIDTH // 2) - (App_Width // 2)
y = (SCREEN_HEIGHT // 2) - (App_Height // 2)
window.geometry(f"{App_Width}x{App_Height}+{x}+{y}")

# Root title ve başlangıçta tam ekran gelmesi için
window.title('Tokat Haberler!')
window.state("zoomed")

# Global değişkenlerim ve Requests modülü ile veri çekme
other = ""
currency_json = RequestsOperations.get_currency_data()
(news_titles, news_links) = RequestsOperations.get_news_header()
weather_time_json = RequestsOperations.get_weather_and_times_data()
news_count = 8


class HeaderFrame:
    # Class değişlenlerim, frame ve label oluştur
    header_background_color = "#89CFF3"
    header_foreground_color = "white"
    style = ('Comic Sans MS', '24', 'bold')

    header_frame = tk.Frame(window, bg=header_background_color)
    header_frame.pack(side=tk.TOP, fill=tk.X)

    tokat_haberler_lbl = tk.Label(header_frame, text="Tokat Haberler")
    tokat_haberler_lbl.config(bg=header_background_color, fg=header_foreground_color, font=style)
    tokat_haberler_lbl.grid(row=0, column=0, padx=35, pady=10, sticky='W')


class SideNewsFrame:
    # global değişkenlere ulaşmak için
    global news_titles
    global news_links
    global news_count

    # Classta kullandığım değişkenler, label değişkenlerim ve frame oluşturma
    side_news_background_color = "#4F4A45"
    side_news_foreground_color = "white"
    style = ('Comic Sans MS', '20', 'bold')
    news_style = ('Comic Sans MS', '12', 'normal')

    side_news_frame = tk.Frame(window, bg=side_news_background_color)
    side_news_frame.pack(side=tk.LEFT, fill=tk.Y)
    haberler_lbl = tk.Label(side_news_frame, text='Son Haberler', font=style,
                            bg=side_news_background_color, fg=side_news_foreground_color, width=15)
    haberler_lbl.pack(padx=0, pady=10)

    # Haber başlıklarını çek ve text değişkenine aktar
    titles = []
    for i in range(news_count):
        news_title = news_titles[i]
        news_link = news_links[i]
        news_label = tk.Text(side_news_frame, wrap=tk.WORD, font=news_style)

        news_label.insert(tk.END, news_title)
        news_label.config(state=tk.DISABLED, bg=side_news_background_color,
                          fg=side_news_foreground_color, height=1, width=30, borderwidth=0)
        news_label.pack(padx=5, pady=10, expand=tk.YES, fill=tk.BOTH)
        titles.append(news_label)

class BottomCurrencyFrame:
    # global değişkenlere ulaşmak için
    global other
    global currency_json
    global weather_time_json

    #  Class değişkenleri, kullanılan label değişkenleri ve frame oluşturma
    my_currency_code = ['try', 'eur', 'gbp', 'jpy', 'kwd', 'cad', 'idr']
    my_currency_list = []
    bottom_background_color = "#61A3BA"
    bottom_foreground_color = "#fff"
    bottom_header_foreground_color = "#CDF5FD"
    style = ('Calibri', '16', 'bold')
    style_header = ('Calibri', '24', 'bold')
    bottom_frame = tk.Frame(window, bg=bottom_background_color)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    currency_frame = tk.Frame(bottom_frame, bg=bottom_background_color)
    currency_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

    currency_lbl = tk.Label(currency_frame, text='Kur Değerleri', font=style_header,
                            bg=bottom_background_color, fg=bottom_header_foreground_color)
    currency_lbl.grid(row=0, column=0, padx=10, pady=10, sticky='W', columnspan=4)

    # kur değerleri ve isimlerini json dosyasından çekme
    counter = 0
    while counter < len(my_currency_code):
        my_currency_list.append(currency_json[my_currency_code[counter]])
        counter += 1
    # çektiğimiz json verisinde USD ve kur gücü olmadığı için yapay şekilde kendim ekledim
    my_currency_list.append(
        {'code': 'USD', 'alphaCode': 'USD', 'numericCode': '1',
         'name': 'ABD Dolar', 'rate': 1, 'date': 'None', 'inverseRate': 1}
    )
    # [x_ülkesinin_rate_değeri] / [tr_nin_rate_değeri] = 'Örnek bir japon yeni 0.19TL olduğunu belirtir.'

    tr_inverseRate = my_currency_list[0]['inverseRate']
    tr_currency_inverseRate = my_currency_list[0]['inverseRate']
    tr_value_list = []
    for currency in my_currency_list:
        tr_value_list.append((float(currency['inverseRate']) / tr_currency_inverseRate))

    # Kur label değişkenlerini oluştur ve doldur
    currency_count = len(my_currency_list) + 1
    currencyCodeCounter = 0
    currencyCodeInverseRateCounter = 0
    for currentRow in range(1, (currency_count // 2) + 1):
    #currency_count çift olmalı, tek olursa patlar burası
        for currentColumn in range(4):
            if currentColumn % 2 == 0:
                indexData = f"{my_currency_list[currencyCodeCounter]['code']} / {my_currency_list[0]['code']}"
                currency_label = tk.Label(currency_frame, text=indexData, font=style, width=8)
                currency_label.config(bg=bottom_background_color, foreground=bottom_foreground_color)
                currency_label.grid(row=currentRow, column=currentColumn, padx=10, pady=10, sticky='E')
                currencyCodeCounter += 1
            else:
                current_currency_label = tk.Label(currency_frame,
                                                  text=round(tr_value_list[currencyCodeInverseRateCounter], 3),
                                                  font=style, width=10)
                current_currency_label.config(bg=bottom_background_color, foreground=bottom_foreground_color)
                current_currency_label.grid(row=currentRow, column=currentColumn, padx=(0, 10), pady=10, sticky='W')
                currencyCodeInverseRateCounter += 1

    # gelen ingilizce veriyi değiştir - burası pek olmadı sanırım :)
    def set_weather_status(self):
        if self == "Clear":
            return "Açık Hava"
        elif self == "Partly cloudy":
            return "Parçalı Bulutlu"
        elif self == "Patchy light drizzle":
            return "Yer yer hafif yağışlı"
        elif self == "Patchy light rain":
            return "Yer yer yağışlı"
        elif self == "Patchy rain possible":
            return "Parçalı yağmur mümkün"
        elif self == "Light rain":
            return "Hafif yağmur"
        elif self == "Moderate rain at times":
            return "Hafif ılıman yağmur"
        elif self == "Sunny":
            return "Güneşli"

# ------------------------------------------------------------------------------

    # aside frame oluşturma ve class değişkenlerim
    aside_background_color = "#2980b9"
    aside_foreground_color = "#fff"
    aside_social_media_style = ('Calibri', 16, 'bold')
    aside_about_tokat_style = ('Calibri', 18, 'normal')
    aside_about_tokat_header_style = ('Calibri', 20, 'bold')
    aside_frame = tk.Frame(bottom_frame, bg=aside_background_color)
    aside_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Label oluşturmaları ve grid ile yerleştirme
    about_tokat_label = tk.Label(aside_frame, text='Bugün Tokat')
    about_tokat_label.config(font=aside_about_tokat_header_style, bg=aside_background_color,
                             foreground=aside_foreground_color, width=20)
    about_tokat_label.grid(row=0, column=0, columnspan=2, padx=0, pady=10, sticky='nsew')

    localtime_lbl = tk.Label(aside_frame, text='Saat: ')
    localtime_lbl.config(font=aside_about_tokat_style, bg=aside_background_color,
                         foreground=aside_foreground_color, width=15)
    localtime_lbl.grid(row=1, column=0, padx=0, pady=10, sticky='EW')
    localtime_answer_lbl = tk.Label(aside_frame, text=weather_time_json['location']['localtime'])
    localtime_answer_lbl.config(font=aside_about_tokat_style, bg=aside_background_color,
                                foreground=aside_foreground_color, width=20)
    localtime_answer_lbl.grid(row=1, column=1, padx=0, pady=10, sticky='W')

    weather_temperature_lbl = tk.Label(aside_frame, text='Sıcaklık: ')
    weather_temperature_lbl.config(font=aside_about_tokat_style, bg=aside_background_color,
                                   foreground=aside_foreground_color, width=10)
    weather_temperature_lbl.grid(row=2, column=0, padx=0, pady=10, sticky='EW')
    weather_temperature_answer_lbl = tk.Label(aside_frame, text=f"{weather_time_json['current']['temp_c']} Derece")
    weather_temperature_answer_lbl.config(font=aside_about_tokat_style, bg=aside_background_color,
                                          foreground=aside_foreground_color, width=20)
    weather_temperature_answer_lbl.grid(row=2, column=1, padx=0, pady=10, sticky='W')

    weather_status_lbl = tk.Label(aside_frame, text='Hava Durumu: ')
    weather_status_lbl.config(font=aside_about_tokat_style, bg=aside_background_color,
                              foreground=aside_foreground_color, width=10)
    weather_status_lbl.grid(row=3, column=0, padx=0, pady=10, sticky='EW')
    weather_status_answer_lbl = tk.Label(aside_frame, text=set_weather_status(
                                                            weather_time_json['current']['condition']['text']))
    weather_status_answer_lbl.config(font=aside_about_tokat_style, bg=aside_background_color,
                                     foreground=aside_foreground_color, width=20)
    weather_status_answer_lbl.grid(row=3, column=1, padx=0, pady=10, sticky='W')

    # günlük veri image indirme ve oluşturma
    image_direction = f"https:{weather_time_json['current']['condition']['icon']}"
    image_name = weather_time_json['current']['condition']['text']
    my_image_bytes = requests.get(image_direction).content
    with open(f"{image_name}.png", 'wb') as handler:
        my_image = handler.write(my_image_bytes)
    weather_condition_icon = ImageTk.PhotoImage(Image.open(f"{image_name}.png").resize((30, 30)))
    weather_status_lbl = tk.Label(aside_frame, image=weather_condition_icon)
    weather_status_lbl.config(font=aside_about_tokat_style, bg=aside_background_color,
                              foreground=aside_foreground_color, width=10)
    weather_status_lbl.grid(row=4, column=0, columnspan=2, padx=0, pady=10, sticky='EW')

    # sosyal medya link blokları
    social_media_links = {
        "Facebook": ["https://www.facebook.com/tokathabergazetesi", "#6E84B2"],
        "Twitter": ["https://twitter.com/@tokat_haber", "#45BFEE"],
        "Instagram": ["https://www.instagram.com/tokathabergazetesi", "#7196B4"],
        "YouTube": ["https://www.youtube.com/@kemalozdilek7606", "#F27B81"],
        "Whatsapp": ["https://api.whatsapp.com/send?phone=05300713743", "#25D366"]
    }
    for index, (media_name, other) in enumerate(social_media_links.items()):
        aside_social_media_label = tk.Label(aside_frame, text=media_name, cursor="hand2", textvariable=other[0],
                                            font=aside_social_media_style, bg=aside_background_color,
                                            foreground=aside_foreground_color)
        aside_social_media_label.config(bg=other[1], height=2, width=30, foreground=aside_foreground_color)
        aside_social_media_label.bind("<Button-1>", lambda e :webbrowser.open_new(str(e.widget.cget("textvariable"))))
        aside_social_media_label.grid(row=int(index), column=3, padx=0, pady=0, sticky='E')

class MainContentFrame:
    main_frame_background_color = "#04364A"
    main_frame_foreground_color = "#fff"
    main_frame_header_font = ('Calibri', 24, 'bold')
    main_frame_font = ('Calibri', 16, 'normal')
    main_frame_description_font = ('Calibri', 11, 'normal')
    item_padding = 70

    main_frame = tk.Frame(window, bg=main_frame_background_color)
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # about_me
    my_name = tk.Label(main_frame, text="Ahmet Aydoğan")
    my_name.config(bg=main_frame_background_color, foreground=main_frame_foreground_color, font=main_frame_header_font)
    my_name.grid(row=0, column=0, padx=item_padding, pady=(10, 0))

    image_data = requests.get("https://avatars.githubusercontent.com/u/"
                              "143658136?s=400&u=8aa137cb2ec5f8948f7ea5410f7273c0ec9bd8a3&v=4").content
    image_name = "my_image.jpg"
    with open(image_name, 'wb') as handler:
        handler.write(image_data)
    tk_image_open = ImageTk.PhotoImage(Image.open(image_name).resize((250, 250)))
    tk_image = tk.Label(main_frame, image=tk_image_open)
    tk_image.grid(row=1, column=0, padx=item_padding, pady=5)

    my_description = tk.Label(main_frame, text="Düzce Üniversitesi\nBilgisayar Mühendisliği\n18 Yaşında")
    my_description.config(bg=main_frame_background_color, foreground=main_frame_foreground_color, font=main_frame_font)
    my_description.grid(row=2, column=0, padx=item_padding, pady=(10, 0))

    # emirhan verileri
    emirhan_name = tk.Label(main_frame, text="Emirhan Çalışkan")
    emirhan_name.config(bg=main_frame_background_color, foreground=main_frame_foreground_color,
                        font=main_frame_header_font)
    emirhan_name.grid(row=0, column=2, padx=item_padding, pady=(10, 0))

    emirhan_image_data = requests.get("https://avatars.githubusercontent.com/u/126817623?v=4").content
    emirhan_image_name = "emirhan_image.jpg"
    with open(emirhan_image_name, 'wb') as handler:
        handler.write(emirhan_image_data)
    emirhan_tk_image_open = ImageTk.PhotoImage(Image.open(emirhan_image_name).resize((250, 250)))
    emirhan_tk_image = tk.Label(main_frame, image=emirhan_tk_image_open)
    emirhan_tk_image.grid(row=1, column=2, padx=item_padding, pady=5)

    emirhan_my_description = tk.Label(main_frame, text="Ufuk Üniversitesi\nBilişim Güvenliği Teknolojisi\n18 Yaşında")
    emirhan_my_description.config(bg=main_frame_background_color, foreground=main_frame_foreground_color,
                                  font=main_frame_font)
    emirhan_my_description.grid(row=2, column=2, padx=item_padding, pady=(10, 0))

    # orta content
    debug_name = tk.Label(main_frame, text="Bizim Hakkımızda")
    debug_name.config(width=14, bg=main_frame_background_color, foreground=main_frame_foreground_color,
                      font=main_frame_header_font)
    debug_name.grid(row=0, column=1, padx=item_padding, pady=(10, 0))

    debug_image_data = requests.get("https://scontent.fteq2-1.fna.fbcdn.net/v/t1.6435-1/"
                                    "98999664_1453585458144585_8260683318211641344_n.jpg?"
                                    "stp=dst-jpg_p320x320&_nc_cat=111&ccb=1-7&_nc_sid=2b6aad&"
                                    "_nc_ohc=8gCaSiMtfOIAX8Hgdh9&_nc_ht=scontent.fteq2-1.fna&"
                                    "oh=00_AfCLRane7rTtFZIf27XlJeMaTh_SIirAfo1uVrGGDWa3Lg&oe=6569F74F").content
    debug_image_name = "debug_image.jpg"
    with open(debug_image_name, 'wb') as handler:
        handler.write(debug_image_data)
    debug_tk_image_open = ImageTk.PhotoImage(Image.open(debug_image_name).resize((250, 250)))
    debug_tk_image = tk.Label(main_frame, image=debug_tk_image_open)
    debug_tk_image.grid(row=1, column=1, padx=item_padding, pady=5)

    debug_description_text = ("Bizler 'Debug Entertaiment' şirketinin kurucularıyız.\n"
                              "Hedefimiz ileride bu hayali şirketi gerçeğe dökmek.\n"
                              "Debug Entertaiment Kurucu Üyeleri\n"
                              "Ahmet Aydoğan ve Emirhan Çalışkan")
    debug_description = tk.Label(main_frame, text=debug_description_text)
    debug_description.config(bg=main_frame_background_color, foreground=main_frame_foreground_color,
                             font=main_frame_description_font)
    debug_description.grid(row=2, column=1, padx=item_padding, pady=5, sticky='N')


window.mainloop()
