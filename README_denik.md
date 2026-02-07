# Deníček commitů

## 2025-11-10
**Autor: vojtechvel** - Zakladní Setup
- Vytvoření základní struktury projektu
- Přidán nový model ProjectModel.py do DBDefinitions
- Přidána GraphQL definice ProjectGQLModel.py
- Vytvoření dataloader pro projekty
- Úprava query.py pro přidání projektu


**Autor: vojtechvel** - Přidání věcí do tabulky
- Rozšíření struktury databáze a dataloaderů

**Autor: otakarszaffner** - Smazání vektoru s nulami
- Vyčištění dat, odebrání prázdných/null hodnot z kolekcí

## 2025-11-24
**Autor: otakarszaffner** - Založení Souboru pro deníček
- Inicializace deníčku commitů v README_project.md
- První záznam o začátku spolupráce na projektu

**Autor: otakarszaffner** - Update README_project.md
- Úprava dokumentace projektu

## 2025-12-11
**Autor: otakarszaffner** - Opravený insert
- Oprava funkčnosti INSERT příkazů do databáze
- Vyřešení problému s vkládáním nových záznamů

## 2025-12-14
**Autor: vojtechvel** - Přidání financí a milníků
- Vytvoření nových modelů pro Finance a Milestones
- Přidání podpory financí a milníků do databázové vrstvy

**Autor: vojtechvel** - Přidání insert pro finance a milníky
- Implementace INSERT operací pro finance a milestone entity
- Umožnění vkládání nových finančních údajů a milníků

## 2025-12-15
**Autor: otakarszaffner** - Přidání testů
- Přidání testovacích funkcí
- Implementace vlastní testovací funkce
- Rozšíření test suite projektu

## 2026-01-05
**Autor: otakarszaffner** - Update ProjectGQLModel.py
- Oprava Delete a Update Mutation operací
- Zlepšení GraphQL mutací pro práci s projekty

## 2026-01-09
**Autor: vojtechvel** - Přidání atributů a cizích klíčů k databázím
- Rozšíření databázových modelů o nové atributy
- Přidání referenčních vazeb (cizí klíče) mezi tabulkami
- Zlepšení relačních vazeb v databázi

## 2026-01-12
**Autor: otakarszaffner** - Oprava a přidání dalších modulů
- Oprava chyb v existujících modulech
- Přidání dalších potřebných modulů do projektu
- Oprava diakritiky (háčky a čárky) v system.rnd.json

## 2026-01-26
**Autor: otakarszaffner** - Přidané testy pro mutace
- Implementace testů pro GraphQL mutace
- Oprava mutation update operace
- Rozšíření testů pouze pro Project entity

**Autor: vojtechvel** - Dokončení insertu a updatu pro finance a milníky
- Finalizace INSERT a UPDATE operací pro finance
- Finalizace INSERT a UPDATE operací pro milníky
- Úplná implementace CRUD operací pro tyto entity

## 2026-01-27
**Autor: otakarszaffner** - Oprava Kodu 
- Oprava chyby v kódu - chybělo ID nadřazených entit
- Vyřešení problému s referencemi mezi entitami

**Autor: otakarszaffner** - Přidal jsem komentáře do client.py
- Přidání detailních komentářů do test klienta
- Zlepšení orientace v kódu a porozumění co který test řeší
- Vylepšená dokumentace testovacích funkcí

## 2026-02-07
**Autor: vojtechvel** - Aktualizace pracovního deníku
- Přidání informací o postupu v projektu

