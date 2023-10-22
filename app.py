import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import sqlite3
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import csv

def submit_resume():
    
    nome = entry_nome.get()
    idade = entry_idade.get()
    email = entry_email.get()
    cidade = entry_cidade.get()
    estado = entry_estado.get()
    telefone = entry_telefone.get()
    linkedin = entry_linkedin.get()
    status = status_var.get()
    habilidades_interpessoais = text1.get("1.0", "end-1c")
    habilidades_tecnicas = text2.get("1.0", "end-1c")
    curriculo = curriculo_var.get()
    expectativa_salarial = expectativa_var.get()

    if not nome or not email or not cidade or not estado or not telefone or not linkedin or not curriculo:
        messagebox.showerror("Erro", "Preencha os campos obrigatórios: Nome, Email, Cidade, Estado, Telefone, Linkedin e Curriculo.")
        return

    conn = sqlite3.connect("formulario.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS formulario (
            nome TEXT,
            idade INTEGER,
            email TEXT,
            cidade TEXT,
            estado TEXT,
            telefone TEXT,
            linkedin TEXT,
            status TEXT,
            habilidades_interpessoais TEXT,
            habilidades_tecnicas TEXT,
            curriculo TEXT,
            expectativa_salarial TEXT
        )
    ''')
    conn.commit()

    cursor.execute('''
        INSERT INTO formulario
        (nome, idade, email, cidade, estado, telefone, linkedin, status, habilidades_interpessoais, habilidades_tecnicas, curriculo, expectativa_salarial)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, idade, email, cidade, estado, telefone, linkedin, status, habilidades_interpessoais, habilidades_tecnicas, curriculo, expectativa_salarial))
    conn.commit()
    conn.close()

    clear_form()

    result_label.config(text="Formulário enviado com sucesso!")

def attach_resume():
    file_path = filedialog.askopenfilename(
        filetypes=[("Arquivos PDF e Word", "*.pdf *.docx"), ("Todos os arquivos", "*")]
    )
    if file_path:
        curriculo_var.set(file_path)
        result_label.config(text=f"Anexo de currículo: {file_path}")

def export_candidates_to_csv(candidates):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivo CSV", "*.csv")])

    if file_path:
        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Nome", "Idade", "Email", "Cidade", "Estado", "Telefone", "LinkedIn", "Status", "Habilidades Interpessoais", "Habilidades Técnicas", "Curriculo", "Expectativa Salarial"])
            for candidate in candidates:
                csvwriter.writerow(candidate)

        result_label.config(text=f"Lista de candidatos exportada para {file_path}")

def open_recruiter_area():
    recrutador_janela = tk.Toplevel()
    recrutador_janela.title("Área do Recrutador")

    candidates = get_candidates()
    display_candidates(recrutador_janela, candidates)

    ttk.Button(recrutador_janela, text="Exportar para CSV", command=lambda: export_candidates_to_csv(candidates)).pack()

def get_candidates():
    conn = sqlite3.connect("formulario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM formulario")
    candidates = cursor.fetchall()
    conn.close()
    return candidates

tree = None 

def display_candidates(recrutador_janela, candidates):
    global tree 
    ttk.Label(recrutador_janela, text="").pack()

    filter_frame = ttk.Frame(recrutador_janela)
    filter_frame.pack()

    ttk.Label(filter_frame, text="Cidade:").grid(row=0, column=0, padx=5)
    filter_cidade = ttk.Combobox(filter_frame, values=[""] + list(set(candidate[3] for candidate in candidates)))
    filter_cidade.grid(row=0, column=1, padx=5)

    ttk.Label(filter_frame, text="Estado:").grid(row=0, column=2, padx=5)
    filter_estado = ttk.Combobox(filter_frame, values=[""] + list(set(candidate[4] for candidate in candidates)))
    filter_estado.grid(row=0, column=3, padx=5)

    ttk.Label(filter_frame, text="Expectativa Salarial:").grid(row=0, column=4, padx=5)
    filter_salario = ttk.Combobox(filter_frame, values=[""] + list(set(candidate[11] for candidate in candidates)))
    filter_salario.grid(row=0, column=5, padx=5)

    ttk.Label(filter_frame, text="Email:").grid(row=0, column=6, padx=5)
    filter_email = ttk.Entry(filter_frame)
    filter_email.grid(row=0, column=7, padx=5)

    ttk.Label(filter_frame, text="Telefone:").grid(row=0, column=8, padx=5)
    filter_telefone = ttk.Entry(filter_frame)
    filter_telefone.grid(row=0, column=9, padx=5)

    ttk.Button(filter_frame, text="Filtrar", command=lambda: filter_candidates(candidates, filter_cidade.get(), filter_estado.get(), filter_salario.get(), filter_email.get(), filter_telefone.get())).grid(row=0, column=10, padx=10)

    ttk.Label(recrutador_janela, text="Lista de Candidatos:").pack()
    tree = ttk.Treeview(recrutador_janela, columns=("Nome", "Cidade", "Estado", "Expectativa Salarial", "Email", "Telefone", "Status"))
    tree.heading("#1", text="Nome")
    tree.heading("#2", text="Cidade")
    tree.heading("#3", text="Estado")
    tree.heading("#4", text="Expectativa Salarial")
    tree.heading("#5", text="Email")
    tree.heading("#6", text="Telefone")
    tree.heading("#7", text="Status")

    tree.tag_configure("aprovado", background="green", foreground="black")
    tree.tag_configure("reprovado", background="red", foreground="white")
    tree.tag_configure("em_espera", background="yellow", foreground="black")

    tree.pack()

    for candidate in candidates:
        status = candidate[7]
        tag = ""
        if status == "Aprovado":
            tag = "aprovado"
        elif status == "Reprovado":
            tag = "reprovado"
        elif status == "Em espera":
            tag = "em_espera"

        tree.insert("", "end", values=(candidate[0], candidate[3], candidate[4], candidate[11], candidate[2], candidate[5], status), tags=(tag))

def filter_candidates(candidates, cidade, estado, salario, email, telefone):
    global tree 
    filtered_candidates = [candidate for candidate in candidates if
                           (not cidade or candidate[3] == cidade) and
                           (not estado or candidate[4] == estado) and
                           (not salario or candidate[11] == salario) and
                           (not email or email.lower() in candidate[2].lower()) and
                           (not telefone or telefone in candidate[5])]

    for item in tree.get_children():
        tree.delete(item)

    for candidate in filtered_candidates:
        status = candidate[7]
        tag = ""
        if status == "Aprovado":
            tag = "aprovado"
        elif status == "Reprovado":
            tag = "reprovado"
        elif status == "Em espera":
            tag = "em_espera"

        tree.insert("", "end", values=(candidate[0], candidate[3], candidate[4], candidate[11], candidate[2], candidate[5], candidate[7]), tags=(tag))

def clear_form():
    entry_nome.delete(0, "end")
    entry_idade.delete(0, "end")
    entry_email.delete(0, "end")
    entry_cidade.delete(0, "end")
    entry_estado.delete(0, "end")
    entry_telefone.delete(0, "end")
    entry_linkedin.delete(0, "end")
    status_var.set("")
    text1.delete("1.0", "end")
    text2.delete("1.0", "end")
    curriculo_var.set("")
    expectativa_var.set("Selecione...")

app = tk.Tk()
app.geometry("900x600")
app.title("Formulário de Inscrição")

style = Style(theme="flatly")

frame = ttk.Frame(app)
frame.pack(side="left", padx=20, pady=20, fill="y")

ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
entry_nome = ttk.Entry(frame)
entry_nome.grid(row=0, column=1)

ttk.Label(frame, text="Idade:").grid(row=1, column=0, sticky="w")
entry_idade = ttk.Entry(frame)
entry_idade.grid(row=1, column=1)

ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w")
entry_email = ttk.Entry(frame)
entry_email.grid(row=2, column=1)

ttk.Label(frame, text="Cidade:").grid(row=3, column=0, sticky="w")
entry_cidade = ttk.Entry(frame)
entry_cidade.grid(row=3, column=1)

ttk.Label(frame, text="Estado:").grid(row=4, column=0, sticky="w")
entry_estado = ttk.Entry(frame)
entry_estado.grid(row=4, column=1)

ttk.Label(frame, text="Telefone:").grid(row=5, column=0, sticky="w")
entry_telefone = ttk.Entry(frame)
entry_telefone.grid(row=5, column=1)

ttk.Label(frame, text="LinkedIn:").grid(row=6, column=0, sticky="w")
entry_linkedin = ttk.Entry(frame)
entry_linkedin.grid(row=6, column=1)

ttk.Label(frame, text="Status Atual:").grid(row=7, column=0, sticky="w")
status_var = tk.StringVar()
ttk.Radiobutton(frame, text="Empregado", variable=status_var, value="Empregado").grid(row=7, column=1, sticky="w")
ttk.Radiobutton(frame, text="Desempregado", variable=status_var, value="Desempregado").grid(row=7, column=2, sticky="w")

ttk.Label(frame, text="Habilidades Interpessoais:").grid(row=8, column=0, columnspan=3, sticky="w")
text1 = tk.Text(frame, wrap="word", height=4, width=40)
text1.grid(row=9, column=0, columnspan=3)

ttk.Label(frame, text="Habilidades Técnicas:").grid(row=10, column=0, columnspan=3, sticky="w")
text2 = tk.Text(frame, wrap="word", height=4, width=40)
text2.grid(row=11, column=0, columnspan=3)

ttk.Label(frame, text="Currículo Anexado:").grid(row=12, column=0, sticky="w")
curriculo_var = tk.StringVar()
curriculo_label = ttk.Label(frame, textvariable=curriculo_var, wraplength=300)
curriculo_label.grid(row=12, column=1, columnspan=2)

attach_button = ttk.Button(frame, text="Anexar Currículo", command=attach_resume)
attach_button.grid(row=13, column=0, columnspan=3, pady=10)

ttk.Label(frame, text="Expectativa Salarial:").grid(row=14, column=0, sticky="w")
salary_options = ["Selecione...", "R$2,000", "R$3,000", "R$4,000", "R$5,000", "R$6,000", "R$7,000", "R$8,000", "R$9,000", "R$10,000"]
expectativa_var = ttk.Combobox(frame, values=salary_options)
expectativa_var.grid(row=14, column=1)
expectativa_var.set("Selecione...")

submit_button = ttk.Button(frame, text="Enviar Formulário", command=submit_resume)
submit_button.grid(row=15, column=0, columnspan=3, pady=10)

clear_button = ttk.Button(frame, text="Limpar Formulário", command=clear_form)
clear_button.grid(row=16, column=0, columnspan=3, pady=10)

recruiter_button = ttk.Button(frame, text="Área do Recrutador", command=open_recruiter_area)
recruiter_button.grid(row=17, column=0, columnspan=3)

recruiter_label = ttk.Label(frame, text="Área do Recrutador")
recruiter_label.grid(row=18, column=0, columnspan=3)

result_label = ttk.Label(frame, text="", wraplength=300)
result_label.grid(row=19, column=0, columnspan=3)

imagem = Image.open("work.png")
imagem = imagem.resize((550, 500))
imagem = ImageTk.PhotoImage(imagem)

image_label = ttk.Label(app, image=imagem)
image_label.pack(side="right", padx=20, pady=20)

app.mainloop()
