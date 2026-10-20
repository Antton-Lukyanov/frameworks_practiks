"""Р’СЃРїРѕРјРѕРіР°С‚РµР»СЊРЅС‹Рµ С„СѓРЅРєС†РёРё Р±РµР·РѕРїР°СЃРЅРѕРіРѕ РІРІРѕРґР°."""

from datetime import date


def input_str(prompt: str) -> str:
    """Р—Р°РїСЂРѕСЃРёС‚СЊ РЅРµРїСѓСЃС‚СѓСЋ СЃС‚СЂРѕРєСѓ."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Р’РІРѕРґ РЅРµ РјРѕР¶РµС‚ Р±С‹С‚СЊ РїСѓСЃС‚С‹Рј. РџРѕРІС‚РѕСЂРёС‚Рµ.")


def input_int(prompt: str) -> int:
    """Р—Р°РїСЂРѕСЃРёС‚СЊ С†РµР»РѕРµ С‡РёСЃР»Рѕ СЃ РѕР±СЂР°Р±РѕС‚РєРѕР№ РѕС€РёР±РѕРє."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("РќРµРєРѕСЂСЂРµРєС‚РЅС‹Р№ РІРІРѕРґ. Р’РІРµРґРёС‚Рµ С†РµР»РѕРµ С‡РёСЃР»Рѕ.")


def input_float(prompt: str) -> float:
    """Р—Р°РїСЂРѕСЃРёС‚СЊ С‡РёСЃР»Рѕ СЃ РїР»Р°РІР°СЋС‰РµР№ С‚РѕС‡РєРѕР№ СЃ РѕР±СЂР°Р±РѕС‚РєРѕР№ РѕС€РёР±РѕРє."""
    while True:
        try:
            return float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("РќРµРєРѕСЂСЂРµРєС‚РЅС‹Р№ РІРІРѕРґ. Р’РІРµРґРёС‚Рµ С‡РёСЃР»Рѕ.")


def input_date(prompt: str) -> str:
    """Р—Р°РїСЂРѕСЃРёС‚СЊ РґР°С‚Сѓ РІ С„РѕСЂРјР°С‚Рµ Р“Р“Р“Р“-РњРњ-Р”Р” СЃ РѕР±СЂР°Р±РѕС‚РєРѕР№ РѕС€РёР±РѕРє."""
    while True:
        raw = input(prompt).strip()
        try:
            return date.fromisoformat(raw).isoformat()
        except ValueError:
            print("РќРµРєРѕСЂСЂРµРєС‚РЅС‹Р№ С„РѕСЂРјР°С‚ РґР°С‚С‹. РћР¶РёРґР°РµС‚СЃСЏ Р“Р“Р“Р“-РњРњ-Р”Р”.")

