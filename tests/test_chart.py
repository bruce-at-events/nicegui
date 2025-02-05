from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


def test_change_chart_series(screen: Screen):
    chart = ui.chart({
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['A', 'B']},
        'series': [
            {'name': 'Alpha', 'data': [0.1, 0.2]},
            {'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    }).classes('w-full h-64')

    def update():
        chart.options['series'][0]['data'][:] = [1, 1]
        chart.update()

    ui.button('Update', on_click=update)

    def get_series_0():
        return screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-series-0 .highcharts-point')

    screen.open('/')
    screen.wait(0.5)
    before = [bar.size['width'] for bar in get_series_0()]
    screen.click('Update')
    screen.wait(0.5)
    after = [bar.size['width'] for bar in get_series_0()]
    assert before[0] < after[0]
    assert before[1] < after[1]


def test_adding_chart_series(screen: Screen):
    chart = ui.chart({
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['A', 'B']},
        'series': [],
    }).classes('w-full h-64')

    def add():
        chart.options['series'].append({'name': 'X', 'data': [0.1, 0.2]})
        chart.update()
    ui.button('Add', on_click=add)

    screen.open('/')
    screen.click('Add')
    screen.wait(0.5)
    assert len(screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-point')) == 3


def test_removing_chart_series(screen: Screen):
    chart = ui.chart({
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['A', 'B']},
        'series': [
            {'name': 'Alpha', 'data': [0.1, 0.2]},
            {'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    }).classes('w-full h-64')

    def remove():
        chart.options['series'].pop(0)
        chart.update()
    ui.button('Remove', on_click=remove)

    screen.open('/')
    screen.click('Remove')
    screen.wait(0.5)
    assert len(screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-point')) == 3


def test_extra(screen: Screen):
    ui.chart({'chart': {'type': 'solidgauge'}}, extras=['solid-gauge'])

    screen.open('/')
    assert screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-pane')


def test_missing_extra(screen: Screen):
    ui.chart({'chart': {'type': 'solidgauge'}})

    screen.open('/')
    assert not screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-pane')


def test_stock_chart(screen: Screen):
    ui.chart({}, type='stockChart', extras=['stock'])

    screen.open('/')
    assert screen.selenium.find_elements(By.CSS_SELECTOR, '.highcharts-range-selector-buttons')


def test_replace_chart(screen: Screen):
    with ui.row() as container:
        ui.chart({'series': [{'name': 'A'}]})

    def replace():
        container.clear()
        with container:
            ui.chart({'series': [{'name': 'B'}]})
    ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')
    screen.click('Replace')
    screen.should_contain('B')
    screen.should_not_contain('A')
