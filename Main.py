from PyQt5.QtCore import Qt
import Constants
import sys
import openai 
from PyQt5.QtCore import Qt  
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QGroupBox, 
    QTextEdit
)

#OpenAI API key(Where constants is a python file which include OpenAI key's information)
openai.api_key = Constants.API_key

class Main_Window(QWidget) : 

    def __init__(self) : 
        super().__init__() 
        self.init_ui()
    
    def init_ui(self) : 
        #Create the Widgets
        self.logo_label = QLabel()
        self.input_label = QLabel("Start Chatting:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter your message here.")
        self.answer_label = QLabel() 
        self.answer_field = QTextEdit()
        self.answer_field.setReadOnly(True)
        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet(
            """
QPushButton{
background-color: #4CAF50;
border: none;
color: white;
padding: 15px 32px; 
font-size: 18px; 
font-weight: bold;
border-radius: 10px;
}
QPushButton: hover{
background-color: #3e8e41;
}
            """
        )
        self.popular_questions_group = QGroupBox("Popular Questions")
        self.popular_questions_layout = QVBoxLayout()
        self.popular_questions = {"What is Machine Learning?", "What are some popular Machine Learing algorithms?", "What is python?"}
        self.question_buttons = []

        #Create a layout 
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20) 
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter) 

        #Adding Logo 
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter) 

        #Adding Indput Feild and Submit Button 
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)
        layout.addLayout(input_layout)

        #Adding Answer Feild 
        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_field)
        
        #Adding Answer Feild 
        for questions in self.popular_questions : 
            button = QPushButton(questions) 
            button.setStyleSheet(
                """
QPushButton{
background-color: #FFFFFF;
border: 2px solid #00AEFF;
colour: #00AEFF
padding: 10px 20px; 
font-size: 18px; 
font-weight: bold;
border-radius: 5px;
}
QPushButton:hover{
background-color: #00AEFF;
color: #FFFFFF;
}"""
            )
            button.clicked.connect(lambda _, q = questions: self.input_field.setText(q)) 
            self.popular_questions_layout.addWidget(button)
            self.question_buttons.append(button)
        self.popular_questions_group.setLayout(self.popular_questions_layout) 
        layout.addWidget(self.popular_questions_group)

        #Set the layout 
        self.setLayout(layout)

        #Set the window properties 
        self.setWindowTitle("Machine Learning Career Advicer")
        self.setGeometry(200, 200, 600, 600)

        # Set the background color of the window
        self.setStyleSheet("background-color: #8478bf;")

        #Connect the submmit button to the function which queries OpenAI's API 
        self.submit_button.clicked.connect(self.get_answer)
    
    def get_answer(self) : 
        question = self.input_field.text()

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [{"role" : "user", "content" : "You are a machine leaning engineer. Answer the following question in a concise way or with bullet points."}, 
                        {"role" : "user", "content" : f'{question}'}], 
            max_tokens = 1024, 
            n = 1, 
            stop = None, 
            temperature = 0.7
        )

        answer = completion.choices[0].message.content 

        self.answer_field.setText(answer) 

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
