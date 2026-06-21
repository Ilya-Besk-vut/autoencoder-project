# Anomaly Detection using Autoencoders

Tento projekt představuje Proof of Concept (PoC) systému pro detekci anomálií a defektů v obraze pomocí hlubokého učení (autoencoderů). Model se trénuje výhradně na „normálních“ vzorcích (Unsupervised Learning) a detekuje defekty na základě chyby rekonstrukce (Reconstruction Error).

## Dataset
Pro realizaci projektu byl použit dataset **MVTec AD (kategorie bottle)**, který je k dispozici ke stažení na odkazu: [MVTec AD Dataset](https://www.mvtec.com/research-teaching/datasets/mvtec-ad/downloads).

Pro trénování autoencoderu byly použity fotografie ze složky `bottle/train/good`. Obrázky představují snímky skleněných lahví shora; všechny vzorky jsou původně vycentrované a upravené na jednotnou velikost.

## Struktura projektu

* `utils.py` – funkce pro preprocessing (předzpracování) dat: načítání obrázků, konverze do RGB, normalizace pixelů do rozsahu [0, 1] a změna velikosti (resize) na 64x64.
* `Autoencoder.ipynb` – Jupyter notebook s architekturou konvolučního autoencoderu (Convolutional Autoencoder – CAE), procesem trénování na „zdravých“ datech a uložením modelu (`AE.keras`).
* `Anomaly_detection.ipynb` – inference modelu: načtení testovacích dat, výpočet chyby (MSE), překrytí nalezených defektů červenou maskou a vizualizace (Explainable AI).

## Aktuální stav
Projekt úspěšně zvládá základní detekci defektů na vycentrovaných obrázcích fixní velikosti. V této fázi však model generuje poměrně nepřesnou binární masku lokalizace defektu přes původní obrázek (rozmazání obrysů souvisí s nízkým vstupním rozlišením $64 \times 64$).

---

## Známá omezení a možnosti rozvoje

### 1. Problém nestatické kamery (nevycentrované objekty)
**Podstata problému:** Současný model byl natrénován na dokonale vycentrovaných objektech. Pokud se kamera na dopravníkovém pásu posune nebo objekt projde pod mírným úhlem, autoencoder se pokusí rekonstruovat objekt uprostřed. Porovnání (MSE) posunutého originálu a vycentrované rekonstrukce pak způsobí falešně pozitivní detekce defektů podél všech okrajů objektu.

Jak se to plánuje řešit v produkci:
* Přístup A: 
  Před předáním snímku do autoencoderu najde lehký model pro detekci objektů (např. YOLOv8-nano nebo klasický OpenCV algoritmus pro hledání kontur `cv2.findContours`) samotnou součástku na pásu. Obrázek se ořízne (Crop) podle ohraničujícího rámečku (Bounding Box) součástky a teprve poté se změní jeho velikost na 64x64 a předá se do autoencoderu. To zaručí, že součástka bude vždy vycentrovaná.
* Přístup B:
  Přidání náhodných posunů (Translations), rotací a přiblížení (Zoom) do trénovací množiny. To přinutí autoencoder naučit se prostorově invariantní rysy (může to však mírně snížit citlivost na velmi malé defekty).

### 2. Dynamický výpočet prahové hodnoty
* Nyní: Prahová hodnota detekce je pevně nastavena v kódu (`THRESHOLD = 0.04`).
* Zlepšení: Implementace funkce, která nechá projít natrénovaným modelem validační sadu obsahující *pouze bezchybné* součástky, vykreslí rozdělení jejich chyb rekonstrukce a automaticky nastaví prahovou hodnotu na úroveň 95. nebo 99. percentilu. To systému umožní automaticky se adaptovat na nové světelné podmínky nebo nové typy součástek.

### 3. Rozlišení obrázků
* Pro kvalitní vyhledávání poškození (mikrotrhliny, škrábance) rozlišení `64x64` nestačí, protože malé defekty se při kompresi do latentního prostoru autoencoderu „rozmažou“. Plánuje se zvýšení vstupního rozlišení na `128x128` nebo `256x256` spolu s odpovídajícím prohloubením architektury neuronové sítě.

---

## Jak spustit

1. Nainstalujte potřebné závislosti: `tensorflow`, `numpy`, `matplotlib`, `pillow`.
2. Při použití originálního datasetu MVTec AD (bottle): vytvořte v kořenovém adresáři projektu složku `data` a vložte do ní rozbalenou složku `bottle`.
3. Spusťte Jupyter notebook `Autoencoder.ipynb` pro natrénování modelu.
4. Spusťte Jupyter notebook `Anomaly_detection.ipynb` pro kontrolu funkčnosti a vizualizaci výsledků.

Při použití vlastních dat:
 !Pamatujte, že současný model je optimalizován pro vycentrované obrázky lahví (pohled shora)!
* Umístěte trénovací data bez defektů do složky `./data/bottle/train/good`.
* Umístěte testovací data (s defekty i bez nich) do složek `./data/bottle/test/good` a `./data/bottle/test/broken_large`.
* Alternativa: Změňte cesty k adresářům přímo pomocí proměnných `TRAIN_FOLDER`, `TEST_FOLDER`, `GOOD_FOLDER`, `BRAKE_FOLDER` uvnitř notebooků.
