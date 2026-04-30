import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def analyze_pressure_data(file_path):

    try:
        # Phyphox може використовувати коми або крапки з комою залежно від налаштувань
        df = pd.read_csv(file_path)
        
        # Автоматичне перейменування колонок, якщо вони мають специфічні назви від Phyphox
        if len(df.columns) >= 2:
            df = df.iloc[:, [0, 1]] # беремо перші дві колонки
            df.columns = ['time', 'pressure']
        else:
            print("Помилка: Некоректна структура CSV файлу.")
            return

    except FileNotFoundError:
        print(f"Помилка: Файл {file_path} не знайдено.")
        return

    # Розрахунок основних статистичних показників
    mean_p = df['pressure'].mean()
    std_p = df['pressure'].std()
    max_p = df['pressure'].max()
    min_p = df['pressure'].min()

    # Візуалізація
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))
    
    plt.plot(df['time'], df['pressure'], label='Показники барометра (hPa)', color='teal', linewidth=1.5)
    plt.axhline(mean_p, color='red', linestyle='--', label=f'Середнє значення: {mean_p:.2f} hPa')
    
    # Виділення зони стандартного відхилення
    plt.fill_between(df['time'], mean_p - std_p, mean_p + std_p, color='orange', alpha=0.2, label='Варіативність (±1 std)')
    
    plt.title('Дослідження коливань атмосферного тиску (Лабораторна робота 6)')
    plt.xlabel('Час (секунди)')
    plt.ylabel('Тиск (hPa)')
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

    # Вивід аналітичного звіту
    print(f"--- Результати аналізу (Мідловець А. Л., ТВ-33) ---")
    print(f"Середній тиск: {mean_p:.4f} hPa")
    print(f"Діапазон (max - min): {max_p - min_p:.4f} hPa")
    print(f"Стандартне відхилення: {std_p:.4f}")
    
    if std_p > 0.03:
        print("Висновок: Виявлено значні мікроколивання тиску. Можливий вплив вітру або переміщення між приміщеннями.")
    else:
        print("Висновок: Тиск стабільний. Дані відповідають умовам закритого приміщення без активної вентиляції.")

if __name__ == "__main__":
   
    filename = 'sensor_data_example.csv'
    
    demo_time = np.linspace(0, 600, 1000) 
    

    room_pressure = np.random.normal(1013.25, 0.005, 500)
    street_pressure = np.random.normal(1012.80, 0.04, 500)
    demo_press = np.concatenate([room_pressure, street_pressure])
    
    demo_df = pd.DataFrame({'time': demo_time, 'pressure': demo_press})
    demo_df.to_csv(filename, index=False)
    
    print(f"Демонстраційні дані збережено у {filename}. Починаю аналіз...")
    analyze_pressure_data(filename)