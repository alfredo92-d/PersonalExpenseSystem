/* ============================================================
   PROGETTO: Sistema Gestione Spese Personali e Budget
   DB: GestioneSpese
   TABELLE: categorie, spese, budget
   ============================================================ */

-- 1) Creazione database
DROP DATABASE IF EXISTS GestioneSpese;
CREATE DATABASE GestioneSpese
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE GestioneSpese;

-- 2) Eliminazione tabelle (ordine corretto per le FK)
DROP TABLE IF EXISTS spese;
DROP TABLE IF EXISTS budget;
DROP TABLE IF EXISTS categorie;

-- 3) Tabella CATEGORIE
CREATE TABLE categorie (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(50) NOT NULL,
  CONSTRAINT uq_categoria_nome UNIQUE (nome)
);

-- 4) Tabella SPESE
CREATE TABLE spese (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  data DATE NOT NULL,
  importo DECIMAL(10,2) NOT NULL,
  categoria_id INT UNSIGNED NOT NULL,
  descrizione VARCHAR(255) NULL,

  CONSTRAINT chk_importo_spesa CHECK (importo > 0),

  CONSTRAINT fk_spese_categoria
    FOREIGN KEY (categoria_id)
    REFERENCES categorie(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

-- 5) Tabella BUDGET
CREATE TABLE budget (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  mese CHAR(7) NOT NULL,          -- formato YYYY-MM
  categoria_id INT UNSIGNED NOT NULL,
  importo DECIMAL(10,2) NOT NULL,

  CONSTRAINT chk_importo_budget CHECK (importo > 0),

  -- un solo budget per mese + categoria
  CONSTRAINT uq_budget_mese_categoria UNIQUE (mese, categoria_id),

  CONSTRAINT fk_budget_categoria
    FOREIGN KEY (categoria_id)
    REFERENCES categorie(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

-- ============================================================
-- DATI DI ESEMPIO (dimostrano che il sistema funziona)
-- ============================================================

INSERT INTO categorie (nome) VALUES
('Alimentari'),
('Trasporti');

-- Spese di esempio (Alimentari = id 1, Trasporti = id 2)
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES
('2026-02-01', 10.00, 1, 'pane'),
('2026-02-02', 2.50, 2, 'bus');

-- Budget di esempio
INSERT INTO budget (mese, categoria_id, importo) VALUES
('2026-02', 1, 300.00),
('2026-02', 2, 60.00);

-- ============================================================
-- ESEMPI DI VINCOLI (NON eseguire: servono solo come prova)
-- ============================================================

-- 1) CHECK importo spesa > 0 (fallisce)
-- INSERT INTO spese (data, importo, categoria_id, descrizione)
-- VALUES ('2026-02-03', -5.00, 1, 'errore');

-- 2) FOREIGN KEY: categoria_id deve esistere (fallisce se 999 non esiste)
-- INSERT INTO spese (data, importo, categoria_id, descrizione)
-- VALUES ('2026-02-03', 5.00, 999, 'errore');

-- 3) UNIQUE su categorie.nome (fallisce se duplicato)
-- INSERT INTO categorie (nome) VALUES ('Alimentari');

-- 4) UNIQUE su budget (mese, categoria_id) (fallisce se duplicato)
-- INSERT INTO budget (mese, categoria_id, importo) VALUES ('2026-02', 1, 999.00);