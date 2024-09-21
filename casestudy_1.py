# master_id: Eşsiz müşteri numarası
# order_channel: Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile)
# last_order_channel: En son alışverişin yapıldığı kanal
# first_order_date: Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date: Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online: Müşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline: Müşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online: Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline: Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline: Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online: Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12: Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listes

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width',1000)
##############################################
#  Görev 1: Veriyi Anlama ve Hazırlama
##############################################

# Adım 1: flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.
df_ = pd.read_csv("C:\\Users\\bferid854\\PycharmProjects\\CRM_Analytics\\projects\\case_study_1\\flo_data_20k.csv")
df = df_.copy()

'Adım 2: Veri setinde'

# a. İlk 10 gözlem,
df.head(10)
# b. Değişken isimleri,
df.columns
# c. Betimsel istatistik,
df.shape
df.describe().T
# d. Boş değer,
df.isnull().sum()
df.isnull()
# e. Değişken tipleri, incelemesi yapınız.
df.dtypes
df.info()

# Adım 3: Omnichannel müşterilerin hem online'dan hemde offline
# platformlardan alışveriş yaptığını ifade etmektedir. Her bir müşterinin
# toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.

df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
# Adım 4: Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()
# Adım 5: Alışveriş kanallarındaki müşteri sayısının,toplam alınan
# ürün sayısının ve toplam harcamaların dağılımına bakınız.
df.groupby('order_channel').agg({'master_id': 'count',
                                 'order_num_total': 'sum',
                                 'customer_value_total': 'sum'})

# Adım 6: En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.

df.sort_values('customer_value_total',ascending=False).head(10)

# Adım 7: En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
df.sort_values('order_num_total',ascending=False).head(10)

# Adım 8: Veri ön hazırlık sürecini fonksiyonlaştırınız.

def data_preparation (dataframe):
    dataframe['order_num_total'] = dataframe['order_num_total_ever_online'] + dataframe['order_num_total_ever_offline']
    dataframe['customer_value_total'] = dataframe['customer_value_total_ever_offline'] + dataframe['customer_value_total_ever_online']
    date_columns = dataframe.columns[dataframe.columns.str.contains('date')]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    return dataframe

############################################################################################
#Görev 2: RFM Metriklerinin Hesaplanması
############################################################################################

# Adım 1: Recency, Frequency ve Monetary tanımlarını yapınız.
# recency: analiz tarihi- son satış tarihi
# frequency: müşteri özelinde satın alma işlemi sayısı toplamı
# monetary : müşteri özelinde bırakılan kar mikterı

# Adım 2: Müşteri özelinde Recency, Frequency ve Monetary metriklerini hesaplayınız.
df['last_order_date'].max() # 2021-05-30
today_date = dt.datetime(2021,6,1)
type(today_date)

df.head()
df['master_id'] = df['master_id'].astype(str)


# Adım 3: Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.

# Benim yöntemim
rfm = df.groupby('master_id').agg({'last_order_date': lambda x: (today_date - x).dt.days,
                                   'order_num_total': lambda x: x,
                                   'customer_value_total': lambda x: x})


rfm.columns = ['recency','frequency','monetary']


# Eğitmenin çözüm videosunda yaptığı yöntem:

"""
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (today_date - df["last_order_date"]).dt.days
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]
"""
# Adım 4: Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.
rfm.head()
##########################################################
#Görev 3: RF Skorunun Hesaplanması
##########################################################
#Adım 1: Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.

pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

#Adım 2: Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm.head()
rfm.dtypes
#Adım 3: recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz.

rfm['rf_score'] = (rfm['recency_score'].astype(str)) + (rfm['frequency_score'].astype(str))
rfm.head()

##########################################################
#Görev 4: RF Skorunun Segment Olarak Tanımlanması
##########################################################

#Adım 1: Oluşturulan RF skorları için segment tanımlamaları yapınız.

#Adım 2: Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['rf_score'].replace(seg_map, regex=True)


##########################################################
# Görev 5: Aksiyon Zamanı !
##########################################################

# Adım 1: Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])


# Adım 2: RFM analizi yardımıyla aşağıda verilen 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv olarak kaydediniz.


# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri
# tercihlerinin üstünde. Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak
# iletişime geçmek isteniliyor. Sadık müşterilerinden(champions, loyal_customers) ve kadın kategorisinden alışveriş
# yapan kişiler özel olarak iletişim kurulacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına kaydediniz.

# b. Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte
# iyi müşteri olan ama uzun süredir alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni
# gelen müşteriler özel olarak hedef alınmak isteniyor. Uygun profildeki müşterilerin id'lerini csv dosyasına kaydediniz.
