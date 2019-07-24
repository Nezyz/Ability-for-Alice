from flask import Flask, request
import logging
import json
import random

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

Session_data = {}
current_status = "start"
current_dialog = "start"
rank = 26
chewed_tie = 0
minister = 0
result = 0


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    main_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def main_dialog(res, req):
    global current_status, current_dialog, Session_data, rank, chewed_tie, minister, result

    user_id = req['session']['user_id']
    if current_dialog == "start":
        if req['session']['new']:
            res['response']['text'] = 'Поздравляем! Вы были избраны президентом Пранкии на ' \
                                      'наследующие 5лет!!! Наша страна обладает огромными запасами' \
                                      ' всех ресурсов. От принятых Вами решений зависит ' \
                                      'судьба Пранкии и её населения. Ваша деятельность ' \
                                      'на посту главы государства будет оцениваться ' \
                                      'рейтингом. В случае высокого рейтинга Вы ' \
                                      'будете переизбраны на второй срок. Иначе: ' \
                                      'крах карьеры. ' \
                                      'Помните: ' \
                                      'Ваш непрофессионализм приведет к ' \
                                      'развалу страны и/ или гибели её граждан. ' \
                                      'Изначально ваш рейтинг равен: ' + str(int(rank)) + \
                                      ' Итак, Вы готовы вершить судьбы?'
            current_dialog = 'choice'
            current_status = 'start_question'
            Session_data[user_id] = {
                'suggests': [
                    "Да",
                    "Нет",
                    "пожевать галстук",
                    "Рейтинг",
                    "Помощь",
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
    if req['request']['original_utterance'].lower() in ['рейтинг']:
        current_main = current_dialog
        current_dialog = 'rank'
    if current_dialog == 'rank':
        res['response'][
            'text'] = 'Ваш рейтинг: ' + str(int(rank)) + ' Так что Вы решили?'
        current_dialog = current_main
    if req['request']['original_utterance'].lower() in ['помощь']:
        current_main = current_dialog
        current_dialog = 'help'
    if current_dialog == 'help':
        res['response']['text'] = 'Вы были избраны президентом Пранкии ' \
                                  'наследующие 5лет!!! Наша страна-республика со смешанной ' \
                                  'формой правления. Она обладает огромными запасами' \
                                  ' всех ресурсов. От принятых Вами решений зависит ' \
                                  'судьба Пранкии и её населения. Ваша деятельность ' \
                                  'на посту главы государства будет оцениваться ' \
                                  'рейтингом. В случае высокого рейтинга Вы ' \
                                  'будете переизбраны на второй срок. Иначе ' \
                                  'крах карьеры. В управлении страной Вам ' \
                                  'помогают советники, но ответственность ' \
                                  'несете только Вы. Будьте начеку - против ' \
                                  'Вас затеяли грязную игру нечистоплотные ' \
                                  'политики, завистливые коллеги и ' \
                                  'иностранные государства, желающие ' \
                                  'расширить свои территории. Помните: ' \
                                  'Ваш непрофессионализм приведет к ' \
                                  'развалу страны и/или гибели её граждан.' \
                                  'Изначально ваш рейтинг равен: ' + str(int(rank)) + ' Так что Вы решили?'
        current_dialog = current_main
    if current_dialog == "choice":
        if req['request']['original_utterance'].lower() not in ['да', 'нет', 'пожевать галстук', 'помощь', 'рейтинг']:
            res['response'][
                'text'] = 'Такого выбора ответа нет. Попробуй ещё раз.' + 'Ваш рейтинг равен: ' + str(int(rank))
            Session_data[user_id] = {
                'suggests': [
                    "Да",
                    "Нет",
                    "пожевать галстук",
                    "Рейтинг",
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in ['да']:
            rank += 5
            current_dialog = 'prime_minister'
            res['response'][
                'text'] = 'Вам нужно назначить премьер-министра. ' \
                          'Советники предложили четырех кандидатов:' \
                          '1) ПМ1 - дочь олигарха, очень красивая, но глупая и много говорит, популярна в народе.' \
                          '2) ПМ2 - карьерист, взяточник, обладает обширными связями и влиянием в СМИ.' \
                          '3) ПМ3 - бывший руководитель внешней разведки, государственник,сильный экономист.' \
                          '4) ПМ4-женщина средних лет, всего добилась сама, крупный специалист в' \
                          ' социальной сфере, слабость -' \
                          'непутевый сын, которого она хочет сделать президентом. Что делать? ' \
                          'Ваш рейтинг равен: ' + str(int(rank))
            Session_data[user_id] = {
                'suggests': [
                    "1",
                    "2",
                    "3",
                    "4",
                    "Рейтинг",
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in ['нет']:
            rank = 0
            res['response']['text'] = 'Пограничник вручает Вам паспорт и желает счастливого пути.' \
                                      'Ваш рейтинг равен: ' + str(int(rank))
            Session_data[user_id] = {
                'suggests': [
                    "Начать заново.",
                    "Выйти",
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in ['пожевать галстук']:
            rank -= 10
            spis = [3, -3]
            a = random.choice(spis)
            rank += a
            chewed_tie += 1
            current_dialog = 'prime_minister'
            res['response'][
                'text'] = 'Будем считать, что Вы согласились. Такие ответы добавляют вам либо отрицательное' \
                          ' значение рейтинга, либо положительное,' \
                          ' в зависимости' \
                          ' от ситуации, будьте аккуратнее. Вам нужно назначить премьер-министра. ' \
                          'Советники предложили четырех кандидатов:' \
                          '1) ПМ1 - дочь олигарха, очень красивая, но глупая и много говорит, популярна в народе.' \
                          '2) ПМ2 - карьерист, взяточник, обладает обширными связями и влиянием в СМИ.' \
                          '3) ПМ3 - бывший руководитель внешней разведки, государственник,сильный экономист.' \
                          '4) ПМ4 - женщина средних лет, всего добилась сама, крупный специалист в социальной' \
                          ' сфере, слабость -' \
                          'непутевый сын, которого она хочет сделать президентом. Что делать? ' \
                          'Ваш рейтинг равен: ' + str(int(rank))
            Session_data[user_id] = {
                'suggests': [
                    "1",
                    "2",
                    "3",
                    "4",
                    "Рейтинг",
                    "Помощь"
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
    if current_dialog == 'prime_minister':
        if req['request']['original_utterance'].lower() not in ['1', '2', '3', '4', 'рейтинг', 'помощь']:
            res['response'][
                'text'] = 'Такого выбора ответа нет. Попробуй ещё раз.'
            Session_data[user_id] = {
                'suggests': [
                    "1",
                    "2",
                    "3",
                    "4",
                    "Рейтинг",
                    "Помощь"
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in ['1']:
            minister = 1
            rank -= 10
            res['response']['text'] = 'Вы сделали плохой выбор, Ваш рейтинг упал на 10 единиц. ' \
                                      'ПМ1 предложила состав Кабинета министров. Что делать?' \
                                      ' ' + 'Ваш рейтинг равен: ' + str(int(rank))
            current_dialog = 'minister'
            Session_data[user_id] = {
                'suggests': [
                    "Одобряю",
                    "Не одобряю",
                    "Рейтинг",
                    "Помощь"
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in ['2']:
            minister = 2
            rank -= 3
            res['response']['text'] = 'Вы сделали не самый лучший выбор, Ваш рейтинг упал на 3. ' \
                                      'ПМ2 предложил состав Кабинета министров. Что делать?' \
                                      ' ' + 'Ваш рейтинг равен: ' + str(int(rank))
            current_dialog = 'minister'
            Session_data[user_id] = {
                'suggests': [
                    "Одобряю",
                    "Не одобряю",
                    "Рейтинг",
                    "Помощь"
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in ['3']:
            minister = 3
            rank += 5
            res['response']['text'] = 'Вы сделали отличный выбор, Ваш рейтинг поднялся на 5.' \
                                      ' ПМ3 предложил состав Кабинета министров. Что делать? ' \
                                      + 'Ваш рейтинг равен: ' + str(int(rank))
            current_dialog = 'minister'
            Session_data[user_id] = {
                'suggests': [
                    "Одобряю",
                    "Не одобряю",
                    "Рейтинг",
                    "Помощь"
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in ['4']:
            minister = 4
            rank -= 0
            res['response']['text'] = 'Вы сделали неплохой выбор, Ваш рейтинг остался без изменений.' \
                                      ' ПМ1 предложила состав Кабинета министров. Что делать? ' \
                                      + 'Ваш рейтинг равен: ' + str(int(rank))
            current_dialog = 'minister'
            Session_data[user_id] = {
                'suggests': [
                    "Одобряю",
                    "Не одобряю",
                    "Рейтинг",
                    "Помощь"
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return
    if current_dialog == 'minister':
        if minister == 1:
            if req['request']['original_utterance'].lower() not in ['одобряю', 'не одобряю']:
                res['response']['text'] = 'Такого выбора нет. Попробуйте ещё раз.'
                Session_data[user_id] = {
                    'suggests': [
                        "Одобряю",
                        "Не одобряю",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
            if req['request']['original_utterance'].lower() in ['одобряю']:
                rank -= 3
                res['response']['text'] = 'Ваш рейтинг упал на 3.' \
                                          'На первом заседании кабинета ' \
                                          'министров объявили о том, что ' \
                                          'ВВП в этом году увеличился ' \
                                          'на 300%. Министры не сошлись ' \
                                          'во мнении,как распределить ' \
                                          'доход, и, открыв ' \
                                          'рты, ждут Вашего ' \
                                          'решения. Что делать? ' \
                                          'Возможные варианты: ' \
                                          '1) Отличные новости! Направим ресур сы на развитие науки и технологи. ' \
                                          '2) Прекрасно! Распределим деньги по' \
                                          ' частным компаниям: пусть создают новые технологии. ' \
                                          '3) Хорошо! Создадим кубышку. ' \
                                          '4) Я приказываю разделить неожиданный доход поровну между' \
                                          ' всеми гражданами нашей страны. ' \
                                          + 'Ваш рейтинг равен: ' + str(int(rank))
                current_dialog = 'first_picking_minister'
                Session_data[user_id] = {
                    'suggests': [
                        "1",
                        "2",
                        "3",
                        "4",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
            if req['request']['original_utterance'].lower() in ['не одобряю']:
                rank += 5
                res['response']['text'] = 'Ваш рейтинг поднялся  на 5.' \
                                          'На первом заседании кабинета ' \
                                          'министров объявили о том, что ' \
                                          'ВВП в этом году увеличился ' \
                                          'на 300%. Министры не сошлись ' \
                                          'во мнении,как распределить ' \
                                          'доход, и, открыв ' \
                                          'рты, ждут Вашего ' \
                                          'решения. Что делать? ' \
                                          'Возможные варианты: ' \
                                          '1) Отличные новости! Направим ресур сы на развитие науки и технологи. ' \
                                          '2) Прекрасно! Распределим деньги по' \
                                          ' частным компаниям: пусть создают новые технологии. ' \
                                          '3) Хорошо! Создадим кубышку. ' \
                                          '4) Я приказываю разделить неожиданный доход поровну между' \
                                          ' всеми гражданами нашей страны. ' \
                                          + 'Ваш рейтинг равен: ' + str(int(rank))
                current_dialog = 'first_picking_minister'
                Session_data[user_id] = {
                    'suggests': [
                        "1",
                        "2",
                        "3",
                        "4",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
        if minister == 2:
            if req['request']['original_utterance'].lower() not in ['одобряю', 'не одобряю']:
                res['response']['text'] = 'Такого выбора нет. Попробуйте ещё раз.'
                Session_data[user_id] = {
                    'suggests': [
                        "Одобряю",
                        "Не одобряю",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
            if req['request']['original_utterance'].lower() in ['одобряю']:
                rank -= 3
                res['response']['text'] = 'Ваш рейтинг упал на 3.' \
                                          'На первом заседании кабинета ' \
                                          'министров объявили о том, что ' \
                                          'ВВП в этом году увеличился ' \
                                          'на 300%. Министры не сошлись ' \
                                          'во мнении,как распределить ' \
                                          'доход, и, открыв ' \
                                          'рты, ждут Вашего ' \
                                          'решения. Что делать? ' \
                                          'Возможные варианты: ' \
                                          '1) Отличные новости! Направим ресур сы на развитие науки и технологи. ' \
                                          '2) Прекрасно! Распределим деньги по' \
                                          ' частным компаниям: пусть создают новые технологии. ' \
                                          '3) Хорошо! Создадим кубышку. ' \
                                          '4) Я приказываю разделить неожиданный доход поровну между' \
                                          ' всеми гражданами нашей страны. ' \
                                          + 'Ваш рейтинг равен: ' + str(int(rank))
                current_dialog = 'first_picking_minister'
                Session_data[user_id] = {
                    'suggests': [
                        "1",
                        "2",
                        "3",
                        "4",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
            if req['request']['original_utterance'].lower() in ['не одобряю']:
                rank += 5
                res['response']['text'] = 'Ваш рейтинг поднялся  на 5.' \
                                          'На первом заседании кабинета ' \
                                          'министров объявили о том, что ' \
                                          'ВВП в этом году увеличился ' \
                                          'на 300%. Министры не сошлись ' \
                                          'во мнении,как распределить ' \
                                          'доход, и, открыв ' \
                                          'рты, ждут Вашего ' \
                                          'решения. Что делать? ' \
                                          'Возможные варианты: ' \
                                          '1) Отличные новости! Направим ресур сы на развитие науки и технологи. ' \
                                          '2) Прекрасно! Распределим деньги по' \
                                          ' частным компаниям: пусть создают новые технологии. ' \
                                          '3) Хорошо! Создадим кубышку. ' \
                                          '4) Я приказываю разделить неожиданный доход поровну между' \
                                          ' всеми гражданами нашей страны. ' \
                                          + 'Ваш рейтинг равен: ' + str(int(rank))
                current_dialog = 'first_picking_minister'
                Session_data[user_id] = {
                    'suggests': [
                        "1",
                        "2",
                        "3",
                        "4",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
        if minister == 3:
            if req['request']['original_utterance'].lower() not in ['одобряю', 'не одобряю']:
                res['response']['text'] = 'Такого выбора нет. Попробуйте ещё раз.'
                Session_data[user_id] = {
                    'suggests': [
                        "Одобряю",
                        "Не одобряю",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
            if req['request']['original_utterance'].lower() in ['одобряю']:
                rank += 5
                res['response']['text'] = 'Ваш рейтинг поднялся на 5.' \
                                          'На первом заседании кабинета ' \
                                          'министров объявили о том, что ' \
                                          'ВВП в этом году увеличился ' \
                                          'на 300%. Министры не сошлись ' \
                                          'во мнении,как распределить ' \
                                          'доход, и, открыв ' \
                                          'рты, ждут Вашего ' \
                                          'решения. Что делать? ' \
                                          'Возможные варианты: ' \
                                          '1) Отличные новости! Направим ресур сы на развитие науки и технологи. ' \
                                          '2) Прекрасно! Распределим деньги по' \
                                          ' частным компаниям: пусть создают новые технологии. ' \
                                          '3) Хорошо! Создадим кубышку. ' \
                                          '4) Я приказываю разделить неожиданный доход поровну между' \
                                          ' всеми гражданами нашей страны. ' \
                                          + 'Ваш рейтинг равен: ' + str(int(rank))
                current_dialog = 'first_picking_minister'
                Session_data[user_id] = {
                    'suggests': [
                        "1",
                        "2",
                        "3",
                        "4",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
            if req['request']['original_utterance'].lower() in ['не одобряю']:
                rank -= 3
                res['response']['text'] = 'Ваш рейтинг упал  на 3.' \
                                          'На первом заседании кабинета ' \
                                          'министров объявили о том, что ' \
                                          'ВВП в этом году увеличился ' \
                                          'на 300%. Министры не сошлись ' \
                                          'во мнении,как распределить ' \
                                          'доход, и, открыв ' \
                                          'рты, ждут Вашего ' \
                                          'решения. Что делать? ' \
                                          'Возможные варианты: ' \
                                          '1) Отличные новости! Направим ресур сы на развитие науки и технологи. ' \
                                          '2) Прекрасно! Распределим деньги по' \
                                          ' частным компаниям: пусть создают новые технологии. ' \
                                          '3) Хорошо! Создадим кубышку. ' \
                                          '4) Я приказываю разделить неожиданный доход поровну между' \
                                          ' всеми гражданами нашей страны. ' \
                                          + 'Ваш рейтинг равен: ' + str(int(rank))
                current_dialog = 'first_picking_minister'
                Session_data[user_id] = {
                    'suggests': [
                        "1",
                        "2",
                        "3",
                        "4",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
        if minister == 4:
            if req['request']['original_utterance'].lower() not in ['одобряю', 'не одобряю']:
                res['response']['text'] = 'Такого выбора нет. Попробуйте ещё раз.'
                Session_data[user_id] = {
                    'suggests': [
                        "Одобряю",
                        "Не одобряю",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
            if req['request']['original_utterance'].lower() in ['одобряю']:
                rank += 5
                res['response']['text'] = 'Ваш рейтинг поднялся на 5.' \
                                          'На первом заседании кабинета ' \
                                          'министров объявили о том, что ' \
                                          'ВВП в этом году увеличился ' \
                                          'на 300%. Министры не сошлись ' \
                                          'во мнении,как распределить ' \
                                          'доход, и, открыв ' \
                                          'рты, ждут Вашего ' \
                                          'решения. Что делать? ' \
                                          'Возможные варианты: ' \
                                          '1) Отличные новости! Направим ресур сы на развитие науки и технологи. ' \
                                          '2) Прекрасно! Распределим деньги по' \
                                          ' частным компаниям: пусть создают новые технологии. ' \
                                          '3) Хорошо! Создадим кубышку. ' \
                                          '4) Я приказываю разделить неожиданный доход поровну между' \
                                          ' всеми гражданами нашей страны. ' \
                                          + 'Ваш рейтинг равен: ' + str(int(rank))
                current_dialog = 'first_picking_minister'
                Session_data[user_id] = {
                    'suggests': [
                        "1",
                        "2",
                        "3",
                        "4",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
            if req['request']['original_utterance'].lower() in ['не одобряю']:
                rank -= 3
                res['response']['text'] = 'Ваш рейтинг упал  на 3.' \
                                          'На первом заседании кабинета ' \
                                          'министров объявили о том, что ' \
                                          'ВВП в этом году увеличился ' \
                                          'на 300%. Министры не сошлись ' \
                                          'во мнении,как распределить ' \
                                          'доход, и, открыв ' \
                                          'рты, ждут Вашего ' \
                                          'решения. Что делать? ' \
                                          'Возможные варианты: ' \
                                          '1) Отличные новости! Направим ресур сы на развитие науки и технологи. ' \
                                          '2) Прекрасно! Распределим деньги по' \
                                          ' частным компаниям: пусть создают новые технологии. ' \
                                          '3) Хорошо! Создадим кубышку. ' \
                                          '4) Я приказываю разделить неожиданный доход поровну между' \
                                          ' всеми гражданами нашей страны. ' \
                                          + 'Ваш рейтинг равен: ' + str(int(rank))
                current_dialog = 'first_picking_minister'
                Session_data[user_id] = {
                    'suggests': [
                        "1",
                        "2",
                        "3",
                        "4",
                        "Рейтинг",
                        "Помощь"
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
    if current_dialog == 'first_picking_minister':
        if req['request']['original_utterance'].lower() in ['1']:
            result = 1
            rank += 5
            res['response']['text'] = 'Принятое Вами решение позволило ученым' \
                                      ' создать комплекс экологически' \
                                      ' чистых технологий, которые получили' \
                                      ' признание во всем мире. Можно' \
                                      ' применить технологии в Пранкии,' \
                                      ' можно поделиться технологиями' \
                                      ' с соседями?' \
                                      ' Что делать? Возможные варианты: ' \
                                      '1) Применить в Пранкии. Нужно заботиться о здоровье нации. ' \
                                      '2) Малую часть внедрить в Пранкии, но сделать упор на ' \
                                      'выгодной продаже другим странам. ' \
                                      '3) Отличная новость. Буду иметь ввиду, а сейчас нет денег для внедрения. ' \
                                      '4) Я расчитывал на более полезные изобретения, закрыть лаборотирию' + '' \
                                      ' Ваш рейтинг: ' + str(int(rank))
            Session_data[user_id] = {
                'suggests': [
                    "1",
                    "2",
                    "3",
                    "4",
                    "Рейтинг",
                    "Помощь"
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return



def get_suggests(user_id):
    session = Session_data[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]
    Session_data[user_id] = session
    return suggests


if __name__ == '__main__':
    app.run()
