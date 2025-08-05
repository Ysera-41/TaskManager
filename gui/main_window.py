import tkinter as tk
from tkinter import messagebox
from app.models import insert_task, get_tasks, update_task, delete_task

def start_gui():
    def add_task():
        desc = entry_desc.get()
        cat = var_categoria.get()
        if not desc.strip():
            messagebox.showwarning("Erro", "Descrição não pode ser vazia.")
            return
        insert_task(desc, cat)
        entry_desc.delete(0, tk.END)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Task adicionada!")

    def atualizar_lista():
        listbox_tasks.delete(0, tk.END)
        for task_id, task_desc in get_tasks():
            listbox_tasks.insert(tk.END, f"{task_id} - {task_desc}")

    def atualizar_task():
        selected = listbox_tasks.curselection()
        if not selected:
            messagebox.showwarning("Seleção", "Selecione uma task.")
            return
        task_text = listbox_tasks.get(selected[0])
        task_id = int(task_text.split(" - ")[0])
        nova_desc = entry_desc.get()
        if not nova_desc.strip():
            messagebox.showwarning("Erro", "Descrição não pode ser vazia.")
            return
        update_task(task_id, nova_desc)
        entry_desc.delete(0, tk.END)
        atualizar_lista()
        messagebox.showinfo("Atualizado", "Task atualizada!")

    def excluir_task():
        selected = listbox_tasks.curselection()
        if not selected:
            messagebox.showwarning("Seleção", "Selecione uma task.")
            return
        task_text = listbox_tasks.get(selected[0])
        task_id = int(task_text.split(" - ")[0])
        delete_task(task_id)
        atualizar_lista()
        messagebox.showinfo("Deletado", "Task excluída!")

    # Janela principal
    root = tk.Tk()
    root.title("Task Manager")
    root.geometry("400x400")

    # Campo de entrada
    tk.Label(root, text="Descrição da Task:").pack()
    entry_desc = tk.Entry(root, width=50)
    entry_desc.pack(pady=5)

    tk.Label(root, text="Categoria:").pack()
    var_categoria = tk.StringVar(root)
    var_categoria.set("1")  # padrão
    categorias = {"1": "Trabalho", "2": "Estudo", "3": "Entretenimento"}
    drop = tk.OptionMenu(root, var_categoria, *categorias.values())

    drop.pack(pady=5)

    # Botões de ação
    tk.Button(root, text="Adicionar Task", command=add_task).pack(pady=5)
    tk.Button(root, text="Atualizar Task Selecionada", command=atualizar_task).pack(pady=5)
    tk.Button(root, text="Excluir Task Selecionada", command=excluir_task).pack(pady=5)

    # Listagem
    tk.Label(root, text="Lista de Tasks:").pack(pady=5)
    listbox_tasks = tk.Listbox(root, width=50, height=10)
    listbox_tasks.pack()

    atualizar_lista()
    root.mainloop()
