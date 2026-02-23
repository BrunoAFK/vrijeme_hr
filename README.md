# Vrijeme HR for Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

`vrijeme_hr` je neslužbena Home Assistant integracija za prikaz trenutnih meteoroloških podataka iz DHMZ XML izvora.

## Što integracija radi
- dohvaća trenutna mjerenja za odabrani grad
- može kreirati `sensor`, `weather` ili oba tipa entiteta
- konfiguracija ide kroz Home Assistant UI (`config_flow`)
- interval osvježavanja je podesiv

## Važno
- Integracija daje **trenutne uvjete** (observations), ne višednevnu prognozu.

## Izvor podataka
- Source: **DHMZ (Croatian Meteorological and Hydrological Service)**
- Podaci se dohvaćaju iz javnog DHMZ XML feeda.

## Instalacija
### HACS (preporučeno)
1. Otvori HACS.
2. Idi na `Integrations`.
3. U `Custom repositories` dodaj ovaj repo kao `Integration`.
4. Instaliraj `Vrijeme HR`.
5. Restartaj Home Assistant.

### Ručno
1. Kopiraj `custom_components/vrijeme_hr` u svoj HA `custom_components` direktorij.
2. Restartaj Home Assistant.

## Konfiguracija
1. `Settings` -> `Devices & Services` -> `Add Integration`.
2. Potraži `Vrijeme HR`.
3. Odaberi:
   - tip integracije (`sensor`, `weather`, `both`)
   - grad
   - interval osvježavanja

## Dostupni senzori
- temperatura
- vlaga
- tlak
- tendencija tlaka
- brzina vjetra
- smjer vjetra
- opis stanja
- geografska širina
- geografska dužina

## Pouzdanost i ponašanje
- robustnije parsiranje numeričkih vrijednosti iz feeda
- zaštita od neispravnih/praznih vrijednosti
- reload opcija nakon promjene postavki
- sprječavanje duplih unosa istog grada

## HACS update flow
HACS prikazuje update kada postoji novi release/tag i veći `version` u `manifest.json`.

Preporučeni flow:
1. Povećaj `custom_components/vrijeme_hr/manifest.json` -> `version`.
2. Merge/push na `main`.
3. Objavi release/tag `vX.Y.Z`.

## Attribution
- Data source: DHMZ
- Ova integracija je neslužbena i nije službeni DHMZ proizvod.

## Podrška
Bugove i prijedloge prijavi kroz GitHub Issues.
