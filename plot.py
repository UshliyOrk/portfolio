from matplotlib.pyplot import title, xlabel, ylabel, grid, plot, show, savefig, legend, gca
import numpy as np
import sympy as sp


class Main:
    # запрос исходных данных
    def __init__(self):
        super(Main, self).__init__()
        self.functions = input("введите графики через пробел--> ").split()
        self.a = float(input("начало интервала--> "))
        self.b = float(input('конец интервала--> '))
    # создание графиков
    def funcPlot(self):
        # Независимая (x) и зависимая (y) переменные
        self.x = np.linspace(self.a, self.b, 50)
        # Построение графика
        for function in self.functions:
            f = sp.sympify(function)  # перевод текста в понятный формат для sympy
            x = sp.symbols("x")  # переменная x для sympy
            fnc = sp.lambdify(x, f, 'numpy')  # создание функции для y
            y = fnc(self.x)
            plot(self.x, y, label = function)  # добавление графика с названием (для легенды) на плоскость

        ax = gca()

        # plot X - axis    
        ax.axhline(y=0, color='k')

        # plot Y - axis    
        ax.axvline(x=0, color='k')
        title('здесь могла быть ваша реклама')  # заголовок
        xlabel('x')  # ось абсцисс
        ylabel('y')  # ось ординат
        grid()  # включение отображение сетки
        legend()  # включение легенды
        savefig("plt.png")  # график в png файл
        show()  # вывод конечного результата


if __name__ == "__main__":
    app = Main()
    app.funcPlot()