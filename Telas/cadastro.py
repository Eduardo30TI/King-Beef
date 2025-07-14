import streamlit as st
import os
from glob import glob
import socket as s
import pandas as pd
import time
from datetime import datetime
from streamlit_js_eval import streamlit_js_eval
from CNPJ import CNPJ

delete=None

class Cadastro:

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

        df=pd.DataFrame(columns=['E-mail','Senha','Empresa'])

        temp_path=os.path.join(self.path_excel,self.memoria)
        arq=glob(temp_path)

        if len(arq)>0:

            df=pd.read_excel(temp_path,dtype='object')

            pass

        placeholder=st.empty()

        with placeholder.container():

            divs=st.columns(3,vertical_alignment='center')

            with divs[1].container():

                imgs=st.columns(3,vertical_alignment='center')

                with imgs[1].container():

                    st.image('Logo/logo.png')

                    pass

                tab1,tab2=st.tabs(['Cadastro','Lista'])

                with tab1.container():   

                    st.subheader('Cadastro')

                    st.text_input('E-mail',key='cad_email')
                    st.text_input('Senha',type='password',key='cad_senha')
                    st.text_input('Validar',type='password',key='cad_validar')

                    cols=st.columns(2,vertical_alignment='bottom')

                    with cols[0].container():

                        st.text_input('CNPJ',key='cad_cnpj')

                        pass

                    with cols[-1].container():

                        st.button('CNPJ',key='btn_cnpj')

                        pass

                    if st.session_state['btn_cnpj']:

                        js=CNPJ.getDados(st.session_state['cad_cnpj'])
                        empresa=str(js['alias']).upper()

                        st.text_input('Empresa',value=empresa,disabled=True,key='cad_empresa')

                        pass                

                    btns=st.columns(2,vertical_alignment='center')

                    with btns[0]:

                        st.button('Salvar',key='cad_save',use_container_width=True,type='primary')

                        pass

                    with btns[-1]:

                        st.button('Sair',key='cad_exit',use_container_width=True)

                        pass

                    pass

                with tab2.container():
                
                    st.data_editor(df,use_container_width=True,hide_index=True)

                    lista=df['E-mail'].unique().tolist()
                    cols=st.columns([6,2],vertical_alignment='bottom')

                    with cols[0].container():

                        st.multiselect(label='Filtro',options=lista,placeholder='Escolha um usuário',label_visibility='collapsed',max_selections=1,key='mult1')

                        pass

                    with cols[-1].container():

                        disable=False if len(st.session_state['mult1'])>0 else True
                        st.button('Deletar',key='btn_delete',type='primary',use_container_width=True,disabled=disable)

                        pass

                    if len(st.session_state['mult1'])<=0:

                        st.text_input('Senha',key='edit_senha')
                        st.text_input('Nova Senha',key='edit_nova',type='password')

                        st.button('Editar',key='btn_edit',type='primary')                        

                        pass


                    else:

                        senha=df.loc[df['E-mail']==st.session_state['mult1'][-1],'Senha'].unique().tolist()[-1]
                        st.text_input('Senha',key='edit_senha',value=senha,disabled=True,type='password')
                        st.text_input('Nova Senha',key='edit_nova',type='password')
                        
                        st.button('Editar',key='btn_edit',type='primary')

                        pass

                    pass


                if st.session_state['cad_save']:
                    
                    if st.session_state['cad_email']=='' or st.session_state['cad_senha']=='' or st.session_state['cad_validar']=='' or st.session_state['cad_cnpj']=='':

                        mensagem=st.warning('Preencha os campos informados.')
                        time.sleep(1)
                        mensagem.empty()                        

                        pass


                    elif st.session_state['cad_senha']!=st.session_state['cad_validar']:

                        mensagem=st.warning('Senha não confere com a informada.')
                        time.sleep(1)
                        mensagem.empty()                         

                        pass

                    else:

                        cont=len(df.loc[(df['E-mail']==st.session_state['cad_email'])])

                        if cont<=0:

                            df.loc[len(df)]=[st.session_state['cad_email'],st.session_state['cad_senha'],st.session_state['cad_empresa']]

                            df.to_excel(temp_path,sheet_name='Acesso',index=False)

                            time.sleep(1)
                            streamlit_js_eval(js_expressions='parent.window.location.reload()')

                            st.rerun()
                            
                            pass

                        else:                       

                            mensagem=st.warning('Usuário já consta na base de dados.')
                            time.sleep(1)
                            mensagem.empty()

                            time.sleep(1)
                            streamlit_js_eval(js_expressions='parent.window.location.reload()')

                            pass                      

                        pass

                    pass

                if st.session_state['cad_exit']:
                    
                    temp_path=os.path.join(self.path_base,self.tela)
                    os.remove(temp_path)

                    st.empty()
                    st.rerun()

                    pass

                if st.session_state['btn_edit']:

                    if st.session_state['edit_nova']=='':

                        mensagem=st.warning('Informe a nova senha!')
                        time.sleep(1)
                        mensagem.empty()

                        pass

                    else:

                        df.loc[df['E-mail']==st.session_state['mult1'][-1],'Senha']=st.session_state['edit_nova']
                        df.to_excel(temp_path,index=False)

                        time.sleep(1)
                        streamlit_js_eval(js_expressions='parent.window.location.reload()')

                        pass

                    pass

                if st.session_state['btn_delete']:

                    self.msgDelete(df,temp_path)

                    pass

                pass

            pass

        pass

    
    @st.dialog(title='Deletar',width='small')
    def msgDelete(self,df:pd.DataFrame,path):

        divs=st.columns([1,4,1],vertical_alignment='center')

        with divs[1].container():

            st.subheader('Deseja remover o usuário do sistema')

            btns=st.columns(2,vertical_alignment='center')

            with btns[0].container():

                st.button('Sim',key='dialog_yes',type='primary',use_container_width=True)

                pass

            with btns[-1].container():

                st.button('Não',key='dialog_no',type='secondary',use_container_width=True)

                pass

            pass
        
        if st.session_state['dialog_yes']:

            index=df.loc[df['E-mail']==st.session_state['mult1'][-1]].index.max()
            df.drop(index=index,inplace=True)
            df.to_excel(path,index=False)

            st.rerun()

            pass

        if st.session_state['dialog_no']:
            
            st.rerun()

            pass

        pass


    pass