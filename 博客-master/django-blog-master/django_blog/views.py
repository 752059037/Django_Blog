# 创建人;WanChun Ye
# 创建时间 : 19.2.20  11:27
from django.shortcuts import render, get_object_or_404, reverse


def game(request):
    """
    标签
    :param request:
    :param name
    :return:
    """
    print('id: ',request)
    return render(request, 'game/game1.html')
