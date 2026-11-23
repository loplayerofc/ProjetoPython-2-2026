"""
Projeto Integrador Python - Análise e Desenvolvimento de Sistemas (ADS)
Arquivo: src/analisador.py
Classe: AnalisadorDeDados

Integrantes:
- Gilmar Vitor Soares de Oliveira - Matrícula: 2025.15.1436
- Josué Teixeira Ferreira Filho - Matrícula: 2026.15.178
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class AnalisadorDeDados:
    """
    Classe responsável pela leitura, limpeza técnica dos dados e geração
    dos relatórios e gráficos estatísticos para tomada de decisão.
    """

    def __init__(self, caminho_csv='data/superstore_sales.csv'):
        """
        Construtor da Classe:
        Importa o arquivo CSV com Pandas e aplica a rotina técnica de limpeza.
        """
        self.caminho_csv = caminho_csv

        # Valida se o arquivo realmente existe na pasta data/
        if not os.path.exists(caminho_csv):
            raise FileNotFoundError(f"Arquivo CSV não encontrado: {caminho_csv}")

        print("\n[INICIANDO PIPELINE] Carregando a base de dados do Kaggle...")
        self.df_bruto = pd.read_csv(self.caminho_csv)
        self.total_bruto = self.df_bruto.shape[0]

        # Executa a limpeza técnica obrigatória dos dados
        self._limpar_dados()

    def _limpar_dados(self):
        """
        Rotina técnica de limpeza dos dados:
        - .drop_duplicates(): remove registros repetidos.
        - .dropna(): remove linhas com valores faltantes/nulos.
        - pd.to_datetime(): converte colunas de data e ordena cronologicamente.
        """
        # 1. Remoção de duplicatas
        df_sem_duplicadas = self.df_bruto.drop_duplicates()
        self.duplicatas_removidas = self.total_bruto - df_sem_duplicadas.shape[0]

        # 2. Remoção de dados nulos
        df_limpo = df_sem_duplicadas.dropna()
        self.nulos_removidos = df_sem_duplicadas.shape[0] - df_limpo.shape[0]

        # 3. Conversão de datas e criação de períodos
        df_limpo['Order_Date'] = pd.to_datetime(df_limpo['Order_Date'])
        df_limpo['Ship_Date'] = pd.to_datetime(df_limpo['Ship_Date'])
        df_limpo['Ano_Mes'] = df_limpo['Order_Date'].dt.to_period('M')
        df_limpo['Ano'] = df_limpo['Order_Date'].dt.year

        self.df = df_limpo
        self.total_limpo = self.df.shape[0]

        print(f"[STATUS DA LIMPEZA]")
        print(f" -> Registros originais lidos : {self.total_bruto}")
        print(f" -> Linhas duplicadas removidas: {self.duplicatas_removidas}")
        print(f" -> Linhas nulas descartadas   : {self.nulos_removidos}")
        print(f" -> Registros finais prontos   : {self.total_limpo}\n")

    # ==============================================================
    # MÉTODOS ANALÍTICOS (ORIENTAÇÃO A OBJETOS)
    # ==============================================================

    def relatorio_limpeza(self):
        """Retorna o resumo da limpeza técnica da base de dados."""
        return {
            "arquivo": self.caminho_csv,
            "brutos": self.total_bruto,
            "duplicatas": self.duplicatas_removidas,
            "nulos": self.nulos_removidos,
            "limpos": self.total_limpo,
            "colunas": len(self.df.columns),
            "data_inicial": str(self.df['Order_Date'].min()),
            "data_final": str(self.df['Order_Date'].max())
        }

    def calcular_resumo_geral(self):
        """Calcula os totais e as principais métricas do negócio."""
        faturamento = self.df['Sales'].sum()
        lucro = self.df['Profit'].sum()
        margem = (lucro / faturamento * 100) if faturamento > 0 else 0.0
        ticket_medio = self.df['Sales'].mean()
        quantidade = self.df['Quantity'].sum()
        total_pedidos = self.df['Order_ID'].nunique()
        total_clientes = self.df['Customer_ID'].nunique()

        return {
            "faturamento": faturamento,
            "lucro": lucro,
            "margem_percentual": margem,
            "ticket_medio": ticket_medio,
            "quantidade_itens": quantidade,
            "total_pedidos": total_pedidos,
            "total_clientes": total_clientes
        }

    def vendas_por_categoria(self):
        """Agrupa faturamento e lucro por Categoria com .groupby()."""
        resultado = self.df.groupby('Category').agg({
            'Sales': ['sum', 'mean'],
            'Profit': ['sum', 'mean'],
            'Quantity': 'sum'
        })
        return resultado

    def vendas_por_regiao(self):
        """Agrupa vendas e lucratividade por Região com .groupby()."""
        resultado = self.df.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        })
        return resultado

    def evolucao_mensal(self):
        """Agrupa o faturamento por Ano-Mês em ordem cronológica."""
        resultado = self.df.groupby('Ano_Mes').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        })
        return resultado

    def filtrar_categoria(self, categoria_desejada):
        """Filtra a base de dados por uma categoria específica."""
        filtro = (self.df['Category'].str.lower() == categoria_desejada.lower().strip())
        df_filtrado = self.df[filtro]
        return df_filtrado

    def top_produtos(self, quantidade=10):
        """Retorna os produtos mais vendidos usando .sort_values()."""
        ordenado = self.df.sort_values(by='Sales', ascending=False)
        return ordenado.head(quantidade)

    def estatisticas_descritivas(self):
        """Gera o resumo estatístico numérico com .describe()."""
        colunas = ['Sales', 'Quantity', 'Discount', 'Profit']
        return self.df[colunas].describe()

    # ==============================================================
    # MÉTODOS VISUAIS (MATPLOTLIB & SEABORN COM LETRAS LEGÍVEIS)
    # ==============================================================

    def grafico_linha_evolucao(self, caminho_salvar='graficos/grafico_1_linha_evolucao.png'):
        """
        Visão 1: Gráfico de Linha
        Evolução temporal do faturamento mensal ao longo dos anos (ordem cronológica).
        Exige plt.title, plt.xlabel e plt.ylabel.
        """
        os.makedirs(os.path.dirname(caminho_salvar), exist_ok=True)
        sns.set_theme(style='whitegrid')

        tabela_mensal = self.evolucao_mensal()
        meses = tabela_mensal['Ano_Mes'].tolist()
        vendas = tabela_mensal['Sales_sum'].tolist() if 'Sales_sum' in tabela_mensal.columns else tabela_mensal['Sales'].tolist()

        plt.figure(figsize=(11, 6))
        plt.plot(meses, vendas, color='#2563eb', marker='o', linewidth=2.5, label='Faturamento')
        plt.title('Evolução Temporal do Faturamento Mensal (Superstore Sales)')
        plt.xlabel('Período (Ano-Mês)')
        plt.ylabel('Faturamento Total (R$)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(caminho_salvar)
        plt.show()
        plt.close()

    def grafico_barras_categoria(self, caminho_salvar='graficos/grafico_2_barras_categorias.png'):
        """
        Visão 2: Gráfico de Barras
        Comparação de faturamento entre as categorias de produtos.
        Exige plt.title, plt.xlabel e plt.ylabel.
        """
        os.makedirs(os.path.dirname(caminho_salvar), exist_ok=True)
        sns.set_theme(style='whitegrid')

        dados_categoria = self.df.groupby('Category')
        soma_vendas = dados_categoria['Sales'].sum()
        nomes_categorias = soma_vendas.index
        valores_vendas = soma_vendas.values

        plt.figure(figsize=(10, 6))
        plt.bar(nomes_categorias, valores_vendas, color='#16a34a', width=0.55, label='Faturamento')
        plt.title('Faturamento Total por Categoria de Produto')
        plt.xlabel('Categoria de Produto')
        plt.ylabel('Faturamento Total (R$)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(caminho_salvar)
        plt.show()
        plt.close()

    def grafico_histograma_vendas(self, caminho_salvar='graficos/grafico_3_histograma_vendas.png'):
        """
        Visão 3: Histograma
        Distribuição de frequência dos valores das vendas (ticket por pedido).
        Exige plt.title, plt.xlabel e plt.ylabel.
        """
        os.makedirs(os.path.dirname(caminho_salvar), exist_ok=True)
        sns.set_theme(style='whitegrid')

        valores_vendas = self.df['Sales'].tolist()

        plt.figure(figsize=(10, 6))
        plt.hist(valores_vendas, bins=10, color='#0891b2', edgecolor='black', label='Frequência de Vendas')
        plt.title('Distribuição de Frequência do Valor das Vendas (Ticket)')
        plt.xlabel('Faixa de Valor da Venda (R$)')
        plt.ylabel('Quantidade de Pedidos')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(caminho_salvar)
        plt.show()
        plt.close()

    def grafico_dispersao_vendas_lucro(self, caminho_salvar='graficos/grafico_4_dispersao_vendas_lucro.png'):
        """
        Visão Bônus: Dispersão (Scatter Plot)
        Relação entre faturamento e lucratividade por pedido.
        Exige plt.title, plt.xlabel e plt.ylabel.
        """
        os.makedirs(os.path.dirname(caminho_salvar), exist_ok=True)
        sns.set_theme(style='whitegrid')

        vendas = self.df['Sales'].tolist()
        lucros = self.df['Profit'].tolist()

        plt.figure(figsize=(10, 6))
        plt.scatter(vendas, lucros, color='#9333ea', alpha=0.7, label='Pedidos')
        plt.title('Relação entre Faturamento e Lucro por Venda')
        plt.xlabel('Faturamento da Venda (R$)')
        plt.ylabel('Lucro Líquido (R$)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(caminho_salvar)
        plt.show()
        plt.close()

    def gerar_todos_graficos(self):
        """Gera e salva todos os gráficos na pasta graficos/."""
        print("\n[DASHBOARDS] Gerando e salvando todos os gráficos...")
        self.grafico_linha_evolucao()
        self.grafico_barras_categoria()
        self.grafico_histograma_vendas()
        self.grafico_dispersao_vendas_lucro()
        print("[SUCESSO] Todos os gráficos foram salvos na pasta 'graficos/' com sucesso!\n")


# Alias para compatibilidade
AnalisadorVendas = AnalisadorDeDados
