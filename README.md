# Projeto Integrador: Análise de Dados em Python (ADS)

**Integrantes da Equipe:**
- Gilmar Vitor Soares de Oliveira - Matrícula: 2025.15.1436
- Josué Teixeira Ferreira Filho - Matrícula: 2026.15.178

---

## 🗂️ Sobre o Dataset Escolhido

- **Tema Geral:** Vendas de Varejo e E-commerce Corporativo (Superstore Sales Analytics).
- **Fonte de Dados (URL):** https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting (ou https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- **Motivação:** Esses dados representam o histórico real de transações comerciais de uma grande rede de varejo, detalhando vendas, lucros, descontos, clientes e regiões geográficas. Nossa motivação foi analisar a evolução do faturamento ao longo dos anos, identificar quais categorias de produtos sustentam o negócio e diagnosticar como descontos excessivos afetam a margem de lucro das operações.

---

## 🏗️ Arquitetura e Estruturação (O que vocês codaram)

- **Módulos / Classes Criadas:** No arquivo `src/analisador.py`, construímos a classe `AnalisadorDeDados`. Ela é o núcleo orientado a objetos do sistema e gerencia a importação do CSV com Pandas, a rotina de saneamento no construtor `__init__`, os métodos analíticos encapsulados (médias, totais, margens e agrupamentos via `.groupby()`) e a geração dos dashboards visuais com Matplotlib e Seaborn. No arquivo `main.py`, implementamos o Ponto de Entrada contendo o Menu Interativo em laço `while True` e tratamento robusto de exceções (`try/except`).
- **Limpeza de Dados:** A base continha registros duplicados e linhas com campos vazios/nulos em variáveis essenciais como vendas e lucros. No método de limpeza, aplicamos a técnica do `.drop_duplicates()` para eliminar compras repetidas e `.dropna()` para descartar registros nulos. Além disso, utilizamos `pd.to_datetime()` para formatar as datas e criamos o campo `Ano_Mes` devidamente ordenado em ordem cronológica para que as análises temporais não sofressem distorções.

---

## 📊 Gráficos Desenvolvidos

Descreva detalhadamente as 3 visualizações construídas:

1. **Visão 1 (Gráfico de Linha):** Apresenta a evolução temporal do faturamento mensal ao longo dos anos (2021 a 2024), traçando a linha de vendas em ordem cronológica rigorosa, permitindo enxergar a sazonalidade, períodos de crescimento e picos de receita da loja.
2. **Visão 2 (Gráfico de Barras):** Compara o faturamento total acumulado entre as três grandes categorias de produtos (Tecnologia, Móveis e Suprimentos de Escritório), exibindo os valores numéricos em reais acima de cada coluna, comprovando a liderança expressiva do setor de Tecnologia.
3. **Visão 3 (Histograma):** Apresenta a distribuição de frequência do valor das transações (ticket por pedido), evidenciando que a grande maioria das compras se concentra na faixa de até R$ 3.000,00, enquanto compras de maior vulto financeiro formam uma cauda longa de aquisições corporativas.
*(Bônus - Visão 4 - Dispersão):* Demonstra a correlação entre faturamento e lucratividade por pedido, sinalizando em verde as transações lucrativas e em vermelho as vendas que geraram prejuízo decorrente de descontos agressivos.

---

## 📁 Estrutura de Arquivos do Repositório

```text
projeto-integrador-python/
│
├── data/                   # Coloque aqui o arquivo .csv baixado do Kaggle.
│   ├── .gitkeep            # Mantém a pasta visível no GitHub. Não apague.
│   └── superstore_sales.csv# Base de dados real do Kaggle utilizada.
│
├── src/                    # Pasta raiz do núcleo do sistema (Orientação a Objetos).
│   ├── __init__.py         # Indica ao Python que a pasta "src" é um módulo importável.
│   └── analisador.py       # Aqui vocês devem construir a Classe AnalisadorDeDados.
│                           # Toda a lógica de limpeza (Pandas) e gráficos fica aqui!
│
├── graficos/               # Pasta de saída contendo as imagens (.png) dos dashboards.
│   ├── grafico_1_linha_evolucao.png
│   ├── grafico_2_barras_categorias.png
│   ├── grafico_3_histograma_vendas.png
│   └── grafico_4_dispersao_vendas_lucro.png
│
├── tests/                  # Suíte de testes automatizados da aplicação.
│   └── test_analisador.py
│
├── main.py                 # O Ponto de Entrada. É aqui que o laço 'while' do Menu Interativo roda.
├── requirements.txt        # Lista de bibliotecas externas obrigatórias do projeto.
├── .gitignore              # Configurado para não subir lixo de compilação (ex: __pycache__).
└── README.md               # Este arquivo com o formulário devidamente preenchido.
```

---

## 🚀 Como Instalar e Rodar o Projeto

1. **Instalar dependências obrigatórias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar o Menu Interativo no Terminal**:
   ```bash
   python main.py
   ```

3. **Executar a Suíte de Testes Unitários**:
   ```bash
   python -m unittest discover -s tests -v
   ```
