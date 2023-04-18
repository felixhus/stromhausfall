import dash_mantine_components as dmc

app.layout = dmc.Card(
    [
        dmc.LoadingOverlay(
            dmc.Container(
                [
                    dmc.TextInput(
                        label="Input 1",
                        value="",
                        placeholder="Enter value",
                    ),
                    dmc.TextInput(
                        label="Input 2",
                        value="",
                        placeholder="Enter value",
                    ),
                    dmc.Button(
                        children="Submit",
                        color="blue",
                        loading={
                            "is_loading": True,
                            "prop_name": "children",
                        },
                    ),
                ],
            ),
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
