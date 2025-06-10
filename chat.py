#importar y renombrar streamlit
import streamlit as st
import groq

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192']
#CONFIGURAR PAGINA
def configurar_pagina():
     st.set_page_config(page_title="Mi primer ChatBot con Python")
     st.title("IA by DaIAn")

#Crear un cliente de groq
def crear_cliente_groq():
     groq_api_key = st.secrets["GROQ_API_KEY"]
     return groq.Groq(api_key=groq_api_key)

#MOSTRAR LA BARRA LATERAL
def mostrar_sidebar():
     st.sidebar.title("Eleji tu modelo de IA favorito")
     modelo = st.sidebar.selectbox("Opciones",MODELOS,index=0)
     st.write(f"**Elegiste el modelo** {modelo}")
     return modelo

def ejecutar_chat():
     configurar_pagina()
     modelo = mostrar_sidebar()
     print(modelo)

#INICIALIZAR EL ESTADO DEL CHAT
#streamlit= variable especial llamada session_state.{mensajes = []}
def inicializar_estado_chat():
     if "mensajes" not in st.session_state:
          st.session_state.mensajes = [] #lista

#mostrar mensajes previos 
def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])   

#Obtener mensaje usuario
def obtener_mensaje_usuario():
     return st.chat_input("Envia tu mensaje", key="input_usuario")

#Guardar los mensajes
def agregar_mensajes_previos(role, content):
     st.session_state.mensajes.append({"role": role, "content" : content})

#Mostrar los mensajes en pantalla
def mostrar_mensaje(role, content):
     with st.chat_message(role):
          st.markdown(content)

#Creacion del modelo de groq
def obtener_respuesta_modelo(cliente, modelo, mensaje):
     respuesta = cliente.chat.completions.create(
          model = modelo,
          messages = mensaje,
          stream = False
     ) 
     return respuesta.choices[0].message.content

def ejecutar_chat():
     configurar_pagina()
     cliente = crear_cliente_groq()
     modelo = mostrar_sidebar()

     inicializar_estado_chat()
     obtener_mensajes_previos()

     mensaje_usuario = obtener_mensaje_usuario()

     if mensaje_usuario:
          agregar_mensajes_previos("user", mensaje_usuario)
          mostrar_mensaje("user", mensaje_usuario)

          respuesta_contenido = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes )
          agregar_mensajes_previos("assistant",respuesta_contenido)
          mostrar_mensaje("assistant", respuesta_contenido)

# EJECUTAR LA APP 
if __name__ == '__main__':
     ejecutar_chat()