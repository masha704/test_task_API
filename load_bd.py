import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Date

# Настройка соединения с базой данных
DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost:5432/postgres"

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)

# Определение базового класса
Base = declarative_base()

class Respondent(Base):
    __tablename__ = 'respondents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)  # Изменено на lower_case
    respondent = Column(Integer)  # Удалено уникальное ограничение
    sex = Column(Integer)  # Изменено на lower_case и соответствующий порядок
    age = Column(Integer)  # Изменено на lower_case
    weight = Column(Float)  # Изменено на lower_case

# Создание таблицы, если она не существует
Base.metadata.create_all(engine)

def load_data_from_csv(file_path):
    # Чтение данных из CSV в DataFrame с разделителем ";"
    df = pd.read_csv(file_path, sep=';')
    
    # Удаление ненужного столбца
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)
    
    # Проверка названий столбцов
    print("Названия столбцов:", df.columns.tolist())
    
    # Конвертация столбца Date в стандартный формат даты
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

    # Добавление уникального идентификатора
    df['id'] = range(1, len(df) + 1)  # Начинается с 1

    # Переименование столбцов
    df.rename(columns={
        'Date': 'date',
        'Sex': 'sex',
        'Age': 'age',
        'Weight': 'weight'
    }, inplace=True)

    # Перемещаем 'id' в начало DataFrame
    cols = ['id'] + [col for col in df.columns if col != 'id']
    df = df[cols]

    print("Названия столбцов:", df.columns.tolist())
    # Заполнение базы данных без удаления дубликатов
    with engine.connect() as connection:
        df.to_sql('respondents', con=connection, if_exists='append', index=False)

if __name__ == '__main__':
    # Замените 'data.csv' на путь к вашему файлу
    load_data_from_csv('data.csv')
    print("Данные успешно загружены в базу данных.")
