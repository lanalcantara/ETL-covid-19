# 📊 Projeto ETL COVID-19 – Aluno 3

Este projeto faz parte da atividade da disciplina, com foco em **Transformação de Saúde e Visualização**.  
Responsável: **Aluno 3**  

---

## ✅ Entregáveis

1. **Transformação de Saúde (Tema 2)**  
   - Base limpa gerada: `data/covid_transformado.csv`.

2. **Agregações Temporais/Geográficas (Tema 4)**  
   - Tabela final: `data/base_final_analise.csv`.

3. **Visualização (Tema 5)**  
   - Dashboard interativo desenvolvido em **Streamlit**: `scripts/app_dashboard.py`.

4. **Documentação Final (Tema 4)**  
   - Este `README.md` com instruções.  
   - Dicionário de Dados (abaixo).

---

## ⚙️ Como rodar o projeto

### 1. Criar e ativar ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
python data/data_transform.py

