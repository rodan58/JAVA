# тестируем систему лифтов (elevators.py)
# при помощи pytest

import pytest

import elevators


class TestElevatorSystem:

    def test_is_there_elevator_on_first_floor(self):
        # создаём систему лифтов для двух этажного дома
        # с двумя лифтами
        elsys = elevators.ElevatorSystem(2, 2)
        # all elevators on the first floor on default
        # все лифты по умолчанию при создании находяться на 
        # первом этаже
        # проверяем, есть ли лифт на первом этаже
        assert elsys.is_there_elevator_on_first_floor() == True
        # all elevators are not on the first floor
        # перегоняем все лифты (оба) на второй этаж
        for elevator, floor in zip(elsys.elevators, (2, 2)):
            elevator.floor = floor
        # убеждаемся что на первом этаде лифтов нет
        assert elsys.is_there_elevator_on_first_floor() == False
        
    def test_search_nearest_elevator(self):
        # система лифтов
        elsys = elevators.ElevatorSystem(3, 2)
        # значения
        # 1. desired_floor - нужный лифт, число для вызова call_elevator()
        # 2. floor_1 - указываем этажа для первого лифта
        # 3. floor_2 - указываем этажа для второго
        # 4. right_answer - номер этажа с которого должен вызваться лифт
        values = (
            (1, 2, 3, 2),
            (3, 2, 1, 2),
            )
        for desired_floor, floor_1, floor_2, right_answer in values:
            # переменные для двух лифтов, их всего два
            first_elevator, second_elevator = elsys.elevators
            # раставляем лифты на нужные этажи
            first_elevator.floor = floor_1
            second_elevator.floor = floor_2
            # находим лифт который ближе всего к желаемому этажу
            elevator = elsys.search_nearest_elevator(desired_floor)
            # номер этажа найденного лифта должен совпадать с ответом
            assert elevator.floor == right_answer

    def test_call_elevator(self):
        # система лифтов, пять этажей, два лифта
        elsys = elevators.ElevatorSystem(5, 2)
        # значения
        # 1. desired_floor - желаемый этаж
        # 2. floor_1 - этаж для первого лифта
        # 3. floor_2 - для второго
        values = (
            (2, 1, 5),
            (3, 2, 1),
            )
        for desired_floor, floor_1, floor_2 in values:
            # сохраняем объекты лифтов в переменные, их всего 2
            first_elevator, second_elevator = elsys.elevators
            # устанавливаем лифты на нужные этажи
            first_elevator.floor = floor_1
            second_elevator.floor = floor_2
            # "вызываем" лифт для нужного этажа
            elsys.call_elevator(desired_floor)
            # ксли есть хоть одни лифт на нужном этаже, то ok
            assert any(filter(
                lambda elevator: elevator.floor == desired_floor,
                elsys.elevators))
            # но при этом на первом этаже тоже должен быть вызван лифт
            assert elsys.is_there_elevator_on_first_floor()

#elsys = elevators.ElevatorSystem(2, 2)
