def read_file(file: str) -> list[list[str]]:
    """
    Чтение отчёта из CSV-файла и возврат списка из списка сотрудников
    :param file: Путь к CSV-файлу с отчётом
    :return: Список списков с информацией о сотрудниках
    """
    employees = []
    with open(file, 'r') as f:
        for line in f:
            employees.append((line[1:-2].split(";")))
    f.close()
    return employees[1:]


def hierarchy(employees: list[list[str]]) -> None:
    """
        Вывод иерархии команд
        :param employees: Список списков с информацией о сотрудниках
        :return: None
    """
    my_dict = {}
    for employ in employees:
        my_dict[employ[1]] = my_dict.get(employ[1], "") + ";" + employ[2]

    for dep in my_dict:
        my_dict[dep] = set(my_dict[dep][1:].split(";"))

    for dep in my_dict:
        print(f"Департамент:\n {dep}")
        print("Команды:")
        for team in my_dict[dep]:
            print(f"  - {team}")
        print()


def department_report(employees: list[list[str]]) -> dict:
    """
            Создание отчета по департаментам
            :param employees: Список списков с информацией о сотрудниках
            :return: словарь ключами которого являются департаменты,
                     а значением - список информации о ключе
    """
    my_dict = {}
    for employ in employees:
        if employ[1] in my_dict:
            my_dict[employ[1]][0] += 1
            my_dict[employ[1]][1] = min(my_dict[employ[1]][1], int(employ[5]))
            my_dict[employ[1]][2] = max(my_dict[employ[1]][2], int(employ[5]))
            my_dict[employ[1]][3] += int(employ[5])
        else:
            my_dict[employ[1]] = [1, int(employ[5]), int(employ[5]), int(employ[5])]
    for dep in my_dict:
        my_dict[dep][3] = round(my_dict[dep][3] / my_dict[dep][0])

    for department, data in my_dict.items():
        print(f'Департамент:{department}\n'
              f'Численность:{data[0]}\n'
              f'Зарплатная вилка min={data[1]} - max={data[2]}\n'
              f'Средняя зарплата:{data[3]}\n')

    return my_dict


def save_department_report(employees: list[list[str]], file_path: str) -> None:
    """
        Сохранение сводного отчёта по департаментам в CSV-файл.
        :param employees: Список списков с информацией о сотрудниках
        :param file_path: Путь для сохранения CSV-файла
    """

    report = {}
    for employ in employees:
        if employ[1] in report:
            report[employ[1]][0] += 1
            report[employ[1]][1] = min(report[employ[1]][1], int(employ[5]))
            report[employ[1]][2] = max(report[employ[1]][2], int(employ[5]))
            report[employ[1]][3] += int(employ[5])
        else:
            report[employ[1]] = [1, int(employ[5]), int(employ[5]), int(employ[5])]
    for dep in report:
        report[dep][3] = round(report[dep][3] / report[dep][0])

    with open(file_path, 'w') as file:
        file.write('Департамент;Численность;Зарплатная вилка(min-max); Средняя зарплата\n')
        for line in report:
            file.write(line + ";" + str(report[line][0]) + ";"
                       + str(report[line][1]) + '-' + str(report[line][2]) + ";" + str(report[line][3]) + '\n')


if __name__ == '__main__':
    FILE = 'Corp_Summary.csv'
    choice = input("Введите \n'1',если хотите вывести департаменты и все команды, которые входят в него\n"
                   "'2', если хотите вывести сводный отчёт по департаментам\n"
                   "'3', если хотите сохранить сводный отчет\n")

    Staff = read_file(FILE)
    if choice == '1':
        hierarchy(Staff)
    elif choice == '2':
        department_report(Staff)
    elif choice == '3':
        name = input("Сохранить отчет как\n")
        save_department_report(Staff, name+".csv")
    else:
        print("Ошибка: выбран неправильный пункт меню")