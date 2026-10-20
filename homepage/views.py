"""РџСЂРµРґСЃС‚Р°РІР»РµРЅРёСЏ РіР»Р°РІРЅРѕР№ СЃС‚СЂР°РЅРёС†С‹ Рё РѕР±С‰РµР№ РѕС€РёР±РєРё 404."""

from django.shortcuts import render


def index(request):
    """РџРѕРєР°Р·Р°С‚СЊ РіР»Р°РІРЅСѓСЋ СЃС‚СЂР°РЅРёС†Сѓ РїСЂРѕРµРєС‚Р°."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """РџРѕРєР°Р·Р°С‚СЊ РѕР±С‰СѓСЋ СЃС‚СЂР°РЅРёС†Сѓ РѕС€РёР±РєРё 404."""
    return render(request, "404.html", status=404)

