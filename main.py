#Programa para comunicacion Wall-E por Alberto Esquer
#Ya que mi memoria es muy selectiva y suelo olvidar cosas inecesarias muy rapido
#y este metodo de programacion es nuevo para mi, me limitare a plasmar mis memorias
#a los largo del proyecto para retomar mas rapido el mismo.

#ChangeLog:
#v1.0 : inicio de menu y librerias telnet en python 3.4
#v1.1 : Se testeo la comunicacion se va a rescribir la parte de conectar para hacerlo global.
#Tambien se agrego un apartado de edef horareal():
#Se agrego funcion say para hablar y hora para saber el string de la hora.
#v1.2 : Se empezo a programar la ruta, se hicieron pruebas por putty para los movimientos
#Se definieron funciones con hora y un goto para moverse, tambien se creearon loops para simular
#encendido a cierta hora y funciono.
#v1.3 : Se redefinio hora para entregar un string de 4 caracteres con formato, es mas comodo
#se comentaron todas las funciones explicando su porque
#v1.4 : Se creo una funcion para cambiar fecha, en la version 3, pero no se cambio su changelog, 
#v2.0 : Se empezaron a realizar pruebas en campo.


#Iniciar Librerias

import telnetlib as tn
import time
import datetime as dt
import sys
import os

#Definir Variables de Conexion Globales

ipadress = "1.2.3.4"
password = "adept"
port = 7171
timeout = 1
walle = tn.Telnet(ipadress,port,timeout)
buf=walle.read_until(b'\n')

ready=False
working = False
charging = False
bussy = False

def hora():
	#print("La hora es: {:02d}:{:02d}".format(dt.datetime.today().hour,dt.datetime.today().minute))
	#horaactual = "{:02d}{:02d}".format(dt.datetime.today().hour,dt.datetime.today().minute)
	horax = int(dt.datetime.today().hour)
	return horax

def minuto():
	#print("La hora es: {:02d}:{:02d}".format(dt.datetime.today().hour,dt.datetime.today().minute))
	#horaactual = "{:02d}{:02d}".format(dt.datetime.today().hour,dt.datetime.today().minute)
	horax = int(dt.datetime.today().minute)
	return horax

def dia():
    day=dt.datetime.today().weekday()
    return day

# horareal: se esta trabajando, regresa el valor de la hora en string con el formato siguiente 00:00.
def horareal():
        horareal = "{:02d}:{:02d}".format(dt.datetime.today().hour,dt.datetime.today().minute)
        return horareal

def Interfaz():
    os.system('clear')
    print("----------------------------------------------------------------------") #70
    print("----                                                              ----")
    print("-                                MENU                                -")
    print("- Estado: OFFLINE                                      HORA: {}   -".format(horareal()))
    print("-                                                                    -")
    print("-                                                                    -")
    print("-  1.-Status para arranque                                           -")
    print("-  2.-Definir horario de carga                                       -")
    print("-  3.-                                                               -")
    print("-  4.-                                                               -")
    print("-  5.-                                                               -")
    print("-  6.-Cambiar Horario                                                -")
    print("-  r.-Actualizar                                                     -")#
    print("-  x.-Cerrar                                                         -")
    print("-                                                                    -")
    print("----------------------------------------------------------------------")
    menu()
    
def menu():
    #Interfaz()
    sta=input("-  Selecione una Opcion: ")
    if sta=="r":
        Interfaz()
        
    elif sta == "x":
        try:
            print("Cerrando Conexion")
            walle.close()
        except:
            Error(1)

        time.sleep(1)
        print("Cerrando programa")
        os.system('clear')
        sys.exit(1)
    elif sta == "1":
        try:
            status()
        except:
            Error(2)
            
    elif sta == "2":
        print("menu en trabajo")
    elif sta == "3":
        print("menu en trabajo")
    elif sta == "4":
        print("menu en trabajo")
    elif sta == "5":
        horario()

    elif sta == "6":
        status()
    
    else:
        print ("Clave Incorrecta")
        time.sleep(1.5)



def Error(x):
    if x ==1:
        print("Error de Conexion")
    if x == 2:
        print("Mensaje no enviado Error")
        
    else:
        print("Error Desconocido")

def say(texto):
	try:
		walle.write(b"say " +texto.encode('ascii') + b"\n")
	except:
		Error(1)

def escribe(texto):
    try:
        walle.write(texto.encode('ascii') + b"\n")
    except:
        Error(1)
        print(texto)

def send(text):
    try:
        acceso()
        walle.write(text.encode('ascii')+b"\n")
        print(text)
        #print((text.encode('ascii')+b'\n'))
        #buf = walle.read_eager()
        buf = walle.read_until(b'\n')
        buf = buf.decode('ascii')
        return buf
    except:
        Error(2)
        
def acceso():
    try:
        walle.close()
        time.sleep(.2)
        walle.open(ipadress,port,timeout)
        buf=walle.read_until(b'Enter password:\r\n')
        print("Intentando Conectar")
        walle.write(password.encode('ascii')+b"\n")
        print("Conexion Establecida")
        buf=walle.read_until(b"End of commands\r\n",10)
    except:
        Error(1)

def status():
    try:
        global ready
        global working
        global charging
        global bussy
    
        acceso()
        escribe("stop")
        time.sleep(.2)
        acceso()
        code = "status"
        
        walle.write(code.encode('ascii')+b"\n")
        estado=walle.read_until(b"\n")
        estado=estado.decode('ascii')
        estado=str(estado[25:])
        buf = walle.read_until(b"\n")
        buf = walle.read_until(b"\n")
        buf = walle.read_until(b"\n")
        localizacion = walle.read_until(b"\n")
        localizacion = localizacion.decode('ascii')
        localizacion = float(localizacion[19:])
        localizacion = localizacion * 100
        localizacion = str(localizacion)
        localizacion = (localizacion[:2])
        say("My status is "+estado)
        time.sleep(1)
        say("My Localization Score is "+localizacion)
        print(estado)
        print(localizacion)
        if estado == "Stopped\r\n":
            localizacion = int(localizacion)
            print("Listo Para correr")
            time.sleep(1)
            if localizacion > 50:
                say("I am ready to run in 10 seconds. Thank you")
                time.sleep(10)
                ready = True
                print(ready)
                print("aqui voy")
                #working = True
            else:
                say("Please check the localitation score")
        else:
            say("Please check and release the Emergency stop")
            time.sleep(5)
        
    except:
        Error(2)
        print("error en status")

def statuswork():
    try:
        acceso()
        escribe("stop")
        time.sleep(.2)
        acceso()
        code = "status"
        walle.write(code.encode('ascii')+b"\n")
        estado=walle.read_until(b"\n")
        estado=estado.decode('ascii')
        estado=str(estado[25:])
        buf = walle.read_until(b"\n")
        buf = walle.read_until(b"\n")
        buf = walle.read_until(b"\n")
        localizacion = walle.read_until(b"\n")
        print(localizacion)
        localizacion = localizacion.decode('ascii')
        localizacion = float(localizacion[19:])
        localizacion = localizacion * 100
        localizacion = str(localizacion)
        localizacion = (localizacion[:2])
        #say("My status is "+estado)
        time.sleep(1)
        #say("My Localization Score is "+localizacion)
        print(estado)
        if estado != "Stopped\r\n" or estado != "EStop pressed\r\n" or estado != "EStop relieved but motors still disabled\r\n":
            localizacion = int(localizacion)
            print("Estado OK")
            time.sleep(1)
            if localizacion > 50:
                #say("I am ready to run in 60 seconds Thank you")
                time.sleep(60)
                ready = True
        else:
            ready = False
            print("release")
            #say("Please check and release the Emergency stop button and press ON button.")
        
        
    except:
        Error(2)
        
def dock():
    say("dock")

def automatico():
    bussy = False
    charging= False
    working = False
    while True:
        if ready == False:
            print (ready)
            status()
            
        else:
            while ready == True:
                x = hora()
                y= minuto()
                y=y/100
                x=x+y
                print(x)
                if(dia()==0):
                    if (x>=0 and x<7.59) or (x>=18.36 and x<19.59):
                        
                        if charging == False:
                            acceso()
                            say("I need to charge my battery i will be back in 2 hours")
                            charging = True 
                            working = False
                            bussy = False
                            #cargar
                            escribe("dock")
                            time.sleep(5)
                            
                    else:
                        
                        working = True
                        charging = False
					
                
                elif(dia()<=3 and dia()>0):
                    if (x>=6.00 and x<7.59) or (x>=18.36 and x<19.59):
                        
                        if charging == False:
                            acceso()
                            say("I need to charge my battery i will be back in 2 hours")
                            charging = True 
                            working = False
                            bussy = False
                            #cargar
                            escribe("dock")
                            time.sleep(5)
                            
                    else:
                        
                        working = True
                        charging = False
                        
                elif(dia()==4):
                    x = hora()
                    y= minuto()
                    y=y/100
                    x=x+y
                    if (x==6.29):
                        
                        if charging == False:
                            acceso()
                            say("I need to charge my battery i will be back in 2 hours")
                            charging = True 
                            working = False
                            bussy = False
                            #cargar
                            escribe("dock")
                            #time.sleep(10800)
                            #escribe("undock")
                            charging = False
                            
                elif(dia()==5):
                    x = hora()
                    y= minuto()
                    y=y/100
                    x=x+y
                    if (x==6.29):
                        
                        if charging == False:
                            acceso()
                            say("I need to charge my battery i will be back in 2 hours")
                            charging = True 
                            working = False
                            bussy = False
                            #cargar
                            escribe("dock")
                            #time.sleep(10800)
                            #escribe("undock")
                            charging = False
                
                elif(dia()==6):
                    x = hora()
                    y= minuto()
                    y=y/100
                    x=x+y
                    if (x==6.29):
                        
                        if charging == False:
                            acceso()
                            say("I need to charge my battery i will be back in 2 hours")
                            charging = True 
                            working = False
                            bussy = False
                            #cargar
                            escribe("dock")
                            #time.sleep(10800)
                            #escribe("undock")
                            charging = False
                            

                else:
                    if charging == False:
                        acceso()
                        say("I need to charge my battery i will be back in 2 hours")
                        charging = True 
                        working = False
                        bussy = False
                        #cargar
                        escribe("dock")
                        time.sleep(5)
                        
                    
                    
                if working == True:
                    working = False
                    charging = False
                    if bussy == False:
                        acceso()
                        say("I am need to work")
                        time.sleep(3)
                        code = "patrol cleanroute"
                        walle.write(code.encode('ascii')+b"\n")
                        say("cleaning my routes")
                        time.sleep(10)
                        say("Beginning to patrol route 1")
                        acceso()
                        time.sleep(1)
                        code = "patrol Ruta1"
                        walle.write(code.encode('ascii')+b"\n")
                        #iniciar
                        print("voa trabajar")
                        bussy = True
                        
                        time.sleep(5)
                    
                time.sleep(2)
        time.sleep(2)
                    
def test():
    counter = 0
    bussy = False
    charging= False
    working = False
    while True:
        if ready == False:
            print (ready)
            status()
            
        else:
            while ready == True:
                x = minuto()
                print(x)
                if (x>=0 and x<5) or (x>=10 and x<15) or (x>=20 and x<25) or (x>=30 and x<35) or (x>=40 and x<45) or (x>=50 and x<55):
                    if charging == False:
                        counter = counter+1
                        acceso()
                        say("I need to charge my battery i will be back in 10 minutes")
                        time.sleep(2)
                        escribe("stop")
                        say("This is my charger number "+str(counter))
                        time.sleep(2)
                        charging = True 
                        working = False
                        bussy = False
                        #cargar
                        escribe("dock")
                        time.sleep(5)
                        
                else:
                    working = True
                    charging = False
                    
                if working == True:
                    working = False
                    charging = False
                    if bussy == False:
                        acceso()
                        say("I am need to work")
                        time.sleep(3)
                        code = "patrol test"
                        code2 = "gotoRouteGoal 6"
                        walle.write(code.encode('ascii')+b"\n")
                        time.sleep(1)
                        walle.write(code2.encode('ascii')+b"\n")
                        time.sleep(1)
                        #iniciar
                        print("voa trabajar")
                        bussy = True
                        
                        time.sleep(5)
                    
                time.sleep(2)
        time.sleep(2)
        
automatico()

#acceso()
#escribe("patrol 16 por ciento")

#while False:
    #walle = tn.Telnet(ipadress,port,timeout)
    #print(walle.read_until(b"Enter Password:",1))
    #walle.write(password.encode('ascii')+b"\n")
    #walle.write(say.encode('ascii')+b"\n")
    #print(walle.read_until(b"\n"))
    #time.sleep(2)
    #walle.close()
    #walle.open(ipadress,port,timeout)
    #print(walle.read_until(b"\n"))
    #walle.write(password.encode('ascii')+b"\n")
    #time.sleep(2)
    #walle.write(say2.encode('ascii')+b"\n")
