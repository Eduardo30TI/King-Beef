import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from streamlit_option_menu import option_menu
import os
from glob import glob
import socket as s
import pandas as pd
import time
from datetime import datetime
import Telas as gui

class Menu:

    def __init__(self):

        self.IP=s.gethostbyname(s.gethostname())
        self.path_base=os.path.join(os.getcwd(),'PC',self.IP)
        os.makedirs(self.path_base,exist_ok=True)
        self.tela='tela.txt'

        self.path_excel=os.path.join(os.getcwd(),'Base')
        os.makedirs(self.path_excel,exist_ok=True)
        self.memoria='memoria.xlsx'        

        pass


    def main(self):

        placeholder=st.empty()

        with placeholder.container():

            with st.sidebar:

                temp_path=os.path.join(self.path_base,'log.xlsx')
                df=pd.read_excel(temp_path,dtype='object')
                
                user_name=df['E-mail'].unique().tolist()[-1]
                empresa=df['Empresa'].unique().tolist()[-1]
                
                st.image('Logo/logo.png')
                st.text(user_name)

                option_menu(menu_title='Opções',options=['Importar XML','Dashboard','Sair'],icons=['clipboard2','speedometer','box-arrow-left'],key='opc')

                pass

            if st.session_state['opc']=='Sair':

                temp_path=os.path.join(self.path_base,self.tela)
                os.remove(temp_path)

                st.empty()
                st.rerun()

                pass

            elif st.session_state['opc']=='Importar XML':

                app=gui.Importador()
                app.main()

                pass

            elif st.session_state['opc']=='Dashboard':

                app=gui.Dash()
                app.main()

                pass            

            pass

        pass    


    pass