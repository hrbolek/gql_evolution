# GQL_TV

__Ondřej Begy__ 
________________________________________________________________________

## Popis

Projekt vytvoření backendu databází pro systém, který zahrnuje požadavky stanovené CTVS. Tento systém je následně součástí UOIS. Základem jsou nejdůležitější funkce systému pro potřeby CTVS. V budoucnosti je zde možnost systém rozšířit o další moduly a postupně jej vylepšovat a přidávat další funkce.

Mezi požadavky tohoto systému patří:

- výpis údajů o studentovi (pohlaví, rok narození, výsledky přezkoušení atd.)
- přehled studentů, kteří jsou přiřazení k učební skupině
- zapisování výsledků z přezkoušení a udělování zápočtu
- editace výsledků pouze pro uživatele s oprávněním (tělocvikář přidělený ke skupině)
- editace disciplíny pro jednotlivé učební skupiny či studenty
- záznam o prodloužení zápočtu u studenta
- student má možnost podívat se na své výsledky (pravděpodobně řešeno skrze gql_users?)
- záznam a historie editace disciplín a výsledků (řešeno skrze UOIS)

## Struktura systému
Žlutě znázorněné databáze jsou základ systému pro CTVS.

<img src="database-structure.png" alt="Chyba">

Zdroj: RÁČIL, Tomáš. IS pro sběr a vyhodnocení vybraných anatomicko- fyziologických dat a výzkumů. DIPLOMOVÁ PRÁCE. BRNO: UNIVERZITA OBRANY V BRNĚ, 2020.

Zde bude umístěná aktualizovaná struktura systému:

## Požadavky

- všechny typy, input typy (s vyjímkou filtrů), mají description = **splněno**
- všechny GQL typy mají private attribut _data, což je odpovídající db řádek (neplatí pro extended types) = **splněno**
- všechny GQL typy a odpovídající DB modely mají atributy 
    lastchange
    created
    changedby_id
    createby_id
    rbacobject_id = **splněno**
- vektorové atributy mají volitelné parametry where, limit a skip (je možné se domluvit na výjimce) a mají alternativu podle standardu relay connection = **chybí where a alternativa**
- součástí filtrů (where) bude primární klíč i cizí klíče = **splněno?**
- počáteční import dat je realizován jako asynchronní task:
task = asyncio.create_task(initDB(asyncSessionMaker)) = **splněno**
- mutace upravit tak, aby používaly
from uoishelpers.resolvers import encapsulateInsert, encapsulateUpdate, encapsulateDelete
(je možné se domluvit na výjimce) = **splněno?**
- všechny typy, inputs, apod. mají description = **splněno**
- všechny atributy mají anotace, např. Annotated[Optional[str], strawberry.argument(description="")]="0" = **splněno**
- u všech fields jsou permission classes a v komentáři uvedeno, kdo má k atributu či funkcionalitě přístup = **nesplněno**
- testy s alespoň 90% pokrytím pomocí dotazů, ty jsou uloženy v systému souborů (read.gql, create.gql, …) = **nesplněno**

________________________________________________________________________

## Úkoly

- udělat návrh databází = **hotovo**
- vytvořit tabulky databází = **hotovo**
- vytvořit GQL modely databází = **hotovo**
- odstranit chyby v propojení GQL modelů = **hotovo**
- předělat systemadata.json (jeden uživatel s jedním výsledkem) = **hotovo**
- vytvořit a zprovoznit READ operace pro jedotlivé GQL modely = **hotovo**
- vytvořit a zprovoznit CUD operace pro jednotlivé GQL modely = **hotovo**
- vytvořit a zprovoznit testy s minimálním 90 % pokrytím dotazů = **nesplněno**

________________________________________________________________________

## Záznamy

- 4.11. = základní návrh databáze
- 14.11. = zprovoznění GQL, Voyageru, drobné úpravy v kódu
- 25.11. = vytvoření systemdata.json a odstranění chyb v rámci propojení GQL modelů
- 5.12. = zprovnění READ operací pro každý GQL model
- 18.12. = zprovoznění CUD operací pro každý GQL model
- 6.1. = počátek vytváření testů
- 29.1. = první pokus o test
- 5.2. = zprovoznění testů (77%)
- 6.2. = 89 % pokrytí testů
________________________________________________________________________

## Poznámky

Důležité termíny

- 7.10.2024 vybraná témata, publikované repositories
- 7.11.2024 1. projektový den, doložení kompletních descriptions (gql modely)
- 9.12.2024 2. projektový den, doložení funkcionality (crud)
- 29.1.2025 3. projektový den, doložení testů

## Poznámky pro spuštění

- uvicorn main:app --env-file enviroment.txt --reload (pro spuštění GQL modelů)

- pytest --cov=DBs --cov=GQLs --cov-report term-missing --log-cli-level=INFO -x (pro spuštění testů)