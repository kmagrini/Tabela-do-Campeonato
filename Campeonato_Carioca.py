+import requests
+import pandas as pd
+import tkinter as tk
+from tkinter import scrolledtext, messagebox
+from bs4 import BeautifulSoup
+
+# Função para coletar dados
+def coletar_dados():
+    url = "https://ge.globo.com/rj/futebol/campeonato-carioca/"
+    response = requests.get(url)
+    if response.status_code != 200:
+        messagebox.showerror("Erro", "Falha ao coletar dados.")
+        return None
+    
+    soup = BeautifulSoup(response.text, 'html.parser')
+    # Aqui você deve ajustar a lógica para extrair os dados corretos
+    # Exemplo: encontrar a tabela de classificação
+    tabela = soup.find('table', class_='tabela-classificacao')
+    if not tabela:
+        messagebox.showerror("Erro", "Tabela de classificação não encontrada.")
+        return None
+    
+    classificacao = []
+    for linha in tabela.find_all('tr')[1:]:  # Ignora o cabeçalho
+        colunas = linha.find_all('td')
+        time = colunas[1].text.strip()  # Nome do time
+        pontos = int(colunas[2].text.strip())  # Pontos
+        classificacao.append({'Time': time, 'Pontos': pontos})
+    
+    return classificacao
+
+# Função para exibir resultados na interface
+def exibir_resultados():
+    dados = coletar_dados()
+    if dados:
+        df = pd.DataFrame(dados)
+        resultado_text.delete(1.0, tk.END)  # Limpa a área de texto
+        resultado_text.insert(tk.END, df.to_string(index=False))  # Insere os resultados
+
+# Configuração da interface
+app = tk.Tk()
+app.title("Classificação Campeonato Carioca 2025")
+
+# Botão para coletar dados
+botao_coletar = tk.Button(app, text="Coletar Dados", command=exibir_resultados)
+botao_coletar.pack(pady=10)
+
+# Área de texto para exibir resultados
+resultado_text = scrolledtext.ScrolledText(app, width=50, height=20)
+resultado_text.pack(pady=10)
+
+app.mainloop()
