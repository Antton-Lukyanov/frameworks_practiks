#!/usr/bin/env python
"""РЈС‚РёР»РёС‚Р° РєРѕРјР°РЅРґРЅРѕР№ СЃС‚СЂРѕРєРё РґР»СЏ СѓРїСЂР°РІР»РµРЅРёСЏ Django-РїСЂРѕРµРєС‚РѕРј."""

import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_service.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django РЅРµ СѓСЃС‚Р°РЅРѕРІР»РµРЅ. РЈСЃС‚Р°РЅРѕРІРёС‚Рµ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё: "
            "pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

