import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit,
    QFrame, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from app.models import insert_task, get_tasks, update_status_task, delete_task
from .task_widget import TaskWidget


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jira 2 o inimigo agora é outro")
        self.setGeometry(100, 100, 900, 650)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
            QLabelFrame {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Formulário de nova task
        self.setup_form(layout)
        
        # Área do Kanban
        self.setup_kanban(layout)
        
        # Atualiza o kanban inicial
        self.atualizar_kanban()
    
    def setup_form(self, parent_layout):
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #ecf0f1; padding: 10px; border-radius: 5px;")
        form_layout = QVBoxLayout()
        form_frame.setLayout(form_layout)
        
        # Descrição
        lbl_desc = QLabel("Descrição:")
        self.entry_desc = QLineEdit()
        self.entry_desc.setPlaceholderText("Digite a descrição da tarefa...")
        form_layout.addWidget(lbl_desc)
        form_layout.addWidget(self.entry_desc)
        
        # Categoria e Data
        info_layout = QHBoxLayout()
        
        lbl_cat = QLabel("Categoria:")
        self.combo_cat = QComboBox()
        self.combo_cat.addItems(["Trabalho", "Estudo", "Entretenimento"])
        info_layout.addWidget(lbl_cat)
        info_layout.addWidget(self.combo_cat)
        
        lbl_date = QLabel("Data de Vencimento:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        info_layout.addWidget(lbl_date)
        info_layout.addWidget(self.date_edit)
        
        form_layout.addLayout(info_layout)
        
        # Botão Adicionar
        self.btn_add = QPushButton("Adicionar Task")
        self.btn_add.setStyleSheet("background-color: #2ecc71;")
        self.btn_add.clicked.connect(self.add_task)
        form_layout.addWidget(self.btn_add)
        
        parent_layout.addWidget(form_frame)
    
    def setup_kanban(self, parent_layout):
        kanban_frame = QFrame()
        kanban_layout = QHBoxLayout()
        kanban_frame.setLayout(kanban_layout)
        
        self.columns = {
            "AF": self.create_column("A Fazer"),
            "EP": self.create_column("Em Progresso"),
            "CO": self.create_column("Concluídas")
        }
        
        for column in self.columns.values():
            kanban_layout.addWidget(column)
        
        parent_layout.addWidget(kanban_frame)
    
    def create_column(self, title):
        column = QFrame()
        column.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        column.setLayout(layout)
        
        lbl_title = QLabel(title)
        lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        column.scroll_layout = scroll_layout
        return column
    
    def add_task(self):
        desc = self.entry_desc.text().strip()
        cat = self.combo_cat.currentText()
        dt_venc = self.date_edit.date().toString("yyyy-MM-dd")
        
        if not desc:
            QMessageBox.warning(self, "Erro", "Descrição não pode ser vazia.")
            return
        
        insert_task(desc, cat, dt_venc)
        self.entry_desc.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.atualizar_kanban()
        QMessageBox.information(self, "Sucesso", "Task adicionada!")
    
    def atualizar_kanban(self):
        for column in self.columns.values():
            while column.scroll_layout.count():
                item = column.scroll_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        
        for task in get_tasks():
            task_id, desc, status, categoria, dt_venc = task
            task_widget = TaskWidget(task_id, desc, status, categoria, dt_venc, self)
            self.columns[status].scroll_layout.addWidget(task_widget)
        
        for column in self.columns.values():
            column.scroll_layout.addStretch()
    
    def move_task(self, task_id, new_status):
        update_status_task(task_id, new_status)
        self.atualizar_kanban()
    
    def delete_task(self, task_id):
        delete_task(task_id)
        self.atualizar_kanban()
        QMessageBox.information(self, "Sucesso", "Tarefa excluída.")


def start_gui():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())