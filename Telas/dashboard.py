import streamlit as st
import streamlit_shadcn_ui as ui
import os
from glob import glob
import pandas as pd
import time
from datetime import datetime
import DataBase.dataset
from Moeda import Moeda
import socket as s

class Dash:

    def __init__(self):

        self.IP=s.gethostbyname(s.gethostname())
        self.path_base=os.path.join(os.getcwd(),'PC',self.IP)
        os.makedirs(self.path_base,exist_ok=True)

        self.path_excel=os.path.join(os.getcwd(),'Notas')
        os.makedirs(self.path_excel,exist_ok=True)

        self.excel='notas.xlsx'

        pass


    def main(self):

        placeholder=st.empty()

        excel_df=pd.DataFrame(columns=['Data','Empresa','SKU','Produto','Unid CMP','Qtde','Destinatário'])
        stk_path=os.path.join(os.getcwd(),'Estoque')
        os.makedirs(stk_path,exist_ok=True)
        stk_path=os.path.join(stk_path,'estoque.xlsx')
        arq=glob(stk_path)

        if len(arq)>0:

            excel_df=pd.read_excel(stk_path)

            colunas=['Empresa','SKU']
            col_leach={'Qtde':'sum'}
            
            baixa_df=excel_df.loc[excel_df['Data'].dt.date<datetime.now().date()].groupby(colunas,as_index=False).agg(col_leach)
            baixa_df.rename(columns={'Qtde':'Saida'},inplace=True)
            pend_df=excel_df.loc[excel_df['Data'].dt.date==datetime.now().date()].groupby(colunas,as_index=False).agg(col_leach)
            pend_df.rename(columns={'Qtde':'Pendente'},inplace=True)            
            
            pass
        
        var_dict=dict()

        with placeholder.container():

            st.title('Dashboard')
            
            with st.sidebar:

                st.button('Atualizar',type='primary',use_container_width=True,key='btn_refresh')

                df=DataBase.dataset.dados()

                for c in ['Empresa','Nome Fantasia Destinatário','Produto']:

                    lista=df[c].unique().tolist()
                    st.multiselect(c,options=lista,key=c,placeholder='Escolha as opções')
                    df=df.loc[df[c].isin(st.session_state[c])] if len(st.session_state[c])>0 else df

                    pass
                 
                pass

            tab1,tab2=st.tabs(['Geral','Controle'])

            with tab1.container():

                with st.container():

                    cards=st.columns(4,vertical_alignment='center')

                    with cards[0]:

                        var_dict['xml']=len(df['Chave NFe'].unique().tolist())
                        ui.metric_card(title='Notas',content=Moeda.Numero(var_dict['xml']))

                        pass

                    with cards[1]:

                        var_dict['produtos']=len(df['SKU'].unique().tolist())
                        ui.metric_card(title='Produtos',content=Moeda.Numero(var_dict['produtos']))

                        pass

                    with cards[2]:

                        var_dict['peso']=df['Qtde'].sum()
                        ui.metric_card(title='peso',content=Moeda.FormatarMoeda(var_dict['peso']))

                        pass

                    with cards[-1]:

                        var_dict['total']=df['Total dos Produtos'].sum()
                        ui.metric_card(title='Total dos Produtos',content=f"R$ {Moeda.FormatarMoeda(var_dict['total'])}")

                        pass                                            

                    pass

                with st.container():

                    divs=st.columns(2,vertical_alignment='top')

                    with divs[0].container():

                        colunas=['Nome Fantasia Destinatário','Chave NFe']
                        col_leach={'Qtde':'sum','Total dos Produtos':'sum'}
                        temp_df=df.groupby(colunas,as_index=False).agg(col_leach)
                        col_leach[colunas[-1]]='count'
                        del colunas[-1]
                        temp_df=temp_df.groupby(colunas,as_index=False).agg(col_leach)

                        st.dataframe(temp_df,use_container_width=True,hide_index=True)

                        pass

                    with divs[-1].container():

                        colunas=['Empresa','Chave NFe']
                        col_leach={'Qtde':'sum','Total dos Produtos':'sum'}
                        temp_df=df.groupby(colunas,as_index=False).agg(col_leach)
                        col_leach[colunas[-1]]='count'
                        del colunas[-1]
                        temp_df=temp_df.groupby(colunas,as_index=False).agg(col_leach)                        

                        st.dataframe(temp_df,use_container_width=True,hide_index=True)

                        pass

                    colunas=['SKU','Produto','Unid CMP','Chave NFe']
                    col_leach={'Qtde':'sum','Total dos Produtos':'sum'}
                    temp_df=df.groupby(colunas,as_index=False).agg(col_leach)
                    col_leach[colunas[-1]]='count'
                    del colunas[-1]
                    temp_df=temp_df.groupby(colunas,as_index=False).agg(col_leach)
                    temp_df.sort_values('Qtde',ascending=False,ignore_index=True,inplace=True)

                    st.dataframe(temp_df,use_container_width=True,hide_index=True)            

                    pass
             
                st.dataframe(df,use_container_width=True,hide_index=True)

                pass

            with tab2.container():

                with st.container():

                    cols=st.columns([0.3,5,2,6],vertical_alignment='bottom')

                    with cols[0].container():

                        lista=df['NFe'].unique().tolist()
                        st.checkbox('Deletar',value=False,label_visibility='collapsed',key='check1')

                        pass                    

                    with cols[1].container():

                        lista=df['NFe'].unique().tolist()
                        max=1 if st.session_state['check1']==False else None
                        st.multiselect('Notas',options=lista,placeholder='Escolhas as notas',max_selections=max,key='mult2')

                        pass

                    with cols[2].container():

                        disabled=False if len(st.session_state['mult2'])>0 else True
                        st.button('Deletar',key='btn_delete',type='primary',disabled=disabled)

                        pass                    

                    pass

                with st.container():

                    lista=df.loc[df['NFe'].isin(st.session_state['mult2']),'Empresa'].unique().tolist() if len(st.session_state['mult2'])>0 else df['Empresa'].unique().tolist()
                    st.multiselect(label='Empresa',options=lista,key='mult3')

                    with st.expander('Produtos',expanded=True):
                        
                        colunas=['Empresa','SKU','Produto','Unid CMP']
                        col_leach={'Qtde':'sum'}
                        temp_df=df.loc[df['Empresa'].isin(st.session_state['mult3'])].groupby(colunas,as_index=False).agg(col_leach)
                        temp_df['Pendente']=0
                        temp_df['Saldo']=0

                        arq=glob(stk_path)
                        
                        if len(arq)>0:

                            temp_df=temp_df.merge(baixa_df,on=['Empresa','SKU'],how='left')
                            temp_df=temp_df.merge(pend_df,on=['Empresa','SKU'],how='left')
                            temp_df.fillna(0,inplace=True)
                            temp_df['Qtde']=temp_df.apply(lambda info: info['Qtde']-info['Saida'],axis=1)
                            temp_df.drop(columns=['Saida'],inplace=True)
                            temp_df['Saldo']=temp_df.apply(lambda info: info['Qtde']-info['Pendente'],axis=1)

                            pass

                        temp_df.sort_values('Qtde',ascending=False,ignore_index=True,inplace=True)

                        st.dataframe(temp_df,use_container_width=True,hide_index=True,column_config={

                            'Qtde':st.column_config.NumberColumn(
                                
                                'Estoque',
                                format='%.3f'
                            )
                        })

                        st.button('Editar',type='primary',key='btn_edit')

                        pass

                    pass

                pass

            pass

        if st.session_state['btn_refresh']:

            st.cache_data.clear()
            st.rerun()

            pass

        if st.session_state['btn_delete']:

            temp_path=os.path.join(self.path_excel,self.excel)
            self.msgDelete(st.session_state['mult2'],df,temp_path)

            pass

        if st.session_state['btn_edit']:

            self.dialogPed(temp_df,df,stk_path)

            pass

        pass

    @st.dialog('Aviso',width='small')
    def msgDelete(self,lista:list,df:pd.DataFrame,path):
        
        divs=st.columns([1,4,1],vertical_alignment='center')

        with divs[1].container():

            st.subheader('Deseja excluir a nota da plataforma?')

            temp_df=df.loc[df['NFe'].isin(lista)]
            destinatario=temp_df['Nome Fantasia Destinatário'].unique().tolist()
            st.multiselect('Destinatário',options=destinatario,key='multdialog1',placeholder='Escolha o Destinatário')

            btns=st.columns(2,vertical_alignment='center')

            with btns[0].container():

                st.button('Sim',key='btn_yes',type='primary',use_container_width=True)

                pass

            with btns[-1].container():

                st.button('Não',key='btn_no',type='secondary',use_container_width=True)

                pass          

            pass

        if st.session_state['btn_no']:

            st.rerun()

            pass


        if st.session_state['btn_yes']:

            if len(st.session_state['multdialog1'])<=0:

                mensagem=st.warning('Informe o destinatário!')
                time.sleep(1)
                mensagem.empty()

                pass

            else:

                xml=temp_df.loc[temp_df['Nome Fantasia Destinatário']==st.session_state['multdialog1'][-1],'Chave NFe'].unique().tolist()
                temp_path=os.path.join(os.getcwd(),'XML','*.xml*')
                arq_xml=glob(temp_path)

                for arq in arq_xml:

                    name=str(os.path.basename(arq))
                    name=''.join([l for l in name if str(l).isnumeric()])

                    if not name in xml:

                        continue

                    index=temp_df.loc[temp_df['Chave NFe']==name].index.values
                    df.drop(index=index,inplace=True)
                    df.to_excel(path,index=False)

                    os.remove(arq)

                    pass
                
                st.cache_data.clear()
                st.rerun()

                pass

            pass


        pass

    @st.dialog('Lançamento',width='large')
    def dialogPed(self,df:pd.DataFrame,base_df:pd.DataFrame,path):

        excel_df=pd.DataFrame(columns=['Data','Empresa','SKU','Produto','Unid CMP','Qtde','Destinatário'])
        temp_path=os.path.join(self.path_base,'temp.xlsx')
        arq=glob(temp_path)

        if len(arq)>0:

            excel_df=pd.read_excel(temp_path)

            pass

        with st.container():

            lista=df['Produto'].unique().tolist()
            lista.insert(0,None)
            st.selectbox('Produto',options=lista,key='select1',placeholder='Escolha os produtos')

            with st.container():

                divs=st.columns([2,2,6],vertical_alignment='bottom')

                if st.session_state['select1']==None:

                    with divs[0].container():

                        st.number_input(label='SKU',key='dialog_sku',disabled=True)
                        
                        pass

                    with divs[1].container():

                        st.text_input(label='Unid CMP',key='dialog_unid',disabled=True)

                        pass

                    with divs[-1].container():

                        lista=base_df['Nome Fantasia Destinatário'].unique().tolist() if st.session_state['select1']!=None else []
                        st.selectbox(label='Destinatário',key='dialog_dest',options=lista,placeholder='Escolha as opções')

                        pass                    

                    pass

                else:

                    with divs[0].container():

                        var=df.loc[df['Produto']==st.session_state['select1'],'SKU'].max()
                        st.number_input(label='SKU',key='dialog_sku',disabled=True,value=var)

                        pass

                    with divs[1].container():

                        var=df.loc[df['Produto']==st.session_state['select1'],'Unid CMP'].unique().tolist()[-1]
                        st.text_input(label='Unid CMP',key='dialog_unid',value=var,disabled=True)

                        pass

                    with divs[-1].container():

                        lista=base_df['Nome Fantasia Destinatário'].unique().tolist() if st.session_state['select1']!=None else []
                        st.selectbox(label='Destinatário',key='dialog_dest',options=lista,placeholder='Escolha as opções')

                        pass                    

                    pass                

                pass

            divs=st.columns([2,2,2,3,6],vertical_alignment='bottom')

            with divs[0].container():

                var=df.loc[df['Produto']==st.session_state['select1'],'Qtde'].sum()-df.loc[df['Produto']==st.session_state['select1'],'Pendente'].sum() if st.session_state['select1']!=None else 0.00
                st.number_input('Estoque',key='qtde_stk',value=var,disabled=True,format='%.2f')

                pass

            with divs[1].container():

                st.number_input('Qtde',key='qtde_pend',min_value=0.00,format='%.2f')

                pass

            with divs[2].container():

                var=st.session_state['qtde_stk']-st.session_state['qtde_pend']
                st.number_input('Saldo',key='qtde_saldo',value=var,format='%.2f',disabled=True)

                pass

            with divs[3].container():

                st.button('Adicionar',key='btn_add')

                pass
            
            with st.expander('Lista'):

                st.dataframe(excel_df,use_container_width=True,hide_index=True)

                pass

            st.button('Salvar',key='dialog_save',type='primary')           

            if st.session_state['btn_add']:

                if st.session_state['select1']==None or st.session_state['dialog_dest']==None:

                    mensagem=st.warning('Preencha os campos.')
                    time.sleep(1)
                    mensagem.empty()

                    pass

                elif st.session_state['qtde_stk']<0:

                    mensagem=st.warning('Saldo insuficiente.')
                    time.sleep(1)
                    mensagem.empty()

                    pass

                else:

                    empresa=df['Empresa'].unique().tolist()[-1]
                    excel_df.loc[len(excel_df)]=[datetime.now().date(),empresa,st.session_state['dialog_sku'],st.session_state['select1'],st.session_state['dialog_unid'],st.session_state['qtde_pend'],st.session_state['dialog_dest']]
                    temp_path=os.path.join(self.path_base,'temp.xlsx')
                    excel_df.to_excel(temp_path,index=False)

                    pass

                pass

            if st.session_state['dialog_save']:
                
                arq=glob(path)
                temp_df=pd.DataFrame(columns=['Data','Empresa','SKU','Produto','Unid CMP','Qtde','Destinatário'])

                if len(arq)>0:

                    temp_df=pd.read_excel(path)

                    pass

                temp_df=pd.concat([temp_df,excel_df],axis=0,ignore_index=True)
                temp_df.to_excel(path,index=False)                

                os.remove(temp_path)
                st.rerun()

                pass 

            pass

        pass

    pass