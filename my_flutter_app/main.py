import flet as ft  # Importa la biblioteca flet para construir la interfaz de usuario.
import requests  # Importa la biblioteca requests para hacer solicitudes HTTP.
import json  # Importa la biblioteca json para trabajar con datos JSON.

# Define una clase Song para representar una canción.
class Song:
    def __init__(self, id, name, author):
        self.id = id  # Inicializa el atributo id de la canción.
        self.name = name  # Inicializa el atributo name de la canción.
        self.author = author  # Inicializa el atributo author de la canción.

# Define la función principal que se ejecuta al iniciar la aplicación.
def main(page: ft.Page):
    page.title = "My_Flutter_App"  # Establece el título de la página.
    page.theme_mode = ft.ThemeMode.SYSTEM  # Establece el modo de tema de la página según el sistema.
    page.theme = ft.Theme(color_scheme_seed=ft.colors.INDIGO)  # Establece el esquema de colores de la página.
    page.padding = 0  # Establece el padding de la página a 0.
    page.spacing = 0  # Establece el spacing de la página a 0.
    page.adaptive = True  # Habilita el modo adaptativo de la página.
    
    songs = []  # Inicializa una lista vacía para almacenar las canciones.
    selected_song = None  # Inicializa la variable selected_song como None.

    # Define una función para obtener la lista de canciones desde una API.
    def get_songs():
        nonlocal songs  # Permite modificar la variable songs definida en el ámbito externo.
        try:
            response = requests.get("https://binteapi.com:4011/api/songs/examen/2")  # Realiza una solicitud GET a la API.
            response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa.
            songs_data = response.json()  # Convierte la respuesta JSON en un diccionario.
            
            if songs_data.get("ok") and "data" in songs_data:  # Verifica si la respuesta es exitosa y contiene datos.
                songs_list = songs_data["data"]  # Obtiene la lista de canciones de los datos.
                if isinstance(songs_list, list):  # Verifica si los datos son una lista.
                    songs = [Song(str(song["id"]), song["name"], song["author"]) for song in songs_list]  # Crea instancias de Song para cada canción en la lista.
                    update_song_list()  # Actualiza la lista de canciones en la interfaz de usuario.
                else:
                    print(f"Error: 'data' no es una lista. Tipo: {type(songs_list)}")  # Imprime un mensaje de error si los datos no son una lista.
            else:
                print("Error: Estructura de respuesta inesperada o petición no exitosa")  # Imprime un mensaje de error si la estructura de la respuesta es inesperada.
        except requests.RequestException as e:  # Captura excepciones relacionadas con la solicitud HTTP.
            print(f"Error al obtener canciones: {e}")  # Imprime un mensaje de error si ocurre una excepción.
            page.snack_bar = ft.SnackBar(content=ft.Text("Error al cargar las canciones"))  # Muestra una barra de notificación con un mensaje de error.
            page.snack_bar.open = True  # Abre la barra de notificación.
            page.update()  # Actualiza la página.

    # Define una función para obtener los detalles de una canción desde una API.
    def get_song_details(song_id):
        try:
            response = requests.get(f"https://binteapi.com:4011/api/songs/examen/detail/{song_id}")  # Realiza una solicitud GET a la API con el ID de la canción.
            response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa.
            details = response.json()  # Convierte la respuesta JSON en un diccionario.
            if details.get("ok") and "data" in details:  # Verifica si la respuesta es exitosa y contiene datos.
                return details["data"]  # Retorna los datos de los detalles de la canción.
            else:
                print("Error: Estructura de respuesta inesperada o petición no exitosa")  # Imprime un mensaje de error si la estructura de la respuesta es inesperada.
                return None  # Retorna None si hay un error.
        except requests.RequestException as e:  # Captura excepciones relacionadas con la solicitud HTTP.
            print(f"Error al obtener detalles de la canción: {e}")  # Imprime un mensaje de error si ocurre una excepción.
            return None  # Retorna None si hay un error.

    # Define una función para actualizar la lista de canciones en la interfaz de usuario.
    def update_song_list():
        songs_view.controls.clear()  # Limpia los controles de la vista de canciones.
        for song in songs:  # Itera sobre la lista de canciones.
            songs_view.controls.append(  # Añade un ListTile para cada canción en la lista de controles.
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text(song.name, weight=ft.FontWeight.W_500),  # Establece el título del ListTile con el nombre de la canción.
                        subtitle=ft.Text(song.author, style=ft.TextStyle(size=12, color=ft.colors.GREY_400)),  # Establece el subtítulo del ListTile con el autor de la canción.
                        leading=ft.Icon(ft.icons.MUSIC_NOTE, color=ft.colors.INDIGO_400),  # Añade un icono de nota musical al ListTile.
                        selected=song == selected_song,  # Marca el ListTile como seleccionado si la canción es la seleccionada.
                        on_click=lambda _, s=song: show_song_details(s)  # Define la acción al hacer clic en el ListTile para mostrar los detalles de la canción.
                    ),
                    border_radius=10,  # Establece el radio del borde del contenedor.
                    ink=True,  # Habilita el efecto de tinta al hacer clic.
                    on_hover=lambda e: e.control.bgcolor == ft.colors.with_opacity(0.05, ft.colors.GREY) if e.data == "true" else None,  # Cambia el color de fondo al pasar el ratón.
                )
            )
        page.update()  # Actualiza la página.

    # Define una función para mostrar los detalles de una canción.
    def show_song_details(song):
        nonlocal selected_song  # Permite modificar la variable selected_song definida en el ámbito externo.
        selected_song = song  # Establece la canción seleccionada.
        details = get_song_details(song.id)  # Obtiene los detalles de la canción desde la API.
        if details:  # Verifica si se obtuvieron los detalles de la canción.
            page.go("/details")  # Navega a la vista de detalles.
            song_details.controls = [  # Establece los controles de la vista de detalles con la información de la canción.
                ft.Container(
                    content=ft.Column([
                        ft.Text(details.get('name', 'N/A'), size=28, weight=ft.FontWeight.BOLD),  # Muestra el nombre de la canción.
                        ft.Text(details.get('author', 'N/A'), size=18, color=ft.colors.GREY_400),  # Muestra el autor de la canción.
                        ft.Divider(height=30, color=ft.colors.GREY_400),  # Añade un divisor.
                        ft.Text("Detalles", weight=ft.FontWeight.BOLD, size=20),  # Muestra el título "Detalles".
                        ft.Text(f"Nota Musical: {details.get('music_note', 'N/A')}"),  # Muestra la nota musical de la canción.
                        ft.Text(f"Ruta de la Canción: {details.get('path_song', 'N/A')}"),  # Muestra la ruta de la canción.
                        ft.Text(f"Ruta del Video: {details.get('path_video', 'N/A')}"),  # Muestra la ruta del video.
                        ft.Text(f"Ruta del PDF: {details.get('path_pdf', 'N/A')}"),  # Muestra la ruta del PDF.
                        ft.Divider(height=30, color=ft.colors.GREY_400),  # Añade un divisor.
                        ft.Text("Letra", weight=ft.FontWeight.BOLD, size=20),  # Muestra el título "Letra".
                        ft.Container(
                            content=ft.Text(details.get('letter', 'N/A')),  # Muestra la letra de la canción.
                            bgcolor=ft.colors.with_opacity(0.05, ft.colors.GREY),  # Establece el color de fondo del contenedor.
                            border_radius=10,  # Establece el radio del borde del contenedor.
                            padding=20,  # Establece el padding del contenedor.
                        ),
                    ], scroll=ft.ScrollMode.AUTO, spacing=15),  # Crea una columna con los detalles de la canción.
                    padding=20,  # Establece el padding del contenedor.
                    expand=True,  # Expande el contenedor para ocupar todo el espacio disponible.
                )
            ]
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Error al cargar los detalles de la canción"))  # Muestra una barra de notificación con un mensaje de error.
            page.snack_bar.open = True  # Abre la barra de notificación.
        page.update()  # Actualiza la página.

    songs_view = ft.ListView(expand=1, spacing=2, padding=20)  # Crea una vista de lista para mostrar las canciones.
    song_details = ft.Column(expand=1, scroll=ft.ScrollMode.AUTO)  # Crea una columna para mostrar los detalles de la canción.

    # Define una función para manejar los cambios de ruta.
    def route_change(route):
        page.views.clear()  # Limpia las vistas de la página.
        if page.route == "/":  # Verifica si la ruta es la vista principal.
            page.views.append(  # Añade la vista principal a la página.
                ft.View(
                    "/",
                    [
                        ft.AppBar(
                            title=ft.Text("My Flutter App", weight=ft.FontWeight.BOLD),  # Añade una barra de aplicación con el título "My Flutter App".
                            center_title=True,  # Centra el título en la barra de aplicación.
                            bgcolor=ft.colors.SURFACE_VARIANT,  # Establece el color de fondo de la barra de aplicación.
                        ),
                        songs_view,  # Añade la vista de lista de canciones.
                    ],
                )
            )
        elif page.route == "/details":  # Verifica si la ruta es la vista de detalles.
            page.views.append(  # Añade la vista de detalles a la página.
                ft.View(
                    "/details",
                    [
                        ft.AppBar(
                            title=ft.Text("Detalles de la Canción", weight=ft.FontWeight.BOLD),  # Añade una barra de aplicación con el título "Detalles de la Canción".
                            center_title=True,  # Centra el título en la barra de aplicación.
                            bgcolor=ft.colors.SURFACE_VARIANT,  # Establece el color de fondo de la barra de aplicación.
                            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: page.go("/")),  # Añade un botón de retroceso para volver a la vista principal.
                        ),
                        song_details,  # Añade la columna de detalles de la canción.
                    ],
                )
            )
        page.update()  # Actualiza la página.

    page.on_route_change = route_change  # Establece la función route_change para manejar los cambios de ruta.
    page.go(page.route)  # Navega a la ruta actual de la página.

    get_songs()  # Llama a la función get_songs para obtener la lista de canciones.

ft.app(target=main)  # Inicia la aplicación llamando a la función main.