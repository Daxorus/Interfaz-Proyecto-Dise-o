import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from comunication import Comunication
import collections

"""
Codigo original de: https://youtu.be/DJY9TFxrYbM
Codigo adaptado por: Damian Morales.
"""

class Grafica(Frame):
    def __init__(self, master, *args):
        super().__init__(master, *args)
        self.datos_arduino = Comunication()
        self.actualizar_puertos()
        
        self.muestra = 100
        self.datos = 0.0
        
        self.fig, ax = plt.subplots(facecolor='#000000', dpi=100, figsize=(4,2))
        plt.title("Temperatura vs Tiempo",color='white',size =12)
        ax.tick_params(direction = "out", length=5, width=2,colors='r', grid_color='r',grid_alpha=0.5)
        
        self.line, = ax.plot([],[], color = 'w', marker = '+', linewidth=2,
            markersize = 1, markeredgecolor = 'k')
        
        plt.xlim=([0, self.muestra])
        #plt.ylim([0, 5.5])
        ax.set_xlim(xmin=0.0, xmax=100)
        ax.set_ylim(ymin=0, ymax=5)

        ax.set_facecolor('#6E6D7000')
        ax.spines['bottom'].set_color('blue')
        ax.spines['left'].set_color('blue')

        """
        ax.spines['top'].set_color('blue')
        ax.spines['right'].set_color('blue')
        """

        self.datos_señal_uno = collections.deque([0]*self.muestra, maxlen = self.muestra)
        
        self.widgets()
    
    def animate(self, i):
        self.datos = (self.datos_arduino.datos_recibidos.get())
        dato = self.datos.split(",")
        dato1 = float(dato[0])
        #datos2 = float(dato[1])
        
        self.datos_señal_uno.append(dato1)
        print(dato1)
        #self.datos_señal_dos.append(dato2)
        self.line.set_data(range(self.muestra), self.datos_señal_uno)
        #self.line2.set_data(range(self.muestra), self.datos_señal_dos)
    
    def iniciar(self,):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval =100, blit = False)
        self.bt_graficar.config(state = 'disabled')
        self.bt_pausar.config(state = 'normal')
        self.canvas.draw()

    def pausar(self):
        self.ani.event_source.stop()
        self.bt_reanudar.config(state = 'normal')

    def reanudar(self):
        self.ani.event_source.start()
        self.bt_reanudar.config(state = 'disabled')

        
    def widgets(self):
        frame = Frame(self.master, bg='gray50', bd=2)
        frame.grid(column=0, columnspan =2,row=0, sticky='nsew')
        frame1 = Frame(self.master, bg='black')
        frame1.grid(column=2, row=0, sticky='nsew')
        frame2 = Frame(self.master, bg='black')
        frame2.grid(column=3, row=0, sticky='nsew')

        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.columnconfigure(2, weight = 1)
        self.master.columnconfigure(3, weight = 1)
        self.master.rowconfigure(0, weight = 5)
        #self.master.rowconfigure(1, weight = 5)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master = frame)
        self.canvas.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')
        
        self.bt_graficar = Button(frame2, text='Graficar', width = 12, bg = 'white', fg = 'red',
             command= self.iniciar)
        self.bt_graficar.pack(pady = 5,expand = 1)

        self.bt_pausar = Button(frame2, text='Pausar', width = 12, bg = 'white', fg = 'red',
             command= self.pausar)
        self.bt_pausar.pack(pady = 5,expand = 1)

        self.bt_reanudar = Button(frame2, text='Reanudar', width = 12, bg = 'white', fg = 'red',
             command= self.reanudar)
        self.bt_reanudar.pack(pady = 5,expand = 1)
        
        self.bt_conectar = Button(frame1, text='Conectar', width = 12, bg = 'white', fg = 'red',
            command= self.conectar_serial)
        self.bt_conectar.pack(pady = 5,expand = 1)  

        self.bt_desconectar = Button(frame1, text='Desconectar', width = 12, bg = 'white', fg = 'red', 
            command= self.desconectar_serial)
        self.bt_desconectar.pack(pady = 5,expand = 1)


        port = self.datos_arduino.puertos
        baud = self.datos_arduino.baudrates

        Label(frame1, text= 'Puertos COM', bg='black', fg= 'white').pack(padx=5, expand=1)  
        self.combobox_port = ttk.Combobox(frame1, values = port, justify = 'center', width = 12)
        self.combobox_port.pack(pady = 1,expand = 1) 
        #self.combobox_port.current(0)     


        Label(frame1, text= 'Baudrates', bg='black', fg= 'white').pack(padx=0, expand=1)  
        self.combobox_baud = ttk.Combobox(frame1, values = baud, justify = 'center', width = 12)
        self.combobox_baud.pack(pady = 1,expand = 1) 
        self.combobox_baud.current(3)  
    
    def actualizar_puertos(self):
        self.datos_arduino.puertos_disponibles()

    def conectar_serial(self):
        self.bt_conectar.config(state='disabled')
        self.bt_desconectar.config(state='normal')
        self.bt_graficar.config(state='normal')
        self.bt_reanudar.config(state='disabled')

        self.datos_arduino.arduino.port = self.combobox_port.get()
        self.datos_arduino.arduino.baudrate = self.combobox_baud.get()
        self.datos_arduino.conexion_serial()
        
        #self.datos_arduino.arduino.port = self.datos_arduino.puertos[0]
        #self.datos_arduino.arduino.port = 'COM3'
        #self.datos_arduino.arduino.baudrate = self.datos_arduino.baudrates[0]
        #self.datos_arduino.conexion_serial()
    
    def desconectar_serial(self):
        self.bt_conectar.config(state='normal')
        self.bt_desconectar.config(state='disabled')
        self.bt_pausar.config(state='disabled')

        try:
            self.ani.event_source.stop()
        except AttributeError:
            pass
        self.datos_arduino.desconectar()
    
    """
    aqui definio lo que hacen algunos sliders
    
    """
    
if __name__ == "__main__":
    ventana = Tk()
    ventana.geometry=('800x600')

    
    app = Grafica(ventana)
    app.mainloop()
