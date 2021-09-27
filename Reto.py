import datetime
from peewee import *
from flask import Flask, render_template, request,jsonify

app = Flask(__name__)
#HOST: "difaultn.duckdns.org"
#port: 33061, //En casa
#port: 33016, //Afuera
db =  MySQLDatabase("reto_grupodot", host='192.168.1.199', user='root', passwd='wd7yKQaBYuQZ8Zea',port=33061)


@app.route('/status',methods = ['POST'])
def status():
    return "funcionando"

@app.route('/api/buscar',methods = ['POST'])
def buscar():
    request_json=request.get_json()
    monto = float(request_json.get('monto'))
    esposible=ConsultarPrestamo(monto)
    if(esposible>=0):
        return "Hay socios disponible"
    else:
        return "No hay socio disponible"

@app.route('/api/socios',methods = ['POST'])
def apisocios():
    socios=(Socio.select()).dicts()
    json=jsonify({'Socios':list(socios)})
    return json

@app.route('/api/prestamos',methods = ['POST'])
def apiprestamos():
    prestamos=(Prestamo.select(Socio,Prestamo).join(Socio, on=(Socio.id == Prestamo.idSocio)).dicts())
    json=jsonify({'prestamos':list(prestamos)})
    return json

@app.route('/api/prestar',methods = ['POST'])
def apiprestar():
    request_json=request.get_json()
    monto = float(request_json.get('monto'))
    esposible=CrearPrestamo(monto,36)
    if(esposible):
        return"Se ha creado el prestamo"
    else:
        return"No hay socio disponible"

@app.route('/actualizar',methods = ['GET'])
def Actualizar():
    prestamos=(Prestamo.select(Socio.nombre_Socio,Prestamo.cuota_mensual,Prestamo.pago_futuro,Prestamo.tasa_interes_m).join(Socio, on=(Socio.id == Prestamo.idSocio)).dicts())
    return render_template('menu.html', data=list(prestamos))

@app.route('/cargar',methods = ['GET'])
def cargar():
    msg=prestamo_test_data()
    prestamos=(Prestamo.select(Socio.nombre_Socio,Prestamo.cuota_mensual,Prestamo.pago_futuro,Prestamo.tasa_interes_m).join(Socio, on=(Socio.id == Prestamo.idSocio)).dicts())
    return render_template('menu.html', data=list(prestamos),addstatus=msg)

@app.route('/prestar',methods = ['POST'])
def prestar():
    if request.method == 'POST':
        monto = request.form.get("monto")
        print (monto)
        esposible=CrearPrestamo(monto,36)
        msg=""
        if(esposible):
            msg="Se ha creado el prestamo"
            prestamos=(Prestamo.select(Socio.nombre_Socio,Prestamo.cuota_mensual,Prestamo.pago_futuro,Prestamo.tasa_interes_m).join(Socio, on=(Socio.id == Prestamo.idSocio)).dicts())
            return render_template('menu.html',addstatus=msg,data=list(prestamos)) 
        else:
            msg="No hay socio disponible"
            return render_template('menu.html',addstatus=msg) 
        
@app.route('/',methods = ['GET'])
def student():
    return render_template('menu.html')

@app.route('/vsocios',methods = ['GET'])
def vsocios():
    socios=(Socio.select().dicts())
    return render_template('datossocio.html', data=list(socios))

@app.route('/addvsocios',methods = ['POST'])
def addvsocios():
    nombre = request.form.get("nombre_Socio")
    tasa = request.form.get("Tasa_interes")
    monto = request.form.get("Monto_Max")
    Socio.create(nombre_Socio=nombre,Tasa_interes=tasa ,Monto_Max=monto)
    socios=(Socio.select().dicts())
    return render_template('datossocio.html', data=list(socios))

class BaseModel(Model):
    class Meta:
        database = db

class Socio(BaseModel):
    nombre_Socio= CharField(null = False)
    Tasa_interes = DoubleField(null = False)
    Monto_Max = DoubleField(null = False)
    class Meta:
        db_table="Socio"

class Prestamo(BaseModel):
    idSocio = ForeignKeyField(Socio, backref='Prestamo',null = False)
    timestamp = DateTimeField(default=datetime.datetime.now,null = False)
    cuota_mensual = DoubleField(null = False)    
    pago_futuro = DoubleField(null = False)
    tasa_interes_m = DoubleField(null = False)
    class Meta:
        db_table="Prestamo"

def prestamo_test_data():
    db.create_tables([Socio, Prestamo])
    data = (
        ('Juan', 1.5,5000000),
        ('Andres', 2,7500000),
        ('Maria', 1.2,3000000))
    
    try:
        name=Socio.get(Socio.nombre_Socio == "Juan")
        print(name)
        return "Test Data ya cargada"
    except:
        for socios,tasas_i,monto_max in data:
            socio = Socio.create(nombre_Socio=socios,Tasa_interes=tasas_i,Monto_Max=monto_max)
        #prestamo=Prestamo.create(idSocio=2,cuota_mensual=171111.11 ,pago_futuro=6160000,tasa_interes_m=1.5)
        return "Se carga Test Data"
        
def updateMonto(id,monto):
    socio=Socio.get(Socio.id==id)
    socio.Monto_Max=monto
    socio.save()
   

def ConsultarPrestamo(monto):
    posiblesSocios = Socio.select().where(Socio.Monto_Max >=monto).order_by(Socio.Tasa_interes)
    if len(posiblesSocios)>0:
        posibleSocio=posiblesSocios[0]        
        return posibleSocio.id        
    else:
        return -1
    
def CrearPrestamo(valoraprestar,nmeses):
    idsocio=ConsultarPrestamo(valoraprestar)
    if idsocio>=0:        
        socio=Socio.get(Socio.id == idsocio)
        tasainteresseleccionada=float(socio.Tasa_interes) 
        valoraprestar=float(valoraprestar)
        nmeses= float(nmeses)
        vfuturo=valoraprestar*(1+(nmeses*(tasainteresseleccionada/100)))  
        vfuturo=round(vfuturo, 2)
        cuotamensual=vfuturo/nmeses
        cuotamensual=round(cuotamensual, 2)  
        prestamo=Prestamo.create(idSocio=idsocio,cuota_mensual=cuotamensual ,pago_futuro=vfuturo,tasa_interes_m=tasainteresseleccionada)
        updateMonto(idsocio,((socio.Monto_Max)-valoraprestar))
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(port=5000)
    #app.run(host="0.0.0.0", port=8080)