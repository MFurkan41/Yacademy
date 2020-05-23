from flask import Flask,render_template,redirect,url_for,request,flash
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,BooleanField
import sqlite3
import flask_excel as excel

# Öğrenci Girişi için Form
class StuRegister(Form):
    veli_ads = StringField("Veli Adı Soyadı",validators=[validators.DataRequired()])
    veli_tel = StringField("Veli Telefon Numarası",validators=[validators.DataRequired()])
    veli_il = StringField("Veli İl",validators=[validators.DataRequired()])
    veli_email = StringField("Veli E-Mail",validators=[validators.DataRequired()])
    ogr_ads = StringField("Öğrenci Adı",validators=[validators.DataRequired()])
    tr_18 = BooleanField("Türkçe 18:00 Grubu")
    tr_21 = BooleanField("Türkçe 21:00 Grubu")
    mat_18 = BooleanField("Matematik 18:00 Grubu")
    mat_21 = BooleanField("Matematik 21:00 Grubu")
    fen_18 = BooleanField("Fen 18:00 Grubu")
    fen_21 = BooleanField("Fen 21:00 Grubu")
    odeme_bilgi = TextAreaField("Hangi Derse Ne Kadar Ödediniz?",validators=[validators.DataRequired()])
    oneriler = TextAreaField("Dersler ile ilgili önerileriniz...",validators=[validators.DataRequired()])

# Öğretmenler için Giriş Form
class LoginForm(Form):
    username = StringField("Kullanıcı Adı",validators=[validators.DataRequired()])
    password = PasswordField("Şifre",validators=[validators.DataRequired()])

app = Flask(__name__)
app.secret_key = "yacademy"
excel.init_excel(app)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/newstu',methods=["GET","POST"])
def newstu():
    form =StuRegister(request.form)
    
    if(request.method == "POST" and form.validate()):
        veli_ads= str(form.veli_ads.data)
        veli_tel= str(form.veli_tel.data)
        veli_il= str(form.veli_il.data)
        veli_email= str(form.veli_email.data)
        ogr_ads= str(form.ogr_ads.data)
        tr_18= str(form.tr_18.data)
        tr_21= str(form.tr_21.data)
        mat_18= str(form.mat_18.data)
        mat_21= str(form.mat_21.data)
        fen_18= str(form.fen_18.data)
        fen_21= str(form.fen_21.data)
        odeme_bilgi= str(form.odeme_bilgi.data)
        oneriler= str(form.oneriler.data)
        baglanti = sqlite3.connect("database.db")
        cursor = baglanti.cursor()
        sorgu = "SELECT * FROM students WHERE veli_tel='{}'".format(veli_tel)
        cursor.execute(sorgu)
        data = cursor.fetchall()
        
        if not data:
            sorgu = "INSERT INTO students(veli_ads,veli_tel,veli_il,veli_email,ogr_ads,tr_18,tr_21,mat_18,mat_21,fen_18,fen_21,odeme_bilgi,oneriler) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(veli_ads,veli_tel,veli_il,veli_email,ogr_ads,tr_18,tr_21,mat_18,mat_21,fen_18,fen_21,odeme_bilgi,oneriler)
            cursor.execute(sorgu)
            baglanti.commit()
            f = "{} Bey/Hanım, başarıyla kaydınız oluşturuldu. Lütfen çift kayıt oluşturmayınız. Kaydınızda değişiklik yapmak istiyorsanız +90 552 229 27 78 numaralı telefona Whatsapp üzerinden ulaşınız.".format(veli_ads)
            flash(f,"success")
            return redirect(url_for('index'))
        else:
            f = "{} Bey/Hanım, kaydınız oluşturulamadı. Önceden oluşturulmuş bir kaydınız bulunmaktadır. Kaydınızda değişiklik yapmak için +90 552 229 27 78 numaralı telefona Whatsapp üzerinden ulaşınız.".format(veli_ads)
            flash(f,"warning")
            return redirect(url_for('index'))
    else:
        return render_template("register.html",form=form)


@app.route('/teacher',methods=["GET","POST"])
def teacher():
    usernames = [["myolal","yolal"],["sefa","VGUr8gSm"],["yusuf","W7xvJysC"],["seref","YrBTTY7Y"]]
    #usernames = [["myolal","yolal"],["sefa","1234"],["yusuf","1234"],["seref","1234"]]
    form = LoginForm(request.form)
    if(request.method == "POST" and form.validate()):
        username = str(form.username.data)
        password = str(form.password.data)
        for i in range(len(usernames)):
            if(usernames[i][0] == username and usernames[i][1] == password):
                ders = "tr" if usernames[i][0] == "sefa" else ("mat" if usernames[i][0] == "yusuf" else ("fen" if usernames[i][0] == "seref" else ("")))
        baglanti = sqlite3.connect("database.db")
        cursor = baglanti.cursor()
        try:
            sorgu = "SELECT * FROM students WHERE {}_18='True' or {}_21='True'".format(str(ders),str(ders))
        except UnboundLocalError:
            f = "Kullanıcı adınız veya şifrenizi yanlış girdiniz. Tekrar denemeniz halinde giriş yapamıyorsanız +90 552 229 27 78 numaralı telefona Whatsapp üzerinden ulaşınız."
            flash(f,"warning")
            return redirect(url_for('index'))
        if(ders == ""):
            sorgu = "SELECT * FROM students"
        cursor.execute(sorgu)
        data = cursor.fetchall()
        for j in range(len(data)):
            liste = ["6","7","8","9","10","11"]
            data[j] = list(data[j])
            for b in range(len(liste)):
                if(str(data[j][int(liste[b])]) == "True"):
                    data[j][(int(liste[b]))] = "<span>&#9989;</span>"
                elif(str(data[j][int(liste[b])]) == "False"):
                    data[j][int(liste[b])] = "<span>&#10060;</span>"
        hoca = "Sefa" if ders == "tr" else("Yusuf" if ders =="mat" else("Şeref" if ders == "fen" else ("Murat" if ders == "" else "")))
        #ders = "Türkçe" if ders == "tr" else ("Matematik" if ders == "mat" else ("Fen" if ders == "fen" else ("")))
        return render_template("students.html",data=data,ders=ders,len=len(data),hoca=hoca)
    else:
        return render_template("teacher.html",form=form)

@app.route("/ds/<id>")
def deletestu(id):
    baglanti = sqlite3.connect("database.db")
    cursor = baglanti.cursor()
    sorgu = "SELECT * FROM students WHERE id='{}'".format(int(id))
    cursor.execute(sorgu)
    data = cursor.fetchall()
    sorgu = "DELETE FROM students WHERE id='{}'".format(int(id))
    cursor.execute(sorgu)
    baglanti.commit()
    f = "{} adlı öğrencinin kaydı silinmiştir.".format(data[0][5])
    flash(f,"warning")
    return redirect(url_for('index'))
@app.route("/exportxlsx/<ders>")
def exportxlsx(ders):
    baglanti = sqlite3.connect("database.db")
    cursor = baglanti.cursor()
    u_ders = "Türkçe" if ders == "tr" else("Matematik" if ders == "mat" else("Fen" if ders == "fen" else ""))
    if ders == "tr" or ders == "fen" or ders == "mat":
        sorgu = "SELECT * FROM students WHERE {}_18 = 'True' or {}_21 = 'True';".format(str(ders),str(ders))
        cursor.execute(sorgu)
        data = cursor.fetchall()
        g18 = str("{} 18:00 Grubu".format(str(u_ders)))
        g21 = str("{} 21:00 Grubu".format(str(u_ders)))
        data.insert(0, ["#","Veli Adı Soyadı","Veli Tel No","Veli İl","Veli E-Mail","Öğrenci Adı",g18,g21,"Ödeme Bilgisi","Öğrenci Önerisi"])
        for i in range(1,len(data)):
            data[i] = list(data[i])
            if ders == "tr":
                data[i].pop(8)
                data[i].pop(8)
                data[i].pop(8)
                data[i].pop(8)
            elif ders == "mat":
                data[i].pop(6)
                data[i].pop(6)
                data[i].pop(8)
                data[i].pop(8)
            elif ders == "fen":
                data[i].pop(6)
                data[i].pop(6)
                data[i].pop(6)
                data[i].pop(6)
        for j in range(len(data)):
            liste = ["6","7"]
            data[j] = list(data[j])
            for b in range(len(liste)):
                try:
                    if(str(data[j][int(liste[b])]) == "True"):
                        data[j][int(liste[b])] = "✅"
                    elif(str(data[j][int(liste[b])]) == "False"):
                        data[j][int(liste[b])] = "❌"
                except:
                    pass
        return excel.make_response_from_array(data,"xlsx",file_name="{}_Dersi_Listesi".format(str(u_ders)))
    else:
        sorgu = "SELECT * FROM students"
        cursor.execute(sorgu)
        data = cursor.fetchall()
        data.insert(0,["#","Veli Adı Soyadı","Veli Telefon Numarası","Veli İl","Veli E-Mail","Öğrenci Adı","Türkçe 18:00 Grubu","Türkçe 21:00 Grubu","Matematik 18:00 Grubu","Matematik 21:00 Grubu","Fen 18:00 Grubu","Fen 21:00 Grubu","Ödeme Bilgi","Öneriler"])
        for j in range(len(data)):
            liste = ["6","7","8","9","10","11"]
            data[j] = list(data[j])
            for b in range(len(liste)):
                if(str(data[j][int(liste[b])]) == "True"):
                    data[j][(int(liste[b]))] = "✅"
                elif(str(data[j][int(liste[b])]) == "False"):
                    data[j][int(liste[b])] = "❌"
        return excel.make_response_from_array(data,"xlsx",file_name="Tüm_Dersler_Liste")


if __name__ == "__main__":
    app.run(debug=True)
