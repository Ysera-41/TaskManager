from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class TaskWidget(QFrame):
    def __init__(self, task_id, desc, status, categoria, dt_venc, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.status = status
        self.parent = parent
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setStyleSheet("""
            TaskWidget {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QLabel {
                margin: 2px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Descrição
        lbl_desc = QLabel(desc)
        lbl_desc.setWordWrap(True)
        lbl_desc.setFont(QFont("Segoe UI", 10))
        layout.addWidget(lbl_desc)
        
        # Categoria
        lbl_cat = QLabel(f"[{categoria}]")
        lbl_cat.setFont(QFont("Segoe UI", 8))
        lbl_cat.setStyleSheet("color: #555;")
        layout.addWidget(lbl_cat)
        
        # Data de vencimento
        if dt_venc:
            lbl_date = QLabel(f"Vence: {dt_venc}")
            lbl_date.setFont(QFont("Segoe UI", 8))
            lbl_date.setStyleSheet("color: #d35400;")
            layout.addWidget(lbl_date)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        if status != "AF":
            btn_prev = QPushButton("←")
            btn_prev.setFixedWidth(30)
            btn_prev.setStyleSheet("QPushButton { background-color: #3498db; color: white; }")
            btn_prev.clicked.connect(self.move_left)
            btn_layout.addWidget(btn_prev)
        
        if status != "CO":
            btn_next = QPushButton("→")
            btn_next.setFixedWidth(30)
            btn_next.setStyleSheet("QPushButton { background-color: #2ecc71; color: white; }")
            btn_next.clicked.connect(self.move_right)
            btn_layout.addWidget(btn_next)
        
        btn_delete = QPushButton("🗑️")
        btn_delete.setFixedWidth(30)
        btn_delete.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; }")
        btn_delete.clicked.connect(self.delete_task)
        btn_layout.addWidget(btn_delete)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def move_left(self):
        ordem = ["AF", "EP", "CO"]
        idx = ordem.index(self.status)
        novo_status = ordem[idx - 1]
        self.parent.move_task(self.task_id, novo_status)
    
    def move_right(self):
        ordem = ["AF", "EP", "CO"]
        idx = ordem.index(self.status)
        novo_status = ordem[idx + 1]
        self.parent.move_task(self.task_id, novo_status)
    
    def delete_task(self):
        reply = QMessageBox.question(self, 'Confirmação',
                                     'Deseja realmente excluir esta tarefa?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.parent.delete_task(self.task_id)