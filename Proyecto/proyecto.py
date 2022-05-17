import math
import sys
from posixpath import normcase
import random
import agentpy as ap
import matplotlib.pyplot as plt
import numpy as np


def limpieza_datos(datos):
    datos_completos = []
    for line in datos: 
        datos_jugador = []
        for number in line.split(", "):
            number = number.replace("\n", "")
            datos_jugador.append(float(number))
        datos_completos.append(datos_jugador)
    return datos_completos

with open('datos_gol_messi.txt', 'r') as f:
    datos = f.readlines()
datos = limpieza_datos(datos)

datos_2 = np.zeros([6, len(datos[0])])

for i in range(0, 6):
    datos_2[i:] = np.array(datos[i])

datos = 100*datos_2 # Cada metro representará 100 unidades en el espacio.
f.close()

# ----------------------------------Simulación Original----------------------------------------------

def normalizacion(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def rotacion(v, theta): 
    matriz_rotacion = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
    v_rotado = np.dot(matriz_rotacion, v)
    return v_rotado

# class Jugador(ap.Agent):   

#     def setup_pos(self, espacio):
#         self.espacio = espacio
#         self.neighbors = espacio.neighbors   # .neighbors es un metodo de la clase Space que captura todo los vecinos dentro de una cierta distancia.
#         self.pos = espacio.positions[self]   # .positions es una variable de la clase Space, es un diccionario que vincula a cada agente con sus coordenadas en el espacio.


#     def cambio_posicion(self):
#         id = self.id #el id comienza a contar desde 2
#         pos = self.espacio.positions.values()
#         pos = np.array(list(pos)).T

#         # id == 2, Messi
#         # id == 3, Lass
#         # id == 4, Alonso
#         # id == 5, Ramos
#         # id == 6, Albiol
#         # id == 7, Marcelo
        

#         if id in range(2,8):
#             tramo_AB = datos[id-2][-4]/100   # estos son los frames que se tarda en recorrer el tramo AB
#             tramo_AC = (datos[id-2][-3]+datos[id-2][-4])/100
#             tramo_AD = (datos[id-2][-2]+datos[id-2][-3]+datos[id-2][-4])/100
#             tramo_AE = (datos[id-2][-1]+datos[id-2][-2]+datos[id-2][-3]+datos[id-2][-4])/100

#             if self.model.t<=tramo_AB:
#                 self.velocidad = np.array([datos[id-2][2], datos[id-2][3]]) - np.array([datos[id-2][0], datos[id-2][1]])
#                 self.espacio.move_by(self, self.velocidad/tramo_AB)

#             if tramo_AB<self.model.t<=tramo_AC:    
#                 self.velocidad = np.array([datos[id-2][4], datos[id-2][5]]) - np.array([datos[id-2][2], datos[id-2][3]])
#                 self.espacio.move_by(self, self.velocidad/(tramo_AC-tramo_AB))

#             if tramo_AC <self.model.t<=tramo_AD:    
#                 self.velocidad = np.array([datos[id-2][6], datos[id-2][7]]) - np.array([datos[id-2][4], datos[id-2][5]])
#                 if datos[id-2][-2] != 0: 
#                     self.espacio.move_by(self, self.velocidad /(tramo_AD- tramo_AC))

#             if tramo_AD <self.model.t<=tramo_AE:    
#                 self.velocidad = np.array([datos[id-2][8], datos[id-2][9]]) - np.array([datos[id-2][6], datos[id-2][7]])
#                 if datos[id-2][-1] != 0:
#                     self.espacio.move_by(self, self.velocidad /(tramo_AE- tramo_AD))

#     def probabilidad_de_gol(self):
#         id = self.id
#         h = 4400+100
#         w = 6800 +100+100
#         b = 732
#         if id == 2:
#             x = self.pos[0]
#             y = self.pos[1]
#             numerador = b*(h-y)
#             denominador = (((w-b-2*x)**2/4 + (h-y)**2)*((w+b-2*x)**2/4 + (h-y)**2))**0.5
#             angulo = np.arcsin(numerador/denominador)
#             probabilidad = 1/(1+np.exp(4.03 - 2.53*angulo - 0.12*(h-y)/100 - 0.11*(h-y)/100*angulo + 0.0069*(h-y)**2/10000))
#             if self.model.t<=120:
#                  return probabilidad        



# class Poblacion_modelo(ap.Model):

#     def setup(self):
#         self.espacio = ap.Space(self, shape=[self.p.size]*self.p.dimension)
#         self.agents = ap.AgentList(self, 10, Jugador) #creamos una cantidad |population| de agentes.
#         self.espacio.add_agents(self.agents, [[4066, 650], [4200, 600] , [3500, 650], [3220, 1690 ], [4166, 1690], [5100, 1800], [100,100], [6900, 100], [6900, 5350], [100, 5350]]) #metemos a los agentes creados en el espacio.
#         self.agents.setup_pos(self.espacio)

#     def step(self): 
#         self.agents.cambio_posicion()    
#         self.agents.probabilidad_de_gol()  
    

# def animacion_individual(m, ax):
#     ax.set_title(f"______{m.t}")
#     pos = m.espacio.positions.values()
#     pos = np.array(list(pos)).T 

#     ax.scatter(pos[0][0],pos[1][0], s=50, c='blue', marker = "o")
#     for j in range(1, 10):
#         ax.scatter(pos[0][j],pos[1][j], s=50, c='white', marker = "o")
             
#     ax.set_xlim(0, 7000) #0.4*m.p.size)
#     ax.set_ylim(0, 5450) #0.5*m.p.size)
#     ax.set_axis_off()
              


# def animacion_completa(m, p):
#     fig = plt.figure(figsize=(10,7))
#     fig.patch.set_facecolor("green")
#     ax = fig.add_subplot()
#     animation = ap.animate(m(p), fig, ax, animacion_individual, **{"interval": 100} )
#     plt.show()
#     animation.save("Gol Messi.gif", "GIF")
#     return animation


# # def grafico():
# #     graf = plt.plot(np.arange(0,145), np.arange(0,145) , color = "blue", label = "Susceptibles")
# #     plt.legend()
# #     plt.show()


# parameters = {
#     'dimension': 2,
#     'size': 7000,
#     'seed': 123,
#     'steps': 120,
#     'population': 81,
#     'R': 1.5,
#     'p_c': 0.033,
#     'p_u': 0.2,
#     'p_m': 0.15,
#     'p_quedados' : 0.1,
#     'distancia_al_borde': 3,
# }


# animacion_completa(Poblacion_modelo, parameters)
# # #grafico()


#--------------------------------------Simulación Alterada-----------------------------------

p_1 = random.uniform(0.5,1)
p_2a = np.array([random.uniform(0.5,1), random.uniform(0.5,1), random.uniform(0.5,1), random.uniform(0.5,1)])
p_2b = np.array([random.uniform(0.5,1), random.uniform(0.5,1), random.uniform(0.5,1), random.uniform(0.5,1)])
p_3 = random.uniform(0.5,1)

class Jugador_Simulado(ap.Agent):  

    def setup(self):
        self.estado = 0 
        self.record('estado', self.estado)

    def setup_pos_s(self, espacio):
        self.espacio = espacio
        self.neighbors = espacio.neighbors   # .neighbors es un metodo de la clase Space que captura todo los vecinos dentro de una cierta distancia.
        self.pos = espacio.positions[self]   # .positions es una variable de la clase Space, es un diccionario que vincula a cada agente con sus coordenadas en el espacio.
        
        
    def cambio_estado(self): 
        Messi_x = self.model.agents.log[0]['posiciones'][-1][0]
        Messi_y = self.model.agents.log[0]['posiciones'][-1][1]
        probabilidad_de_robo = 1- 0.68
        probabilidad_de_barrida = 0.3
        probabilidad_de_meter_pie = 0.5
        if self.estado == 0 and self.id in [5,6]:
            if np.linalg.norm([Messi_x-self.pos[0], Messi_y-self.pos[1]])< 50 and self.pos[1]>= Messi_y : 
                if random.uniform(0,1)<probabilidad_de_meter_pie: 
                    if random.uniform(0,1)<probabilidad_de_robo:
                        estado_nuevo = 1
                    else: 
                        estado_nuevo = -1
                
                elif random.uniform(0,1)<probabilidad_de_barrida:
                    if random.uniform(0,1)<probabilidad_de_robo:
                        estado_nuevo = 1
                    else: 
                        estado_nuevo = -2
                else: 
                    estado_nuevo = 0

            elif np.linalg.norm([Messi_x-self.pos[0], Messi_y-self.pos[1]])< 100 and self.pos[1]>= Messi_y : 
                if random.uniform(0,1)<probabilidad_de_barrida:
                    if random.uniform(0,1)<probabilidad_de_robo:
                        estado_nuevo = 1
                    else: 
                        estado_nuevo = -2 
                else: 
                    estado_nuevo = 0
            else: 
                estado_nuevo = 0

        elif self.estado == -1:
            
            if len(self.model.agents.log[self.id-2]['estado'])>= 4:
                if self.model.agents.log[self.id-2]['estado'][-4] == -1:
                    estado_nuevo = 0
                else: 
                    estado_nuevo = -1
            else: 
                estado_nuevo = -1  

        elif self.estado == -2: 
            if len(self.model.agents.log[self.id-2]['estado'])>= 10:
                if self.model.agents.log[self.id-2]['estado'][-10] == -2:
                    estado_nuevo = 0
                else: 
                    estado_nuevo = -2
            else: 
                estado_nuevo = -2

        elif self.estado == 1:
            if self.model.t<100:
                estado_nuevo = 1
            
                #print(self.model.agents.log[2]['estado'])  #(self.model.t, self.id, self.estado)   
            #sys.exit()
        else:
            estado_nuevo = 0
        
        self.estado = estado_nuevo
        if self.id in [5,6]:
            print(self.estado)
        self.record('estado', self.estado)
    
        
        
    def cambio_posicion_s(self):
        id = self.id #el id comienza a contar desde 2
        pos = self.espacio.positions.values()
        pos = np.array(list(pos)).T
        
        # id == 2, Messi
        # id == 3, Lass
        # id == 4, Alonso
        # id == 5, Ramos
        # id == 6, Albiol
        # id == 7, Marcelo

        self.record('posiciones', np.array([pos[0][0], pos[1][0]]))
        
        if id in range(2,8) and id not in [5,6]:
            tramo_AB = datos[id-2][-4]/100   # estos son los frames que se tarda en recorrer el tramo AB
            tramo_AC = (datos[id-2][-3]+datos[id-2][-4])/100
            tramo_AD = (datos[id-2][-2]+datos[id-2][-3]+datos[id-2][-4])/100
            tramo_AE = (datos[id-2][-1]+datos[id-2][-2]+datos[id-2][-3]+datos[id-2][-4])/100

            if self.model.t<=tramo_AB:
                self.velocidad = np.array([datos[id-2][2], datos[id-2][3]]) - np.array([datos[id-2][0], datos[id-2][1]])
                self.espacio.move_by(self, self.velocidad/tramo_AB)

            if tramo_AB<self.model.t<=tramo_AC:    
                self.velocidad = np.array([datos[id-2][4], datos[id-2][5]]) - np.array([datos[id-2][2], datos[id-2][3]])
                self.espacio.move_by(self, self.velocidad/(tramo_AC-tramo_AB))
                
            if tramo_AC <self.model.t<=tramo_AD:    
                self.velocidad = np.array([datos[id-2][6], datos[id-2][7]]) - np.array([datos[id-2][4], datos[id-2][5]])
                if datos[id-2][-2] != 0: 
                    self.espacio.move_by(self, self.velocidad /(tramo_AD- tramo_AC))

            if tramo_AD <self.model.t<=tramo_AE:    
                self.velocidad = np.array([datos[id-2][8], datos[id-2][9]]) - np.array([datos[id-2][6], datos[id-2][7]])
                if datos[id-2][-1] != 0:
                    self.espacio.move_by(self, self.velocidad /(tramo_AE- tramo_AD))

        if id in [5,6]: 
            
            Rapidez_max = [6.8,6.2] # Ramos corre lo más rápido en el último trayecto y cada frame avanza 4.2 unidades, que en esta escala serían 42.
            Messi_x = self.model.agents.log[0]['posiciones'][-1][0]
            Messi_y = self.model.agents.log[0]['posiciones'][-1][1]
            Ramos_x = pos[0][3]
            Ramos_y = pos[1][3]
            Albiol_x = pos[0][4]
            Albiol_y = pos[1][4]
            Velocidades_Messi = [np.array([-13.28, 25.78]), np.array([7.8, 30.55]), np.array([20.96, 30.55]), np.array([0, 34.36]) ]
            

            if self.estado == 0: 
                # Messi es zurdo 
                Defensas_a_la_izquierda = False
                for i in range(1, 6):
                    Jugadori_x = pos[0][i]
                    Jugadori_y = pos[1][i]
                    if 0<Messi_x-Jugadori_x<100 and Messi_y <Jugadori_y: # 1 metro son 100 unidades en el tablero
                        Defensas_a_la_izquierda = True
                if Defensas_a_la_izquierda == False:
                    Central_a_la_izq_id = 5
                    if Ramos_y < Messi_y or Ramos_x > Albiol_x:
                        Central_a_la_izq_id = 6
                    if Central_a_la_izq_id == id:
                        v_1 = p_1*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x - self.pos[0], 0]))
                    else:
                        v_1 = np.array([0,0])
                else:
                    v_1 = np.array([0,0])

                # Lejos del peligro, uno presiona y el otro cubre la espalda
                if Messi_y<2850:
                    if Ramos_y> Messi_y and Albiol_y> Messi_y:
                        if np.linalg.norm([Messi_x-Ramos_x,Messi_y-Ramos_y])<=np.linalg.norm([Messi_x-Albiol_x,Messi_y-Albiol_y]):
                            Central_atacante_id = 5
                        else: 
                            Central_atacante_id = 6
                        if id == Central_atacante_id: 
                            if self.model.t<=36: # El humano promedio tiene un reaction time de 0.2s, o sea 4 frames en nuestro caso 
                                v_2 = p_2a[0]*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 3*Velocidades_Messi[0]-np.array([self.pos[0], self.pos[1]]))
                            elif 36< self.model.t<=54:
                                v_2 = p_2a[1]*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 3*Velocidades_Messi[1]-np.array([self.pos[0], self.pos[1]]))
                            elif 54<self.model.t<= 81: 
                                v_2 = p_2a[2]*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 3*Velocidades_Messi[2]-np.array([self.pos[0], self.pos[1]]))
                            elif 81< self.model.t: 
                                v_2 = p_2a[3]*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 3*Velocidades_Messi[3]-np.array([self.pos[0], self.pos[1]])) 
                        elif id != Central_atacante_id: 
                            v_2 = ((100*Rapidez_max[id-5])/20)*normalizacion(np.array([(3500+Messi_x)/2 - self.pos[0],(4500+Messi_y)/2-self.pos[1]]))
                            
                    elif Ramos_y< Messi_y and Albiol_y< Messi_y:
                        v_2 = ((100*Rapidez_max[id-5])/20)*normalizacion(np.array([(3500+Messi_x)/2 - self.pos[0], (4500+Messi_y)/2-self.pos[1]]))
                    else: 
                        if self.pos[1]<Messi_y:
                            v_2 = ((100*Rapidez_max[id-5])/20)*normalizacion(np.array([(3500+Messi_x)/2 - self.pos[0], (4500+Messi_y)/2-self.pos[1]]))
                        else: 
                            if self.model.t<=36: 
                                v_2 = p_2b[0]*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 10*Velocidades_Messi[0]-np.array([self.pos[0], self.pos[1]]))
                            elif 36< self.model.t<=54:
                                v_2 = p_2b[1]*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 10*Velocidades_Messi[1]-np.array([self.pos[0], self.pos[1]]))
                            elif 54<self.model.t<= 81: 
                                v_2 = p_2b[2]*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 10*Velocidades_Messi[2]-np.array([self.pos[0], self.pos[1]]))
                            elif 81< self.model.t: 
                                v_2 = p_2b[3]*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 10*Velocidades_Messi[3]-np.array([self.pos[0], self.pos[1]])) 
                else:
                    v_2 = np.array([0,0])
            
                # Cerca del area, a presionar
                if Messi_y >= 2850: # está a un metro del area
                    if 40<self.model.t<= 81: 
                        v_3 = p_3*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 3*Velocidades_Messi[2]-np.array([self.pos[0], self.pos[1]]))
                    elif 81< self.model.t: 
                        v_3 = p_3*((100*Rapidez_max[id-5])/20)*normalizacion(np.array([Messi_x, Messi_y]) + 3*Velocidades_Messi[3]-np.array([self.pos[0], self.pos[1]])) 
                else: 
                    v_3 = np.array([0,0])


                # Intento de robo de pelota 

            else:
                v_1 = np.array([0,0])
                v_2 = np.array([0,0])
                v_3 = np.array([0,0])
            
            self.velocidad = v_1 + v_2 + v_3
            self.espacio.move_by(self, self.velocidad)

            

class Poblacion_modelo(ap.Model):

    def setup(self):
        self.espacio = ap.Space(self, shape=[self.p.size]*self.p.dimension)
        self.agents = ap.AgentList(self, 10, Jugador_Simulado) #creamos una cantidad |population| de agentes.
        self.espacio.add_agents(self.agents, [[4066, 650], [4200, 600] , [3500, 650], [3220, 1690 ], [4166, 1690], [5100, 1800], [100,100], [6900, 100], [6900, 4500], [100, 4500]]) #metemos a los agentes creados en el espacio.
        self.agents.setup_pos_s(self.espacio)

    def step(self): 
        self.agents.cambio_posicion_s()      
        self.agents.cambio_estado()
    

def animacion_individual(m, ax):
    ax.set_title(f"______{m.t}")
    ax.set_xlim(0, 7000)
    ax.set_ylim(0, 4600)
    ax.set_axis_off()
    pos = m.espacio.positions.values()
    pos = np.array(list(pos)).T 
    ax.plot([5516,5516, 1484, 1484], [4500,2850, 2850, 4500], color = "white")
    ax.plot([4416,4416, 2584 , 2584], [4500,3950, 3950, 4500], color = "white")
    ax.plot([100, 100, 6900, 6900], [100, 4500, 4500, 100], color = "white")  
    ax.scatter(pos[0][0],pos[1][0], s=50, c='blue', marker = "o")
    for j in range(1,8):
        if j not in [3,4]:
            ax.scatter(pos[0][j],pos[1][j], s=50, c='white', marker = "o")


    estados = []
    for i in range(3,5):
        temporal = m.agents.log[i]
        if len(temporal)!=0:
            estados.append(temporal['estado']) #Esta es una lista con todos los estados que ha pasado el agente i     
        if len(estados)==0:
            estado = 0 
        else: 
            estado = estados[i-3][-1]
            #print(estado)
        
        if estado == 0: 
            ax.scatter(pos[0][i],pos[1][i], s=50, c='white', marker = "o")
        elif estado == -1 or estado == -2:
            ax.scatter(pos[0][i],pos[1][i], s=50, c='red', marker = "o", alpha = 0.4)
        elif estado == 1: 
            ax.scatter(pos[0][i],pos[1][i], s=50, c='yellow', marker = "o")
            
    
    
    
              
    

def animacion_completa(m, p):
    fig = plt.figure(figsize=(10,7))
    fig.patch.set_facecolor("green")
    ax = fig.add_subplot()
    animation = ap.animate(m(p), fig, ax,  animacion_individual, **{"interval": 100} )
    plt.show()
    animation.save("Simulación Gol Messi 3.gif", "GIF")
    #return animation


# def grafico():
#     graf = plt.plot(np.arange(0,145), np.arange(0,145) , color = "blue", label = "Susceptibles")
#     plt.legend()
#     plt.show()


parameters = {
    'dimension': 2,
    'size': 7000,
    'seed': 123,
    'steps': 105,
    'population': 81,
    'R': 1.5,
}


animacion_completa(Poblacion_modelo, parameters)
# # # #grafico()
