from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from utils import (
    get_summary,
    generate_icon_path,
    remove_unnecessary_info,
    beautify_stats,
)


class Covid_19(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordEventListener())


class KeywordEventListener(EventListener):
    data = get_summary()

    def on_event(self, event, extension):

        query = event.get_argument()
        results = []
        if query is None:
            req = self.data.get("Global")
            results.append(
                ExtensionResultItem(
                    name="World",
                    description="World status",
                    on_enter=HideWindowAction(),
                    icon=f"images/emoji/World.png",
                )
            )
            for key, value in req.items():
                results.append(
                    ExtensionResultItem(
                        name=beautify_stats(value),
                        description=key,
                        on_enter=HideWindowAction(),
                        icon=generate_icon_path(key),
                    )
                )
            return RenderResultListAction(results)
        elif query is not None and len(query) >= 2:

            countries = self.data.get("Countries")

            filtered_countries = list(
                filter(
                    lambda country: country.get("CountryCode") == query.upper(),
                    countries,
                )
            )

            if len(filtered_countries) == 1:

                country = dict(filtered_countries[0])
                flag_code = country.pop("CountryCode").lower()
                country = remove_unnecessary_info(country)
                for key, value in country.items():
                    if key == "Country":
                        genereated_icon = generate_icon_path(key, flag_code)
                    else:
                        genereated_icon = generate_icon_path(key)
                    results.append(
                        ExtensionResultItem(
                            name=beautify_stats(value),
                            description=key,
                            on_enter=HideWindowAction(),
                            icon=genereated_icon,
                        )
                    )
                return RenderResultListAction(results)
            else:

                results.append(
                    ExtensionResultItem(
                        name="No data found",
                        description="No country or data found. Try again!",
                        on_enter=HideWindowAction(),
                        icon=f"images/emoji/NotFound.png",
                    )
                )
                return RenderResultListAction(results)


if __name__ == "__main__":
    Covid_19().run()
