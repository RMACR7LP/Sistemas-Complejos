import numpy as np
from math import *
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


# --------------------- Dibujo del la bifurcación----------------------------------------------


N = 500  # indice máximo de la sucesión

#Debido a que eventualmente la sucesión converge a sus puntos fijos tomaremos
#el extracto final de la sucesión truncada esperando que para entonces
#los puntos fijos ya se muestren

T = 500  #elementos en la partición del intervalo (1,4) que es donde puede estar el coeficiente a
a_vector = np.ones(T)
for i in range(1,T):
    a_vector[i] = a_vector[i] + i*3/500         # coeficientes del mapeo logístico


for i in range(T-1):
    a = a_vector[i]  
    x = np.zeros(N)  # sucesión truncada
    x[0] = 0.5  #Definimos un estado inicial
    for n in range(0,N-1):        #definimos la relación de recurrencia
        x[n+1] = a*x[n]*(1-x[n])  

    cola_sucesion = x[np.arange(round(N*0.9), N)]  
    puntos_fijos= np.unique(cola_sucesion)
    eje_x = a*np.ones(len(puntos_fijos))  #valores del coeficiente 
    plt.plot(eje_x, puntos_fijos, ".")     #para un coeficiente, grafico los respectivos puntos fijos

plt.show()

#------------------------------- Dibujo del mapeo de Mandelbrot--------------------------------------

# Consideraremos cada pixel en la pantalla como un punto en el plano complejo

# from PIL import Image, ImageDraw

# Ancho = 1200  #Definimos las dimensiones de nuestro canvas
# Alto = 800

# mandelbrot = Image.new('RGB', (Ancho, Alto), (255,255,255))  # Creamos el canvas
# dibujo = ImageDraw.Draw(mandelbrot)                    # Pintamos y mostramos 

# def En_Mandelbrot(c):
#     z = np.zeros(500, dtype=complex)
#     for n in range(0, 499):
#         z[0]=0
#         z[n+1] = z[n]**2+ c
#         if abs(z[n+1])>2:
#             return False
#     return True
        





# A continuación pintaremos el canvas para que dibuje el conjunto de Mandelbrot.

# for x in range(0,Ancho):
#     for y in range(0, Alto):
#         # Convertir pixeles en numeros complejos
#         c = complex((x-Ancho/2)*3/Ancho,(y-Alto/2)*2/Alto)
#         # Verificar si el punto pertenece al conjunto de Mandelbrot
#         if En_Mandelbrot(c):    
#             dibujo.point([x+Ancho/4, y], (0, 0, 0))

# mandelbrot.save('mandelbrot.png', 'PNG')



# ------------------------------- Lorenz------------------------------------------
# sigma = 10
# r = 28
# b = 8/3

# def f(t,x,y,z):                 #Definimos el sistema de Lorenz
#     func_x = sigma*(y-x)
#     func_y = r*x-y-x*z
#     func_z = -b*z+x*y 
#     return (t, func_x, func_y, func_z)

# def RK4(f, t_0, x_0, y_0, z_0, n):   # Runge Kutta con paso h = 0.0015
#     t = np.zeros(n)
#     x = np.zeros(n)
#     y = np.zeros(n)
#     z = np.zeros(n)
#     t[0] = 0
#     x[0] = x_0
#     y[0] = y_0
#     z[0] = z_0
#     h = 0.0015
#     for i in range(n-1):
#         k_1 = f(t[i], x[i], y[i], z[i])
#         k_2 = f(t[i]+h/2, x[i]+k_1[1]*h/2, y[i]+k_1[2]*h/2, z[i]+k_1[3]*h/2)
#         k_3 = f(t[i]+h/2, x[i]+k_2[1]*h/2, y[i]+k_2[2]*h/2, z[i]+k_2[3]*h/2)
#         k_4 = f(t[i]+h, x[i]+k_3[1]*h, y[i]+k_3[2]*h, z[i]+k_3[3]*h)
#         t[i+1] = t[i]+h
#         x[i+1] = x[i]+(h/6)*(k_1[1]+2*k_2[1]+2*k_3[1]+k_4[1])
#         y[i+1] = y[i]+(h/6)*(k_1[2]+2*k_2[2]+2*k_3[2]+k_4[2])
#         z[i+1] = z[i]+(h/6)*(k_1[3]+2*k_2[3]+2*k_3[3]+k_4[3])
    
#     plt.plot(t, x, "-")
#     plt.show()
#     plt.plot(t, y, "-")
#     plt.show()
#     plt.plot(t, z, "-")
#     plt.show()
#     plt.plot(x,y, "-")
#     plt.show()
#     plt.plot(x,z, "-")
#     plt.show()
#     plt.plot(y,z, "-")
    
#     fig  = plt.figure()
#     ax = plt.axes(projection = "3d")
#     ax.plot3D(x,y,z,'green')
#     plt.show()

#     return "."

# RK4(f, 0, 5, 5, 5, 20000)  # Definimos las condiciones iniciales

