#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import deque

import sys
sys.stdin = open('input.txt')

def input_data():
    """
    Получаем граф от пользователя
    Возвращаем:
                * сам граф
                * название начального узла, откуда ведётся поиск
                * Искомое свойство у людей
                * таблицу свойст узлов
    """
    # Получаем данные от пользователя
    # Название начального узла, откуда ведётся поиск
    start = input().strip()
    # Получаем искомое свойство у персоны в графе
    desired_property = input().strip().lower()

    # Дальше идём до флага в файле, чтобы заполнить таблицу свойств
    while True:
        if input().strip().lower() == 'граф:':
            break
        
    # сам граф
    graph = {}    
    # Заполняем граф
    while True:
        data = input().strip()
        # Если получаем флаг, что нужно вводить свойства персонажей
        if data.lower() == 'свойства:':
            # Переходим к заполнению свойств
            break
        # Если пустая строка, то пропускаем её
        elif not data:
            continue
        # Строка содержит информацию об узле и его потомках (соседях)
        else:
            # Получаем название узла и его потомков
            node, *childs = data.split()
            childs = set(childs)

            # Если такого узла ёще нет в графе
            if node not in graph:
                graph[node] = childs
            else:
                # узел есть в графе, обновляем его потомков
                graph[node].update(childs)
            
            # Добавляем всех потомков этого узла в граф
            for child in childs:
                if child not in graph:
                    # Пустое множество, мы же не знаем пока что потомков этих персонажей
                    graph[child] = set()

    # Таблица свойств узлов, где ключ - имя персонажа, а значение - список его свойств
    properties = {}
    while True:
        try:
            # Получаем узел и его свойства
            node, *childs = input().split()
            childs = set([child.lower() for child in childs])
        except EOFError:             # если достигли конца файла или ввода
            break                    # завершаем бесконечный цикл
        else:
            # Если ввод от пользователя не закончен, то
            # Проверяем есть ли такой узел УЖЕ в таблице свойств
            if node not in properties:
                # Если его нет, то добавляем новую запись
                properties[node] = childs
            else:
                # Узел есть в таблице, обновляем свойства узла
                properties[node].update(childs)

    return (graph, start, desired_property, properties)

def main():
    # Получаем информацию о графе
    graph, start, desired_property, properties = input_data()
    
    # Создаем новую очередь для последовательного обхода всех узлов
    search_queue = deque()
    # Всех дочерних потомков стартового узла добавляем в эту очередь
    search_queue.extend(graph[start])
    # Множество для отслеживания проверенных людей
    searched = set()
    # Флаг что мы точно нашли человека с таким свойством
    # А не просто прошли всех людей и никого не нашли
    is_finded = False
    # Имя человека в графе, нужно для поиска и вывода результата
    person = None
    # Пока очередь не пуста ищем персонажа с нужным свойством в графе
    while search_queue:
        # Извлекаем первого человека из очереди
        person = search_queue.popleft()

        # Если этого человека еще не проверяли
        if person not in searched:
            # Если у данного человека есть необходимое свойство
            if desired_property in properties[person]:
                # Поднимаем флаг что нашли нужного человека
                is_finded = True
                # Завершаем поиск такого человека
                break
            else:
                # Человек не подходит, но возможно среди его друзей (потомков - соседей)
                # найдется человек с нужным свойством
                # Поэтому добавляем все дочерние элменты узла в очередь поиска
                search_queue.extend(graph[person])
                # Помечаем человека как проверенного
                searched.add(person)
    
    # Если нужного человека нашли, то выводим этого человека и его свойства
    if is_finded:
        print(f'{person}: {properties[person]}')
    else:
        # Такого человека не нашли
        print("Такого человека нет")

if __name__ == "__main__":
    main()