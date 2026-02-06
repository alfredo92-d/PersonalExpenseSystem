import sys

from db import get_connection, add_categoria, add_spesa, set_budget


conn = get_connection()
if conn:
    print("✅ Connessione OK!")
    conn.close()
else:
    print("❌ Connessione fallita")

    print("Benvenuto nel Sistema di Gestione\n"
      "Spese e Budget di Alfredo Di Modica\n")


#funzione menuPrincipale
def menuPrincipale():

    while True:
        print("\nMENU PRINCIPALE\n"
          "1. Gestione Categorie\n"
          "2. Inserisci Spesa\n"
          "3. Definisci Budget Mensile\n"
          "4. Visualizza Report\n"
          "5. Esci\n")

        scelta = input("Scegli una opzione del menu: ").strip()

        while not scelta.isdigit() or not (1 <= int(scelta) <= 5):
            scelta = input("Scelta non valida. Riprovare: ").strip()

        print(f"La tua scelta finale è: {scelta}\n")
        if scelta == "1":
            nome = input("Inserisci il nome della categoria: ").strip()

            while nome == "":
                nome = input("Nome non valido. Riprovare: ").strip()

            if add_categoria(nome):
                print("✅ Categoria aggiunta con successo!")
            else:
                print("❌ Errore: categoria già esistente!")


        elif scelta == "2":
            # 1) Acquisizione input
            data_spesa = input("Inserisci la data (YYYY-MM-DD): ").strip()
            importo_str = input("Inserisci l'importo: ").strip().replace(",", ".")
            nome_categoria = input("Inserisci il nome della categoria: ").strip()
            descrizione = input("Inserisci una descrizione (facoltativa): ").strip()

            # descrizione facoltativa -> se vuota mettiamo None
            if descrizione == "":
                descrizione = None

            # 2) Validazione importo
            try:
                importo = float(importo_str)
            except ValueError:
                print("Errore: importo non valido.")
                importo = None

            if importo is None or importo <= 0:
                print("Errore: l'importo deve essere maggiore di zero.")
            else:
                conn = get_connection()
                cursor = conn.cursor(buffered=True)

                # 3) Verifica esistenza categoria (SQL SELECT)
                cursor.execute("SELECT id FROM categorie WHERE nome = %s", (nome_categoria,))
                row = cursor.fetchone()

                if row is None:
                    print("Errore: la categoria non esiste!")
                else:
                    categoria_id = row[0]

                    # 4) Inserimento spesa (SQL INSERT con chiave esterna)
                    cursor.execute(
                        "INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES (%s, %s, %s, %s)",
                        (data_spesa, importo, categoria_id, descrizione)
                    )
                    conn.commit()
                    print("Spesa inserita correttamente!")

                cursor.close()
                conn.close()


        elif scelta == "3":
            import re

            mese = input("Inserisci il mese (YYYY-MM): ").strip().replace("/", "-")
            if not re.match(r"^\d{4}-\d{2}$", mese):
                print("❌ Formato mese non valido. Usa YYYY-MM (es. 2026-02).")
                raise SystemExit()

            nome_categoria = input("Inserisci il nome della categoria: ").strip()

            importo_str = input("Inserisci l'importo del budget: ").strip().replace(",", ".")
            try:
                importo = float(importo_str)
            except ValueError:
                print("❌ Importo non valido.")
                raise SystemExit()

            ok = set_budget(mese, nome_categoria, importo)
            if ok:
                print("✅ Budget mensile salvato correttamente.")
            else:
                print("❌ Impossibile salvare il budget.")

        elif scelta == "4":
            while True:
                print("\nMENU REPORT")
                print("1. Totale spese per categoria")
                print("2. Spese mensili vs budget")
                print("3. Elenco completo delle spese ordinate per data")
                print("4. Ritorna al menu principale")

                scelta_report = input("Scegli un report: ").strip()

                if scelta_report == "1":
                    conn = get_connection()
                    cursor = conn.cursor()

                    query = """
                            SELECT c.nome, SUM(s.importo)
                            FROM spese s
                                     JOIN categorie c ON s.categoria_id = c.id
                            GROUP BY c.nome \
                            """

                    cursor.execute(query)
                    risultati = cursor.fetchall()

                    print("\nCategoria........Totale Speso")
                    for nome, totale in risultati:
                        print(f"{nome:<20} {totale:.2f}")

                    cursor.close()
                    conn.close()

                elif scelta_report == "2":
                    mese = input("Inserisci il mese (YYYY-MM): ").strip()
                    nome_categoria = input("Inserisci il nome della categoria: ").strip()

                    conn = get_connection()
                    cursor = conn.cursor(buffered=True)

                    # Recupero id categoria
                    cursor.execute(
                        "SELECT id FROM categorie WHERE nome = %s",
                        (nome_categoria,)
                    )
                    row = cursor.fetchone()

                    if not row:
                        print("Errore: la categoria non esiste!")
                    else:
                        categoria_id = row[0]

                        # Totale speso nel mese per categoria
                        cursor.execute("""
                                       SELECT COALESCE(SUM(importo), 0)
                                       FROM spese
                                       WHERE categoria_id = %s
                                         AND DATE_FORMAT(data, '%Y-%m') = %s
                                       """, (categoria_id, mese))
                        speso = cursor.fetchone()[0]

                        # Recupero budget
                        cursor.execute("""
                                       SELECT importo
                                       FROM budget
                                       WHERE categoria_id = %s
                                         AND mese = %s
                                       """, (categoria_id, mese))
                        row_budget = cursor.fetchone()

                        if not row_budget:
                            print("Nessun budget definito per questa categoria e mese.")
                        else:
                            budget = row_budget[0]

                            print(f"\nMese: {mese}")
                            print(f"Categoria: {nome_categoria}")
                            print(f"Budget: {budget:.2f}")
                            print(f"Speso: {speso:.2f}")

                            if speso > budget:
                                print("Stato: SUPERAMENTO BUDGET")
                            else:
                                print("Stato: OK")

                    cursor.close()
                    conn.close()
                elif scelta_report == "3":
                    conn = get_connection()
                    cursor = conn.cursor(buffered=True)

                    cursor.execute("""
                                   SELECT s.data, c.nome, s.importo, s.descrizione
                                   FROM spese s
                                            JOIN categorie c ON s.categoria_id = c.id
                                   ORDER BY s.data ASC, s.id ASC
                                   """)
                    righe = cursor.fetchall()

                    print("\nData        Categoria           Importo")
                    print("----------------------------------------")

                    for data, categoria, importo, descrizione in righe:
                        print(f"{data}  {categoria:<18}  {importo:>7.2f}")
                        if descrizione is not None and descrizione.strip() != "":
                            print(f"{descrizione}")

                    cursor.close()
                    conn.close()

                elif scelta_report == "4":
                    #tornare al menu principale
                    menuPrincipale()
                    #break
                else:
                    print("Scelta non valida. Riprovare!")

        elif scelta == "5":

            risposta = input("Vuoi Uscire dal programma? si o no\n")

            if risposta == "si":
                sys.exit()


menuPrincipale()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/