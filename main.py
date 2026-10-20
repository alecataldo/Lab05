import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    tipo_strumento = ft.TextField(value="Tipo")

    marca_strumento = ft.TextField(value="Marca")

    anno_acquisto = ft.TextField(value="Anno acquisto")


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    def handleAdd(e):
        currentVal = txtOut.value

        txtOut.value = currentVal + 5
        txtOut.update()

    def handleRemove(e):
        currentVal = txtOut.value
        if currentVal > 5:
            txtOut.value = currentVal - 5
            txtOut.update()
        else:
            pass

    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=handleRemove)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=handleAdd)
    txtOut = ft.TextField(
        value=0,
        width=70,
        text_align=ft.TextAlign.CENTER,
        disabled=True
    )

    def handle_conferma(e):
        tipo = tipo_strumento.value.strip()
        marca = marca_strumento.value.strip()
        anno = anno_acquisto.value.strip()
        prezzo = txtOut.value

        if not tipo or not marca or not anno or not prezzo:
            alert.show_alert(message="❌ Compilare tutti i campi")
            return

        try:
            prezzo_decimale = float(prezzo)
            anno_a=int(anno)
        except ValueError:
            alert.show_alert(message=f"❌ Errore: inserire valori numerici validi per anno e prezzo")
            return



        deposito.aggiungi_strumento(tipo, marca, anno_a, prezzo_decimale)

        aggiorna_lista_strumenti()

        tipo_strumento.value = ""
        tipo_strumento.update()
        marca_strumento.value = ""
        marca_strumento.update()
        anno_acquisto.value = ""
        anno_acquisto.update()
        txtOut.value=0
        txtOut.update()










    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO


    pulsante_aggiungi_strumento= ft.ElevatedButton(text= "Aggiungi strumento", on_click=handle_conferma)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),


        # Sezione 3
        ft.Divider(),
        ft.Text(value="Aggiungi strumento", size=20),
        ft.Row(spacing=20, controls=[tipo_strumento, marca_strumento, anno_acquisto, btnMinus, txtOut, btnAdd], alignment=ft.MainAxisAlignment.CENTER),
        pulsante_aggiungi_strumento,
        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(target=main)
