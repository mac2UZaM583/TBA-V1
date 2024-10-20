from onion.domain.g_settings_bt import settings_
from onion.app.infrastructure.g_df_test import g_df_test
from onion.infrastructure.visual import g_visualize

def main():
    data = g_df_test(settings_)
    print(data[["BT", "BT/ balance"]])

    g_visualize(
        x=data.index,
        y=data["close"],
        markers=(data["predicted_label"], data["BT"]),
        markers_settings=[
            [
                dict(
                    class_=-1,
                    color="red",
                    name="Sell",
                ),
                dict(
                    class_=1,
                    color="green",
                    name="Buy",
                )
            ],
            (
                dict(
                    class_=1,
                    color="blue",
                    name="in_position"
                ),
                dict(
                    class_=0,
                    color="pink",
                    name="not_in_position"
                ),
                dict(
                    class_=2,
                    color="yellow",
                    name="avg_order"
                )
            )
        ]
    )

if __name__ == "__main__":
    main()
