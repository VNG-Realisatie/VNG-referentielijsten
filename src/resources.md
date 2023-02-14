# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## CommunicatieKanaal

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_2.0/doc/objecttype/communicatiekanaal)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | ja | ~~C~~​R​~~U~~​~~D~~ |
| naam | De gangbare naam van het communicatiekanaal. | string | ja | C​R​U​D |
| omschrijving | Toelichtende beschrijving van (de naam van) het communicatiekanaal. | string | ja | C​R​U​D |

## ProcesType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_2.0/doc/objecttype/procestype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | ja | ~~C~~​R​~~U~~​~~D~~ |
| nummer | Nummer van de selectielijstcategorie | integer | ja | C​R​U​D |
| jaar | Het jaartal waartoe dit ProcesType behoort | integer | ja | C​R​U​D |
| naam | Benaming van het procestype | string | ja | C​R​U​D |
| omschrijving | Omschrijving van het procestype | string | ja | C​R​U​D |
| toelichting | Toelichting van het procestype | string | ja | C​R​U​D |
| procesobject | Object waar de uitvoering van het proces op van toepassing is en waarvan de bestaans- of geldigheidsduur eventueel van belang is bij het bepalen van de start van de bewaartermijn | string | ja | C​R​U​D |

## Resultaat

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_2.0/doc/objecttype/resultaat)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | ja | ~~C~~​R​~~U~~​~~D~~ |
| procesType |  | string | ja | ~~C~~​R​~~U~~​~~D~~ |
| nummer | Nummer van het resultaat. Dit wordt samengesteld met het procestype en generiek resultaat indien van toepassing. | integer | ja | C​R​U​D |
| volledigNummer |  | string | ja | ~~C~~​R​~~U~~​~~D~~ |
| generiek |  | boolean | ja | ~~C~~​R​~~U~~​~~D~~ |
| specifiek |  | boolean | ja | ~~C~~​R​~~U~~​~~D~~ |
| naam | Benaming van het procestype | string | ja | C​R​U​D |
| omschrijving | Omschrijving van het specifieke resultaat | string | nee | C​R​U​D |
| herkomst | Voorbeeld: &#x27;Risicoanalyse&#x27;, &#x27;Systeemanalyse&#x27; of verwijzing naar Wet- en regelgeving | string | ja | C​R​U​D |
| waardering |  |  | ja | C​R​U​D |
| procestermijn | Uitleg bij mogelijke waarden:

* `nihil` - Nihil
* `bestaansduur_procesobject` - De bestaans- of geldigheidsduur van het procesobject.
* `ingeschatte_bestaansduur_procesobject` - De ingeschatte maximale bestaans- of geldigheidsduur van het procesobject.
* `vast_te_leggen_datum` - De tijdens het proces vast te leggen datum waarop de geldigheid van het procesobject komt te vervallen. 
* `samengevoegd_met_bewaartermijn` - De procestermijn is samengevoegd met de bewaartermijn. |  | nee | C​R​U​D |
| procestermijnWeergave |  | string | ja | ~~C~~​R​~~U~~​~~D~~ |
| bewaartermijn |  | string | nee | C​R​U​D |
| toelichting |  | string | nee | C​R​U​D |
| algemeenBestuurEnInrichtingOrganisatie |  | boolean | nee | C​R​U​D |
| bedrijfsvoeringEnPersoneel |  | boolean | nee | C​R​U​D |
| publiekeInformatieEnRegistratie |  | boolean | nee | C​R​U​D |
| burgerzaken |  | boolean | nee | C​R​U​D |
| veiligheid |  | boolean | nee | C​R​U​D |
| verkeerEnVervoer |  | boolean | nee | C​R​U​D |
| economie |  | boolean | nee | C​R​U​D |
| onderwijs |  | boolean | nee | C​R​U​D |
| sportCultuurEnRecreatie |  | boolean | nee | C​R​U​D |
| sociaalDomein |  | boolean | nee | C​R​U​D |
| volksgezonheidEnMilieu |  | boolean | nee | C​R​U​D |
| vhrosv |  | boolean | nee | C​R​U​D |
| heffenBelastingen |  | boolean | nee | C​R​U​D |
| alleTaakgebieden |  | boolean | nee | C​R​U​D |
| procestermijnOpmerking | Voorbeeld: &#x27;25 jaar&#x27;, &#x27;30 jaar, &#x27;5 of 10 jaar&#x27; | string | nee | C​R​U​D |

## ResultaattypeOmschrijvingGeneriek

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_2.0/doc/objecttype/resultaattypeomschrijvinggeneriek)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | ja | ~~C~~​R​~~U~~​~~D~~ |
| omschrijving | Algemeen gehanteerde omschrijvingen van de aard van het resultaat van zaken | string | ja | C​R​U​D |
| definitie | Nauwkeurige beschrijving van het generieke type resultaat. | string | ja | C​R​U​D |
| opmerking | Zinvolle toelichting bij de waarde van de generieke omschrijving van het resultaat. | string | nee | C​R​U​D |


* Create, Read, Update, Delete
