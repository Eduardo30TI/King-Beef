import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import os
from glob import glob
import socket as s
import pandas as pd
import time
from datetime import datetime
import Telas as gui

ico_path=os.path.join(os.getcwd(),'Icone','*.ico*')
ico=glob(ico_path)

if len(ico)>0:

    with open(ico[-1],'rb') as file:

        st.set_page_config(layout='wide',page_title='King Beef DM',page_icon=file.read())

        pass

    pass

else:

    st.set_page_config(layout='wide',page_title='King Beef')

    pass

class Login:

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

        temp_path=os.path.join(self.path_base,self.tela)
        arq=glob(temp_path)

        if len(arq)<=0:

            self.login()

            pass

        else:

            with open(arq[-1],'r') as file:

                name=file.read()

                pass

            if name=='Cadastro':

                app=gui.Cadastro()
                app.main()

                pass

            elif name=='Menu':

                app=gui.Menu()
                app.main()

                pass

            pass

        pass


    def login(self):

        placeholder=st.empty()

        with placeholder.container():

            divs=st.columns(3,vertical_alignment='center')

            with divs[1].container():

                imgs=st.columns(3,vertical_alignment='center')

                with imgs[1].container():

                    st.image('Logo/logo.png')

                    pass

                st.text_input('E-mail',key='log_email')
                st.text_input('Senha',key='log_senha',type='password')

                st.button('Acessar',type='primary',key='btn_acess',use_container_width=True)
                
                if st.session_state['btn_acess']:
                    
                    temp_path=os.path.join(self.path_excel,self.memoria)
                    arq=glob(temp_path)
                    

                    if st.session_state['log_email']=='ti@demarchibrasil.com.br' and st.session_state['log_senha']==f'Nvd@{datetime.now().year}{datetime.now().month}{datetime.now().day}':

                        temp_path=os.path.join(self.path_base,self.tela)
                        
                        with open(temp_path,'w') as file:

                            file.write('Cadastro')

                            pass

                        mensagem=st.success('Administrador logado com sucesso')
                        time.sleep(1)
                        mensagem.empty()

                        st.empty()
                        st.rerun()  

                        pass                   

                    if len(arq)>0:

                        df=pd.read_excel(temp_path,dtype='object')

                        cont=len(df.loc[(df['E-mail']==st.session_state['log_email'])&(df['Senha']==st.session_state['log_senha'])])

                        if st.session_state['log_email']=='' or st.session_state['log_senha']=='':

                            mensagem=st.warning('Preencha as informações no campo!')
                            time.sleep(1)
                            mensagem.empty()

                            pass

                        elif cont>0:

                            mensagem=st.success('Usuário logado com sucesso.')
                            time.sleep(1)
                            mensagem.empty()

                            temp_path=os.path.join(self.path_base,'log.xlsx')
                            df.loc[(df['E-mail']==st.session_state['log_email'])&(df['Senha']==st.session_state['log_senha'])].to_excel(temp_path,index=False)

                            temp_path=os.path.join(self.path_base,self.tela)
                            
                            with open(temp_path,'w') as file:

                                file.write('Menu')

                                pass

                            st.empty()
                            st.rerun()                       

                            pass

                        else:

                            mensagem=st.warning('Usuário não consta cadastrado na base de dados.')
                            time.sleep(1)
                            mensagem.empty()

                            time.sleep(5)
                            streamlit_js_eval(js_expressions='parent.window.location.reload()')                   

                            pass

                        pass

                    pass          

                pass

            pass
        

        pass


    pass



if __name__=='__main__':

    app=Login()
    app.main()

    pass