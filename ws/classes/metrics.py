from collections import OrderedDict
from datetime import datetime, date, time, timedelta


class Metric:
    @staticmethod
    def get_top_users(users_list):
        """Returns chatbot's tops users as a list of ordered 
        dictionaries.

        Keyword arguments:
        users_list -- list of chatbot's top users
        """

        # Variables locales
        users = []  # Lista de listas de tuplas

        for user in users_list:
            new_user = []  # Lista de tuplas
            new_user.append(('usuario', user[0]))
            new_user.append(('cantidad_mensajes', user[1]))

            users.append(OrderedDict(new_user))

        return users

    @staticmethod
    def get_users_amount_by_date(users_amounts):
        """Returns chatbot's users amounts by date as a list of ordered
         dictionaries.

        Keyword arguments:
        users_amounts -- list of chatbot's users amounts by date
        """

        # Variables locales
        amounts_by_date = []  # Lista de listas de tuplas

        for amount in users_amounts:
            new_amount = []  # Lista de tuplas
            new_amount.append(('fecha', amount[0]))
            new_amount.append(('cantidad_usuarios', amount[1]))

            amounts_by_date.append(OrderedDict(new_amount))

        return amounts_by_date

    @staticmethod
    def get_keywords_usage_count(keywords_list):
        """Returns bubbles' keywords and its usage amount as a list of 
        ordered dictionaries.

        Keyword arguments:
        keywords_list -- list of bubbles' keywords
        """

        # Variables locales
        keywords_and_usage = []  # Lista de listas de tuplas

        for keyword in keywords_list:
            new_keyword = []  # Lista de tuplas
            new_keyword.append(('palabra_clave', keyword[0]))
            new_keyword.append(('cantidad_usos', keyword[1]))

            keywords_and_usage.append(OrderedDict(new_keyword))

        return keywords_and_usage

    @staticmethod
    def get_sessions_time(messages_list, max_session_time, sessions_details):
        """Returns sessions statistics as a list of ordered 
        dictionaries.

        Keyword arguments:
        messages_list -- list of messages;
        max_session_time -- session time limit in seconds;
        sessions_details -- sets whether detail users sessions or not
        """

        # Variables locales
        current_id = ""
        oldest_date = ""
        newest_date = ""
        sessions = {}
        durations_sum = 0
        session_counter = 0
        users_counter = 0
        i = 0
        
        # Por cada usuario
        while i in range(len(messages_list)):
            j = i
            user_id = messages_list[i][0]
            current_id = user_id
            if sessions_details:
                sessions[user_id] = []

            # Por cada sesión del usuario
            while user_id == current_id and j in range(len(messages_list)):
                k = j
                oldest_date = datetime.strptime(messages_list[j][1], '%Y/%m/%d %H:%M:%S')
                newest_date = oldest_date
                diff = timedelta.total_seconds(newest_date - oldest_date)
                if j + 1 in range(len(messages_list)):
                    f2 = datetime.strptime(messages_list[j + 1][1], '%Y/%m/%d %H:%M:%S')
                    diff = timedelta.total_seconds(f2 - oldest_date)
                
                # Por cada mensaje de la sesión
                while diff < max_session_time and user_id == current_id and k in range(len(messages_list)):
                    newest_date = datetime.strptime(messages_list[k][1], '%Y/%m/%d %H:%M:%S')
                    diff = 0
                    k += 1
                    # No es el fin de la lista
                    if k in range(len(messages_list)):
                        f2 = datetime.strptime(messages_list[k][1], '%Y/%m/%d %H:%M:%S')
                        diff = timedelta.total_seconds(f2 - newest_date)
                        current_id = messages_list[k][0]
                
                session_dur = timedelta.total_seconds(newest_date - oldest_date)
                durations_sum += session_dur
                session_counter += 1
                if sessions_details:
                    sessions[user_id].append({
                        'oldest_date': oldest_date.strftime('%Y/%m/%d %H:%M:%S'),
                        'newest_date': newest_date.strftime('%Y/%m/%d %H:%M:%S'),
                        'seconds': session_dur
                    })
                j = k if k != j else k + 1  # k == j significa que se salto el 'while' anterior
                if j in range(len(messages_list)):
                    current_id = messages_list[j][0]
            
            users_counter += 1
            i = j
        
        sessions['sessions'] = session_counter
        sessions['users'] = users_counter
        sessions['average_seconds'] = durations_sum / session_counter
        sessions['average_minutes'] = (durations_sum / session_counter) / 60

        return sessions

    @staticmethod
    def get_interactions(interactions_list):
        """Returns interactions as a dictionary.

        Keyword arguments:
        interactions_list -- list of interactions
        """

        # Variables locales
        interactions = {}

        for interaction in interactions_list:
            if interaction[0] not in interactions:
                interactions[interaction[0]] = []
            interactions[interaction[0]].append({
                '{}'.format(interaction[1]): {
                    'cant_mensajes': interaction[2],
                    'cant_usuarios': interaction[3]
                }
            })

        return interactions
    
    @staticmethod
    def get_forms(forms_list):
        """
        """

        # Variables locales
        forms = {}

        for form in forms_list:
            # if form[0] not in forms:
            #     forms[form[0]] = []
            forms[form[0]] = {
                '{}'.format(form[1]): {
                    'cant_formularios': form[2],
                    'cant_usuarios': form[3]
                }
            }
        
        return forms