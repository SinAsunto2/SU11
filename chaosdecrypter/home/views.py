from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import CustomUser
from django.http import HttpResponseBadRequest
from .models import Challenge, CompletedChallenge, ChatMessage, Secrets, CompletedSecrets
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required()
def index(request):
    context = {
        'active_page': 'index',
    }
    return render(request, 'index.html', context)


def ranking(request):
    ranked_users = CustomUser.objects.exclude(username='bot_libur').order_by('-score')[:100]

    context = {
        'active_page': 'ranking',
        'ranked_users': ranked_users,
    }

    return render(request, 'ranking.html', context)


@login_required()
def challenges(request):
    user = request.user

    has_previos_interaction = CompletedChallenge.objects.filter(user=user).exists()

    all_challenges = Challenge.objects.all().count()
    all_completed_challenges = CompletedChallenge.objects.filter(user=user).count()

    all_secrets = Secrets.objects.all().count()
    all_completed_secrets = CompletedSecrets.objects.filter(user=user).count()

    avatar_bot = CustomUser.objects.get(username='bot_libur')

    ranked_users = CustomUser.objects.order_by('-score')
    user_ranking_position = list(ranked_users).index(user) + 1

    next_challenge = Challenge.objects.exclude(completedchallenge__user=user).order_by('id').first()


    user_state = {
        'username': user.username,
        'score': user.score,
        'all_challenges': all_challenges,
        'all_completed_challenges': all_completed_challenges,
        'next_challenge': next_challenge,
        'all_secrets': all_secrets,
        'all_completed_secrets': all_completed_secrets,
    }

    context = {
        'active_page': 'challenges',
        'user_state': user_state,
        'has_previos_interaction': has_previos_interaction,
        'avatar_bot': avatar_bot.profile_picture.url,
        'user_ranking_position': user_ranking_position,
    }

    # print(context)
    return render(request, 'challenges.html', context)


@login_required()
def handle_user_response(request):
    user = request.user

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user_response = request.POST.get('user_response', '').strip().lower()

        # Guardar el mensaje del usuario en la base de datos
        user_message = ChatMessage(sender=request.user, content=user_response)
        user_message.save()

        bot_user = CustomUser.objects.get(username='bot_libur')

        # -------------------------------
        #          RETO NO. 1
        # -------------------------------
        if user_response == 'reto1' or user_response == 'reto 1':
            current_challenge = Challenge.objects.get(id=1)
            challenge_completed = CompletedChallenge.objects.filter(user=user, challenge=current_challenge).exists()
            if not challenge_completed:
                challenge_message = current_challenge.description
                challenge_image_path = 'images/1.PNG'

                # Obtener el ID del desafío actual almacenado en la sesión
                current_challenge_id = request.session.get('current_challenge_id')

                # Construir la URL completa para la imagen
                challenge_image_url = request.build_absolute_uri(default_storage.url(challenge_image_path))

                # Guardar el mensaje del bot en la base de datos
                bot_message = ChatMessage(sender=bot_user, content=challenge_message)
                bot_message.save()

                print("\n1 - Contenido de request.session:", dict(request.session))

                if current_challenge_id != current_challenge.id:
                    # Inicializar el tiempo de inicio del reto
                    request.session['tiempo_inicio_reto'] = timezone.now().isoformat()

                    # Almacenar el ID del desafío actual en la sesión
                    request.session['current_challenge_id'] = current_challenge.id

                print("1.1 - Contenido de request.session:", dict(request.session))

                return JsonResponse({'message': challenge_message, 'challenge_image': challenge_image_url})
            else:
                return JsonResponse({'message': 'Ey ya completaste este reto!'})
        
        # -------------------------------
        #          RETO NO. 1 - ANSWER
        # -------------------------------
        elif user_response == 'bad eyes' or user_response == 'badeyes':
            current_challenge = Challenge.objects.get(id=1)

            # Calcular el tiempo que tardó el usuario en responder
            tiempo_inicio_reto = timezone.datetime.fromisoformat(request.session.get('tiempo_inicio_reto'))
            tiempo_inactivo_minutos = obtener_tiempo_inactivo(tiempo_inicio_reto)

            # Calcular puntos ganados basados en el tiempo invertido
            puntos_ganados = calcular_puntos_ganados(tiempo_inactivo_minutos)

            # Sumar los puntos al usuario
            request.user.score += puntos_ganados
            request.user.save()

            # Guardar el reto completado en la base de datos
            completed_challenge = CompletedChallenge(user=request.user, challenge=current_challenge)
            completed_challenge.save()

            completed_message = """
            <p>¡Felicidades, intrépido aventurero! 🎉</p>
            <p>Has superado con maestría el primer desafío. Tu ingenio es tan brillante como las estrellas. ✨<br>
            Sigue desentrañando misterios y desafiando los límites. El caos no tiene nada contra ti. 🌌🤯<br>
            ¡Estamos emocionados de ver qué maravillas conquistarás a continuación en tu viaje en SU11! 🚀 ¡Bien hecho! 🏆</p>

            <p>¡El próximo desafío te espera! 🚀 Escribe <strong>RETO2</strong> para iniciar la próxima hazaña. 🔍👊</p>

            """

            return JsonResponse({'message': completed_message})

        # -------------------------------
        #          RETO NO. 2
        # -------------------------------
        elif user_response == 'reto2' or user_response == 'reto 2':
            current_challenge = Challenge.objects.get(id=2)

            # Verificar si los desafíos anteriores han sido completados
            challenges_completed = CompletedChallenge.objects.filter(user=user, challenge__id__lt=current_challenge.id).count()

            if challenges_completed < current_challenge.id - 1:
                return JsonResponse({'message': 'Primero debes completar los desafíos anteriores.'})
            else:
                challenge_completed = CompletedChallenge.objects.filter(user=user, challenge=current_challenge).exists()
                if not challenge_completed:
                    challenge_message = current_challenge.description

                    # Obtener el ID del desafío actual almacenado en la sesión
                    current_challenge_id = request.session.get('current_challenge_id')

                    # Guardar el mensaje del bot en la base de datos
                    bot_message = ChatMessage(sender=bot_user, content=challenge_message)
                    bot_message.save()

                    print("\n2 - Contenido de request.session:", dict(request.session))

                    if current_challenge_id != current_challenge.id:
                        # Inicializar el tiempo de inicio del reto
                        request.session['tiempo_inicio_reto'] = timezone.now().isoformat()

                        # Almacenar el ID del desafío actual en la sesión
                        request.session['current_challenge_id'] = current_challenge.id

                    print("2.2 - Contenido de request.session:", dict(request.session))

                    return JsonResponse({'message': challenge_message})
                else:
                    return JsonResponse({'message': 'Ey ya completaste este reto!'})
        
        # -------------------------------
        #          RETO NO. 2 ANSWER
        # -------------------------------
        elif user_response == '13112221':
            current_challenge = Challenge.objects.get(id=2)

            # Calcular el tiempo que tardó el usuario en responder
            tiempo_inicio_reto = timezone.datetime.fromisoformat(request.session.get('tiempo_inicio_reto'))
            tiempo_inactivo_minutos = obtener_tiempo_inactivo(tiempo_inicio_reto)

            # Calcular puntos ganados basados en el tiempo invertido
            puntos_ganados = calcular_puntos_ganados(tiempo_inactivo_minutos)

            # Sumar los puntos al usuario
            request.user.score += puntos_ganados
            request.user.save()

            # Guardar el reto completado en la base de datos
            completed_challenge = CompletedChallenge(user=request.user, challenge=current_challenge)
            completed_challenge.save()

            completed_message = """
            <p>¡Excelente trabajo en el segundo desafío! 🌟</p>
            <p>¿Listo para el siguiente reto? Escribe <strong>RETO3</strong> y descubre lo que sigue. ¡Adelante, sigue brillando! 🚀🔍</p>
            """
            return JsonResponse({'message': completed_message})
        
        # -------------------------------
        #          RETO NO. 3
        # -------------------------------
        elif user_response == 'reto3' or user_response == 'reto 3':
            current_challenge = Challenge.objects.get(id=3)

            # Verificar si los desafíos anteriores han sido completados
            challenges_completed = CompletedChallenge.objects.filter(user=user, challenge__id__lt=current_challenge.id).count()

            if challenges_completed < current_challenge.id - 1:
                return JsonResponse({'message': 'Primero debes completar los desafíos anteriores.'})
            else:
                challenge_completed = CompletedChallenge.objects.filter(user=user, challenge=current_challenge).exists()
                if not challenge_completed:
                    challenge_message = current_challenge.description

                    # Obtener el ID del desafío actual almacenado en la sesión
                    current_challenge_id = request.session.get('current_challenge_id')

                    # Guardar el mensaje del bot en la base de datos
                    bot_message = ChatMessage(sender=bot_user, content=challenge_message)
                    bot_message.save()

                    print("\n2 - Contenido de request.session:", dict(request.session))

                    if current_challenge_id != current_challenge.id:
                        # Inicializar el tiempo de inicio del reto
                        request.session['tiempo_inicio_reto'] = timezone.now().isoformat()

                        # Almacenar el ID del desafío actual en la sesión
                        request.session['current_challenge_id'] = current_challenge.id

                    print("2.2 - Contenido de request.session:", dict(request.session))

                    return JsonResponse({'message': challenge_message})
                else:
                    return JsonResponse({'message': 'Ey ya completaste este reto!'})

        # -------------------------------
        #          RETO NO. 3 ANSWER
        # -------------------------------
        elif user_response == 'umbra':
            current_challenge = Challenge.objects.get(id=3)

            # Calcular el tiempo que tardó el usuario en responder
            tiempo_inicio_reto = timezone.datetime.fromisoformat(request.session.get('tiempo_inicio_reto'))
            tiempo_inactivo_minutos = obtener_tiempo_inactivo(tiempo_inicio_reto)

            # Calcular puntos ganados basados en el tiempo invertido
            puntos_ganados = calcular_puntos_ganados(tiempo_inactivo_minutos)

            # Sumar los puntos al usuario
            request.user.score += puntos_ganados
            request.user.save()

            # Guardar el reto completado en la base de datos
            completed_challenge = CompletedChallenge(user=request.user, challenge=current_challenge)
            completed_challenge.save()

            completed_message = """
            <p>¡Increíble desempeño en el tercer desafío! 🎉</p>
            <p>¿Te animas con el Reto 4? Escribe <strong>RETO4</strong> y continúa explorando. ¡La emoción no para! 🔍🗝️</p>
            """
            return JsonResponse({'message': completed_message})
        
        # -------------------------------
        #          RETO NO. 4
        # -------------------------------
        elif user_response == 'reto4' or user_response == 'reto 4':
            current_challenge = Challenge.objects.get(id=4)

            # Verificar si los desafíos anteriores han sido completados
            challenges_completed = CompletedChallenge.objects.filter(user=user, challenge__id__lt=current_challenge.id).count()

            if challenges_completed < current_challenge.id - 1:
                return JsonResponse({'message': 'Primero debes completar los desafíos anteriores.'})
            else:
                challenge_completed = CompletedChallenge.objects.filter(user=user, challenge=current_challenge).exists()
                if not challenge_completed:
                    challenge_message = current_challenge.description
                    challenge_image_path = 'images/2.PNG'

                    # Construir la URL completa para la imagen
                    challenge_image_url = request.build_absolute_uri(default_storage.url(challenge_image_path))

                    # Obtener el ID del desafío actual almacenado en la sesión
                    current_challenge_id = request.session.get('current_challenge_id')

                    # Guardar el mensaje del bot en la base de datos
                    bot_message = ChatMessage(sender=bot_user, content=challenge_message)
                    bot_message.save()

                    print("\n2 - Contenido de request.session:", dict(request.session))

                    if current_challenge_id != current_challenge.id:
                        # Inicializar el tiempo de inicio del reto
                        request.session['tiempo_inicio_reto'] = timezone.now().isoformat()

                        # Almacenar el ID del desafío actual en la sesión
                        request.session['current_challenge_id'] = current_challenge.id

                    print("2.2 - Contenido de request.session:", dict(request.session))

                    return JsonResponse({'message': challenge_message, 'challenge_image': challenge_image_url})
                else:
                    return JsonResponse({'message': 'Ey ya completaste este reto!'})

        # -------------------------------
        #          RETO NO. 4 ANSWER
        # -------------------------------
        elif user_response == 'andromeda' or user_response == 'andrómeda':
            current_challenge = Challenge.objects.get(id=4)

            # Calcular el tiempo que tardó el usuario en responder
            tiempo_inicio_reto = timezone.datetime.fromisoformat(request.session.get('tiempo_inicio_reto'))
            tiempo_inactivo_minutos = obtener_tiempo_inactivo(tiempo_inicio_reto)

            # Calcular puntos ganados basados en el tiempo invertido
            puntos_ganados = calcular_puntos_ganados(tiempo_inactivo_minutos)

            # Sumar los puntos al usuario
            request.user.score += puntos_ganados
            request.user.save()

            # Guardar el reto completado en la base de datos
            completed_challenge = CompletedChallenge(user=request.user, challenge=current_challenge)
            completed_challenge.save()

            completed_message = """
            <p>¡Estás en fuego! 🔥</p>
            <p>¿Preparado para el Reto 5? Escribe <strong>RETO5</strong> y descubre lo que aguarda. ¡Sigue brillando en este viaje! 🔍🌑</p>
            """
            return JsonResponse({'message': completed_message})

        else:
            # Guardar el mensaje de respuesta del usuario en la base de datos
            bot_message = ChatMessage(sender=bot_user, content='¡Ups! Comando o respuesta incorrectos. 🤔 Inténtalo de nuevo, por favor.')
            bot_message.save()

            return JsonResponse({'message': '¡Ups! Comando o respuesta incorrectos. 🤔 Inténtalo de nuevo, por favor.'})

    # Si no es una solicitud Ajax, devolver un HttpResponseBadRequest
    return HttpResponseBadRequest('Esta vista solo maneja solicitudes Ajax.')
    

def obtener_tiempo_inactivo(tiempo_inicio):
    # Calcula el tiempo inactivo en minutos desde el tiempo de inicio hasta ahora
    tiempo_actual = timezone.now()
    tiempo_inactivo = (tiempo_actual - tiempo_inicio).total_seconds() / 60.0
    return tiempo_inactivo


def calcular_puntos_ganados(tiempo_inactivo_minutos):
    # Calcular puntos ganados basados en la rapidez de la respuesta
    puntos_base = 100
    puntos_descontados = min(5 * tiempo_inactivo_minutos, puntos_base)
    puntos_ganados = max(puntos_base - puntos_descontados, 0)
    
    # Agregar un bono de 30 puntos si el usuario queda con 0 puntos
    if puntos_ganados == 0:
        puntos_ganados += 30
    
    return int(puntos_ganados)





# @login_required
# def chat_history(request):
#     # Recupera el historial de mensajes del usuario actual
#     user_messages = ChatMessage.objects.filter(sender=request.user).order_by('timestamp')

#     # Recupera el historial de mensajes del bot
#     bot_messages = ChatMessage.objects.filter(sender__isnull=True).order_by('timestamp')

#     # Combina los mensajes del usuario y del bot
#     all_messages = sorted(list(user_messages) + list(bot_messages), key=lambda x: x.timestamp)

#     context = {'messages': all_messages}

#     return render(request, 'chat_history.html', context)