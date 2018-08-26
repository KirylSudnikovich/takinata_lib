import argparse
from lib.controllers.user import UserController


class Arguments:
    USER = 'user'
    TASK = 'task'
    NOTICE = 'notice'
    INFO = 'info'

    ADD = 'add'
    SHOW = 'show'
    SHOW_ME = 'show_me'
    SHOW_ALL = 'show_all'
    EDIT = 'edit'
    REMOVE = 'remove'

    REG = 'reg'
    LOGIN = 'login'
    LOGOUT = 'logout'
    WHO = 'who'

    DURATION = 'duration'
    DAYS = 'days'

    ADD_SUB = 'add_sub'

    ESSENCE = 'essence'
    ACTION = 'action'

    ARCHIVE = 'archive'
    UN_ARCHIVE = 'unarchive'

    SHARE = 'share'
    UN_SHARE = 'unshare'


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(Arguments.ESSENCE, action='store', help='')
    parser.add_argument(Arguments.ACTION, action='store', nargs='*', help='add, show and etc.')

    request = parser.parse_args()
    print(process_main_request(request))


def process_main_request(request):
    if request.essence == Arguments.USER:
        return process_user_request(request)

    elif request.essence == Arguments.TASK:
        return process_task_request(request)

    elif request.essence == Arguments.NOTICE:
        return process_notice_request(request)

    # else:
    #     return MainMsg.unknown_essence(request)


def process_user_request(request):
    if request.action[0] == Arguments.REG:
        return UserController.reg(request.action[1], request.action[2], request.action[3])
    elif request.action[0] == Arguments.REMOVE:
        return UserController.delete()


main()

#
# elif request.action[0] == Arguments.EDIT:
# return user.edit(request.action[1], request.action[2])
#
# elif request.action[0] == Arguments.REMOVE:
# return user.remove(request.action[1])
#
# elif request.action[0] == Arguments.REG:
# return user.reg(request.action[1], request.action[2])
#
# elif request.action[0] == Arguments.LOGIN:
# return user.log_in(request.action[1], request.action[2])
#
# elif request.action[0] == Arguments.LOGOUT:
#     return user.log_out()
#
# elif request.action[0] == Arguments.WHO:
#     return user.who()
#
# elif request.action[0] == Arguments.SHOW_ME:
#     return 'Логин: {}\nПароль: {}\nID: {}\nОнлайн: {}'.format(*user.show_me())
#
# else:
#     return MainMsg.unknown_action(request)
#
# def process_task_request(request):
#     if request.action[0] == Arguments.ADD:
#     return task.add(request.action[1], request.action[2], request.action[3])
#
#     elif request.action[0] == Arguments.ADD_SUB:
#     return task.add_sub(request.action[1], request.action[2], request.action[3], request.action[4])
#
#     elif request.action[0] == Arguments.ARCHIVE:
#     return task.archive(request.action[1])
#
#     elif request.action[0] == Arguments.UN_ARCHIVE:
#     return task.unarchive(request.action[1])
#
#     elif request.action[0] == Arguments.SHARE:
#     return task.share(request.action[1], request.action[2])
#
#     elif request.action[0] == Arguments.UN_SHARE:
#     return task.unshare(request.action[1], request.action[2])
#
#     elif request.action[0] == Arguments.SHOW:
#     return 'Заголовок: {}\nПриоритет: {}\nОписание: {}\nДедлайн: {}\nВладелец: {}\nПользователи: {}\nID: {}\n'\
#     'PID: {}\nSID: {}\nСтатус: {}\nВремя создания: {}\nВремя редактирования: {}\nГруппа: {}\n'\
#     'Архивирована: {}\n'.format(request.action[1)
#
#     elif request.action[0] == Arguments.SHOW_ALL:
#     return 'Все задачи: {}'.format(task.show_all())
#
#     elif request.action[0] == Arguments.EDIT:
#     return task.edit(request.action[1], request.action[2], request.action[3])
#
#     elif request.action[0] == Arguments.REMOVE:
#     return task.remove(request.action[1])
#
#     else:
#     return MainMsg.unknown_action(request)
#
# def process_notice_request(request):
# if request.action[0] == Arguments.ADD:
# return notice.add(request.action[1], request.action[2], request.action[3])
#
# elif request.action[0] == Arguments.ARCHIVE:
# return notice.archive(request.action[1])
#
# elif request.action[0] == Arguments.UN_ARCHIVE:
# return notice.unarchive(request.action[1])
#
# elif request.action[0] == Arguments.SHOW:
# return notice.show(request.action[1])
#
# elif request.action[0] == Arguments.SHOW_ALL:
# return notice.show_all()
#
# elif request.action[0] == Arguments.EDIT:
# return notice.edit(request.action[1])
#
# elif request.action[0] == Arguments.REMOVE:
# return notice.remove(request.action[1])
#
# else:
# return MainMsg.unknown_action(request)
